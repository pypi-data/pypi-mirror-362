import jax
import jax.numpy as jnp
import equinox
from jax.scipy.linalg import block_diag
from qpax import solve_qp_primal
import functools
from dynamaxsys.utils import linearize
from dynamaxsys.base import Dynamics
from utils import expand_to_include_slack, extract_solution

solve_qp_jit = jax.jit(solve_qp_primal)

class SQPParams(equinox.Module):
    dynamics: equinox.Module
    Qs_state: jnp.ndarray
    Rs_control: jnp.ndarray
    qs_state: jnp.ndarray
    rs_control: jnp.ndarray
    Qs_trust_region: jnp.ndarray
    Rs_trust_region: jnp.ndarray
    trust_region_weight: float
    slack_weight: float
    u_max: jnp.ndarray
    u_min: jnp.ndarray
    planning_horizon: int
    dt: float

from typing import Optional, Union


class SQPProblem(equinox.Module):
    params: equinox.Module
    z_dim: int
    state_block_size: int

    def __init__(self, sqp_params):
        self.params = sqp_params
        state_dim = self.params.dynamics.state_dim
        control_dim = self.params.dynamics.control_dim
        # z = [x0, x1, ..., xN, u0, ..., uN-1], N = planning horizon
        self.z_dim = (
            state_dim * (self.params.planning_horizon + 1)
            + control_dim * self.params.planning_horizon
        )

        self.state_block_size = (
            self.params.planning_horizon + 1
        ) * state_dim

    @equinox.filter_jit
    def _construct_control_limit_constraints(self):
        plan_horizon = self.params.planning_horizon
        control_dim = self.params.dynamics.control_dim
        G_u = jnp.zeros([control_dim * plan_horizon, self.z_dim])
        G_l = jnp.zeros([control_dim * plan_horizon, self.z_dim])
        for i in range(plan_horizon):
            G_u = jax.lax.dynamic_update_slice(G_u, jnp.eye(control_dim), (i * control_dim, self.state_block_size + i * control_dim))
            G_l = jax.lax.dynamic_update_slice(G_l, -jnp.eye(control_dim), (i * control_dim, self.state_block_size + i * control_dim))

        h_ulim = jnp.concatenate(
            [
                jnp.tile(self.params.u_max, plan_horizon),
                -jnp.tile(self.params.u_min, plan_horizon),
            ]
        )

        G_ulim = jnp.concatenate([G_u, G_l], 0)
        return G_ulim, h_ulim

    @equinox.filter_jit
    def _construct_initial_state_constraint(self, initial_state):
        state_dim = initial_state.shape[0]
        assert state_dim == self.params.dynamics.state_dim, "State dimension mismatch"

        A_init = jnp.zeros([state_dim, self.z_dim])
        A_init = jax.lax.dynamic_update_slice(A_init, jnp.eye(state_dim), (0, 0))
        b_init = initial_state

        return A_init, b_init


    @equinox.filter_jit
    def _construct_planning_cost(self):
        quadratic = block_diag(*self.params.Qs_state, *self.params.Rs_control)
        linear = jnp.concatenate(
            [
                jnp.concatenate(self.params.qs_state, 0),
                jnp.concatenate(self.params.rs_control, 0),
            ]
        )
        return quadratic, linear

    @equinox.filter_jit
    def _construct_trust_region_cost(self, previous_states, previous_controls):
        plan_horizon = self.params.planning_horizon

        assert previous_states.shape[0] == plan_horizon + 1, (
            "Number of previous_states do not matched expected planning horizon"
        )
        assert previous_controls.shape[0] == plan_horizon, (
            "Number of previous_controls do not matched expected planning horizon"
        )

        quadratic = block_diag(
            *self.params.Qs_trust_region, *self.params.Rs_trust_region
        )
        qtrs = jnp.stack(
            [-x.T @ Q for (x, Q) in zip(previous_states, self.params.Qs_trust_region)]
        )
        rtrs = jnp.stack(
            [-u.T @ R for (u, R) in zip(previous_controls, self.params.Rs_trust_region)]
        )
        linear = jnp.concatenate([jnp.concatenate(qtrs, 0), jnp.concatenate(rtrs, 0)])

        return quadratic, linear

    @equinox.filter_jit
    def _construct_sqp_cost(self, states, controls):
        Q_plan, q_plan = self._construct_planning_cost()
        Q_trust, q_trust = self._construct_trust_region_cost(states, controls)

        return (
            Q_plan + self.params.trust_region_weight * Q_trust,
            q_plan + self.params.trust_region_weight * q_trust,
        )

    @equinox.filter_jit
    def _construct_dynamics_constraints(self, states, controls, time=0.0):
        plan_horizon = self.params.planning_horizon

        As, Bs, Cs = jax.vmap(linearize, in_axes=(None, 0, 0, None))(
            self.params.dynamics, states[:-1], controls, time
        )
        state_dim = As[0].shape[0]
        control_dim = Bs[0].shape[1]

        def scan_fn(A_dyn, i):
            A_dyn = jax.lax.dynamic_update_slice(A_dyn, As[i], (i * state_dim, i * state_dim))
            A_dyn = jax.lax.dynamic_update_slice(A_dyn, -jnp.eye(state_dim), (i * state_dim, (i + 1) * state_dim))
            A_dyn = jax.lax.dynamic_update_slice(A_dyn, Bs[i], (i * state_dim, self.state_block_size + i * control_dim))
            return A_dyn, None

        # Create block matrices for the linear dynamics constraint
        A_dyn = jnp.zeros([plan_horizon * state_dim, self.z_dim])
        A_dyn, _ = jax.lax.scan(scan_fn, A_dyn, jnp.arange(plan_horizon))

        b_dyn = -jnp.concatenate(Cs, 0)

        return A_dyn, b_dyn


    @equinox.filter_jit
    def _construct_state_control_constraints(
        self,
        state_control_obstacle_constraint,
        states,
        controls,
        add_slack=False,
        pad=0,
    ):
        """
        Construct state-control obstacle constraints for the SQP problem. The obstacle constraints are linearized around the states and controls provided.

        NOTE: This function will pass the obstacle constraint over each state and control. For constraint functions evaluated over the entire trajectory, use the `_construct_trajectory_constraint` instead.

        Parameters:
        state_control_obstacle_constraint (Callable): Function that defines the obstacle constraints for a (state, control) pair only.
        states (Array): Array of states over the planning horizon.
        controls (Array): Array of controls over the planning horizon.
        add_slack (bool): Whether to add slack variables to the constraints.
        pad (int): Number of additional columns to add to the constraint matrix to accomodate additional variables.

        Returns:
        Tuple: Tuple containing the constraint matrix, constraint vector, and number of slack variables.
        """
        def false_func(operands):
            # no slack
            # need to output the same size as the true_func
            # need to dynamically slice the G_xu_obs_with_slack to the correct size outside if this function
            G_xu_obs, h_xu_obs = operands
            n_slack = G_xu_obs.shape[0]  # number of slack variables needed
            G_xu_obs_with_slack = jnp.zeros(
                [2 * n_slack, G_xu_obs.shape[1] + n_slack]
            )  # twice as tall, and wider by n_slack

            G_xu_obs_with_slack = jax.lax.dynamic_update_slice(G_xu_obs_with_slack, G_xu_obs, (0, 0)) # top left block is the original constraint

            h_xu_obs_with_slack = jnp.concatenate(
                [h_xu_obs, jnp.zeros(n_slack)]
            )  # extend the h vector to accomodate the slack variables positive constraint

            return G_xu_obs_with_slack, h_xu_obs_with_slack, 0

        def true_func(operands):
            # with slack
            G_xu_obs, h_xu_obs = operands
            # add slack variables to the constraints
            n_slack = G_xu_obs.shape[0]  # number of slack variables needed
            # make the constraint block matrix bigger to accomodate the slack variables
            G_xu_obs_with_slack = jnp.zeros(
                [2 * n_slack, G_xu_obs.shape[1] + n_slack]
            )  # twice as tall, and wider by n_slack

            G_xu_obs_with_slack = jax.lax.dynamic_update_slice(G_xu_obs_with_slack, G_xu_obs, (0, 0)) # top left block is the original constraint
            G_xu_obs_with_slack = jax.lax.dynamic_update_slice(G_xu_obs_with_slack, -jnp.eye(n_slack), (0, -n_slack)) # top right block is added slack to the inequality constraint
            G_xu_obs_with_slack = jax.lax.dynamic_update_slice(G_xu_obs_with_slack, -jnp.eye(n_slack), (n_slack, -n_slack)) # bottom right block to ensure slack is positive

            h_xu_obs_with_slack = jnp.concatenate(
                [h_xu_obs, jnp.zeros(n_slack)]
            )  # extend the h vector to accomodate the slack variables positive constraint

            return G_xu_obs_with_slack, h_xu_obs_with_slack, n_slack

        if state_control_obstacle_constraint is None:
            return jnp.zeros([0, self.z_dim + pad]), jnp.zeros(0), 0 # G, h, n_slack

        plan_horizon = self.params.planning_horizon
        state_dim = self.params.dynamics.state_dim
        control_dim = self.params.dynamics.control_dim

        # get jacobian wrt state and control variables
        # will not apply to the last state as it does not have a control associated with it
        dxs, dus = jax.vmap(
            jax.jacfwd(state_control_obstacle_constraint, (0, 1)), in_axes=[0, 0]
        )(states[:-1], controls)
        n_constraints = dxs[0].shape[0]

        G_xu_obs = jnp.zeros([n_constraints * plan_horizon, self.z_dim + pad])

        # looping through and filling in the matrix with jacobian at each state-control pair
        def scan_fn(G_xu_obs, i):
            dx = dxs[i]
            du = dus[i]
            G_xu_obs = jax.lax.dynamic_update_slice(G_xu_obs, dx, (i * n_constraints, i * state_dim))
            G_xu_obs = jax.lax.dynamic_update_slice(G_xu_obs, du, (i * n_constraints, self.state_block_size + i * control_dim))
            return G_xu_obs, None

        G_xu_obs, _ = jax.lax.scan(
            scan_fn, G_xu_obs, jnp.arange(len(dxs))
        )

        h_xu_obs = -jnp.concatenate(
            jax.vmap(
                lambda x, u, dx, du: state_control_obstacle_constraint(x, u)
                - dx @ x
                - du @ u,
                in_axes=[0, 0, 0, 0],
            )(states[:-1], controls, dxs, dus),
            0,
        )

        return jax.lax.cond(add_slack, true_func, false_func, (G_xu_obs, h_xu_obs))

    @equinox.filter_jit
    def _construct_state_constraints(
        self, state_obstacle_constraint, states, add_slack=False, pad=0
    ):
        """
        Construct obstacle constraints for the SQP problem. The obstacle constraints are linearized around the states provided.

        NOTE: This function will pass the obstacle constraint over each state. For constraint functions evaluated over the entire trajectory, use the `_construct_trajectory_constraint` instead.

        Parameters:
        state_obstacle_constraint (Callable): Function that defines the obstacle constraints for a states only.
        states (Array): Array of states over the planning horizon.
        add_slack (bool): Whether to add slack variables to the constraints.
        pad (int): Number of additional columns to add to the constraint matrix to accomodate additional variables.

        Returns:
        Tuple: Tuple containing the constraint matrix, constraint vector, and number of slack variables.
        """

        def false_func(operands):
            # need to output the same size as the true_func
            # need to dynamically slice the G_xu_obs_with_slack to the correct size outside if this function
            G_x_obs, h_x_obs = operands
            n_slack = G_x_obs.shape[0]  # number of slack variables needed
            G_x_obs_with_slack = jnp.zeros(
                [2 * n_slack, G_x_obs.shape[1] + n_slack]
            )  # twice as tall, and wider by n_slack

            G_x_obs_with_slack = jax.lax.dynamic_update_slice(G_x_obs_with_slack, G_x_obs, (0, 0)) # top left block is the original constraint

            h_x_obs_with_slack = jnp.concatenate(
                [h_x_obs, jnp.zeros(n_slack)]
            )  # extend the h vector to accomodate the slack variables positive constraint

            return G_x_obs_with_slack, h_x_obs_with_slack, 0

        def true_func(operands):
            G_x_obs, h_x_obs = operands
            # add slack variables to the constraints
            n_slack = G_x_obs.shape[0]  # number of slack variables needed
            # make the constraint block matrix bigger to accomodate the slack variables
            G_x_obs_with_slack = jnp.zeros(
                [2 * n_slack, G_x_obs.shape[1] + n_slack]
            )  # twice as tall, and wider by n_slack

            G_x_obs_with_slack = jax.lax.dynamic_update_slice(G_x_obs_with_slack, G_x_obs, (0, 0)) # top left block is the original constraint
            G_x_obs_with_slack = jax.lax.dynamic_update_slice(G_x_obs_with_slack, -jnp.eye(n_slack), (0, -n_slack)) # top right block is added slack to the inequality constraint
            G_x_obs_with_slack = jax.lax.dynamic_update_slice(G_x_obs_with_slack, -jnp.eye(n_slack), (n_slack, -n_slack)) # bottom right block to ensure slack is positive

            h_x_obs_with_slack = jnp.concatenate(
                [h_x_obs, jnp.zeros(n_slack)]
            )  # extend the h vector to accomodate the slack variables positive constraint

            return G_x_obs_with_slack, h_x_obs_with_slack, n_slack

        if state_obstacle_constraint is None:
            return jnp.zeros([0, self.z_dim + pad]), jnp.zeros(0), 0

        plan_horizon = self.params.planning_horizon
        state_dim = self.params.dynamics.state_dim


        dxs = jax.vmap(jax.jacfwd(state_obstacle_constraint, (0)), in_axes=[0])(states)
        n_constraints = dxs[0].shape[0]

        G_x_obs = jnp.zeros([n_constraints * (plan_horizon + 1), self.z_dim + pad])



        # looping through and filling in the matrix with jacobian at each state
        def scan_fn(G_x_obs, i):
            dx = dxs[i]
            G_x_obs = jax.lax.dynamic_update_slice(G_x_obs, dx, (i * n_constraints, i * state_dim))
            return G_x_obs, None

        G_x_obs, _ = jax.lax.scan(
            scan_fn, G_x_obs, jnp.arange(len(dxs))
        )

        h_x_obs = -jnp.concatenate(
            jax.vmap(
                lambda x, dx: state_obstacle_constraint(x) - dx @ x, in_axes=[0, 0]
            )(states, dxs),
            0,
        )

        return jax.lax.cond(add_slack, true_func, false_func, (G_x_obs, h_x_obs))

    @equinox.filter_jit
    def linearize_and_update_constraints(
        self,
        states,
        controls,
        state_constraint_function,
        state_control_constraint_function,
        add_slack=False,
    ):
        # Construct the state constraints
        _G_x_obs_tmp, _h_x_obs, _ = self._construct_state_constraints(
            state_constraint_function, states, add_slack
        )  # G_x_obs has size [n_constraints * (plan_horizon + 1), z_dim + n_slack_x_obs], h_x_obs has size [n_constraints * (plan_horizon + 1)]

        n_x_cons = _G_x_obs_tmp.shape[0] // 2 # half is actual constraints, half is slack
        n_slack_x_obs = n_x_cons * add_slack
        _G_x_obs = jax.lax.dynamic_slice(_G_x_obs_tmp, (0,0), (n_x_cons + n_slack_x_obs , self.z_dim + n_slack_x_obs)) # If no slack, remove the padding
        h_x_obs = jax.lax.dynamic_slice(_h_x_obs, (0,), (n_x_cons + n_slack_x_obs,))


        _G_xu_obs, _h_xu_obs, _ = self._construct_state_control_constraints(
            state_control_constraint_function,
            states,
            controls,
            add_slack,
            pad=n_x_cons*add_slack,  # pad the constraint matrix to accomodate the slack variables from the state constraints
        )  # G_xu_obs has size [n_constraints * plan_horizon, z_dim + n_slack_x_obs + n_slack_xu_obs], h_xu_obs has size [n_constraints * plan_horizon]

        n_xu_cons = _G_xu_obs.shape[0] // 2 # half is actual constraints, half is slack
        n_slack_xu_obs = n_xu_cons * add_slack
        G_xu_obs = jax.lax.dynamic_slice(_G_xu_obs, (0,0), (n_xu_cons + n_slack_xu_obs, self.z_dim + n_slack_xu_obs + n_slack_x_obs)) # If no slack, remove the padding
        h_xu_obs = jax.lax.dynamic_slice(_h_xu_obs, (0,), (n_xu_cons + n_slack_xu_obs,))

        n_slack = n_slack_x_obs + n_slack_xu_obs

        G_x_obs = expand_to_include_slack(
            n_slack_xu_obs, _G_x_obs
        )  # expand G_x_obs to include the slack variables from G_xu_obs

        _G_ctrl, _h_ctrl = self._construct_control_limit_constraints()
        G_ctrl = expand_to_include_slack(
            n_slack, _G_ctrl
        )  # expand G_ctrl to include the slack variables

        G_sqp = jnp.concatenate([G_ctrl, G_x_obs, G_xu_obs], 0)
        h_sqp = jnp.concatenate([_h_ctrl, h_x_obs, h_xu_obs], 0)

        return G_sqp, h_sqp, n_slack

    @equinox.filter_jit
    def update_sqp_cost(self, states, controls, n_slack):
        _Q_sqp, _q_sqp = self._construct_sqp_cost(
            states, controls
        )

        Q_sqp = block_diag(
            _Q_sqp, self.params.slack_weight * jnp.eye(n_slack)
        )
        q_sqp = jnp.concatenate([_q_sqp, jnp.zeros(n_slack)])
        return Q_sqp, q_sqp


    @equinox.filter_jit
    def construct_sqp_problem(
        self,
        states,
        controls,
        initial_state,
        state_constraint_function,
        state_control_constraint_function,
        add_slack=False,
    ):
        """
        Construct the SQP problem for the given states and controls.

        Parameters:
            states (Array): Array of states over the planning horizon.
            controls (Array): Array of controls over the planning horizon.
            initial_state (Array): Initial state of the system.
            state_constraint_function (Tuple): Tuple containing the constraint matrix, constraint vector, and number of slack variables for the state constraints.
            state_control_constraint_function (Tuple): Tuple containing the constraint matrix, constraint vector, and number of slack variables for the state-control constraints.

        Returns:
        Tuple: Tuple containing the quadratic cost matrix, linear cost vector, constraint matrix, constraint vector, and number of slack variables.
        """

        # self.n_slack is updated in the linearize_and_update_constraints function
        # self.G_sqp and self.h_sqp are updated here
        G_sqp, h_sqp, n_slack = self.linearize_and_update_constraints(
            states,
            controls,
            state_constraint_function,
            state_control_constraint_function,
            add_slack,
        )



        # Construct the dynamics constraints
        _A_dyn, _b_dyn = self._construct_dynamics_constraints(states, controls)

        # Construct the initial state constraint
        _A_init, _b_init = self._construct_initial_state_constraint(initial_state)

        # initial state constraint always at the bottom
        A_sqp = expand_to_include_slack(n_slack, jnp.concatenate([_A_dyn, _A_init], 0))
        b_sqp = jnp.concatenate([_b_dyn, _b_init], 0)

        Q_sqp, q_sqp = self.update_sqp_cost(states, controls, n_slack)

        return Q_sqp, q_sqp, A_sqp, b_sqp, G_sqp, h_sqp



@equinox.filter_jit
def run_sqp_loop(problem, sqp_matrices, initial_state, n_sqp_iterations=5, state_constraint_function=None, state_control_constraint_function=None, add_slack=True, solver_tol=1E-4):
    def scan_fn(sqp_matrices, x):
        z = solve_qp_jit(*sqp_matrices, solver_tol=solver_tol)
        xs, us, slack = extract_solution(z, problem)
        sqp_matrices = problem.construct_sqp_problem(
            xs,
            us,
            initial_state,  # initial state is the first state in the trajectory
            state_constraint_function,
            state_control_constraint_function,
            add_slack=add_slack,
        )
        return sqp_matrices,  (sqp_matrices, xs, us, slack)

    return jax.lax.scan(
        scan_fn, sqp_matrices, jnp.arange(n_sqp_iterations)
    )
