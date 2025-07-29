
import jax
import jax.numpy as jnp
from jax.scipy.linalg import block_diag
import matplotlib.pyplot as plt
from qpax import solve_qp_primal
import functools
from dynamaxsys.utils import linearize



def construct_dynamics_matrix_constraints(ABCs, time_horizon):

    """
    Constructs the block matrix for the linear dynamics constraints Az = b where z = [x0, x1, ..., xT+1, u0, ..., uT]
    and linear dynamics are given by x_{t+1} = A_t x_t + B_t u_t + C_t.
    Parameters:
    ABCs (tuple): A tuple containing three lists of matrices (As, Bs, Cs) where:
        - As (list of ndarray): List of state transition matrices A_t for each time step t.
        - Bs (list of ndarray): List of control matrices B_t for each time step t.
        - Cs (list of ndarray): List of constant vectors C_t for each time step t.
    time_horizon (int): The number of time steps in the time horizon.
    Returns:
    tuple: A tuple containing:
        - dyn_block_matrix (ndarray): The block matrix representing the linear dynamics constraints.
        - dyn_vector (ndarray): The vector representing the constant terms in the linear dynamics constraints.
    """

    As, Bs, Cs = ABCs
    state_dim = As[0].shape[0]
    control_dim = Bs[0].shape[1]
    # Create block matrices for the linear dynamics constraint
    dyn_block_matrix = jnp.zeros((time_horizon * state_dim, (time_horizon + 1) * state_dim + time_horizon * control_dim))

    for i in range(time_horizon):
        dyn_block_matrix = dyn_block_matrix.at[i * state_dim:(i + 1) * state_dim, i * state_dim:(i + 1) * state_dim].set(As[i])
        dyn_block_matrix = dyn_block_matrix.at[i * state_dim:(i + 1) * state_dim, (i + 1) * state_dim:(i + 2) * state_dim].set(-jnp.eye(state_dim))
        dyn_block_matrix = dyn_block_matrix.at[i * state_dim:(i + 1) * state_dim, (time_horizon + 1) * state_dim + i * control_dim:(time_horizon + 1) * state_dim + (i + 1) * control_dim].set(Bs[i])

    dyn_vector = -jnp.concatenate(Cs, 0)
    return dyn_block_matrix, dyn_vector


def construct_initial_state_constraint(initial_state, control_dim, time_horizon):
    """"
    Constructs the block matrix and vector for the initial state constraint x0 = x0_init.
    Parameters:
    initial_state (jnp.ndarray): The initial state vector.
    control_dim (int): The dimension of the control input.
    time_horizon (int): The time horizon for the constraint.
    Returns:
    tuple: A tuple containing:
        - initial_state_block_matrix (jnp.ndarray): The block matrix for the initial state constraint.
        - initial_state_vector (jnp.ndarray): The initial state vector.

    """
    state_dim = initial_state.shape[0]
    initial_state_block_matrix = jnp.zeros((state_dim, (time_horizon + 1) * state_dim + time_horizon * control_dim))
    initial_state_block_matrix = initial_state_block_matrix.at[0:state_dim, 0:state_dim].set(jnp.eye(state_dim))
    initial_state_vector = initial_state
    return initial_state_block_matrix, initial_state_vector

def construct_control_limit_constraints(u_min, u_max, state_dim, time_horizon):
    """
    Constructs control limit constraints for an optimization problem.
    Parameters:
    u_min (jnp.ndarray): The minimum control limits, a 1D array of shape (control_dim,).
    u_max (jnp.ndarray): The maximum control limits, a 1D array of shape (control_dim,).
    state_dim (int): The dimension of the state vector.
    time_horizon (int): The time horizon for the optimization problem.
    Returns:
    tuple: A tuple (G, h) where:
        - G (jnp.ndarray): The constraint matrix of shape (2 * control_dim * time_horizon, (time_horizon + 1) * state_dim + time_horizon * control_dim).
        - h (jnp.ndarray): The constraint vector of shape (2 * control_dim * time_horizon,).
    """

    control_dim = u_min.shape[0]
    state_block_size = (time_horizon + 1) * state_dim
    G_u = jnp.zeros([control_dim * time_horizon, (time_horizon + 1) * state_dim + time_horizon * control_dim])
    for i in range(time_horizon):
        G_u = G_u.at[i * control_dim:(i + 1) * control_dim,
                     state_block_size + i * control_dim:state_block_size + (i + 1) * control_dim].set(jnp.eye(control_dim))

    G_l = jnp.zeros([control_dim * time_horizon, (time_horizon + 1) * state_dim + time_horizon * control_dim])
    for i in range(time_horizon):
        G_l = G_l.at[i * control_dim:(i + 1) * control_dim,
                     state_block_size + i * control_dim:state_block_size + (i + 1) * control_dim].set(-jnp.eye(control_dim))
    h = jnp.concatenate([jnp.tile(u_max, time_horizon), -jnp.tile(u_min, time_horizon)])

    G = jnp.concatenate([G_u, G_l], 0)
    return G, h


def construct_planning_objective(Qs, Rs, qs, rs, x_goal):
    """
    Constructs the objective function for the optimization problem.

    Args:
        Qs list: List of state cost matrices for each time step, up to time_horizon+1
        Rs list: List of cntrol cost matrices for each time step, up to time_horizon
        x_goal (jnp.ndarray): Goal state.

    Returns:
        jnp.ndarray: Block diagonal matrix combining Qs and Rs.
    """
    assert len(Qs) == len(Rs) + 1, "must have len(Qs) == len(Rs)+1"
    time_horizon = len(Rs)
    state_dim = Qs[0].shape[0]
    quadratic = block_diag(*Qs, *Rs)
    linear = jnp.concatenate([jnp.concatenate(qs, 0), jnp.concatenate(rs, 0)])
    linear += linear.at[time_horizon * state_dim: (time_horizon + 1) * state_dim].set(-x_goal.T @ Qs[-1])

    return quadratic, linear


def construct_trust_region_objective(Qs, Rs, previous_states, previous_controls):
    """
    Constructs the objective function for the optimization problem.

    Args:
        Qs list: List of state cost matrices for each time step, up to time_horizon+1
        Rs list: List of cntrol cost matrices for each time step, up to time_horizon
        x_goal (jnp.ndarray): Goal state.

    Returns:
        jnp.ndarray: Block diagonal matrix combining Qs and Rs.
    """
    assert len(Qs) == len(Rs) + 1, "must have len(Qs) == len(Rs)+1"
    quadratic = block_diag(*Qs, *Rs)
    qtrs = jnp.stack([-x.T @ Q for(x,Q) in zip(previous_states, Qs)])
    rtrs = jnp.stack([-u.T @ R for(u,R) in zip(previous_controls, Rs)])
    linear = jnp.concatenate([jnp.concatenate(qtrs, 0), jnp.concatenate(rtrs, 0)])

    return quadratic, linear

def construct_linearized_state_control_constraints(constraint_function, reference_states, reference_controls):
    """
    Constructs linearized state-control constraints for the optimization problem.

    Args:
        constraint_function: A function that computes the constraint values given state and control.
        reference_states: A (time_horizon+1, state_dim) array of reference states.
        reference_controls: A (time_horizon, control_dim) array of reference controls.

    Returns:
        G: A (n_constraints * time_horizon, (time_horizon + 1) * state_dim + time_horizon * control_dim) array representing the linearized constraints.
        h: A (n_constraints * time_horizon,) array representing the constraint bounds.
    """
    time_horizon = reference_controls.shape[0]
    state_dim = reference_states.shape[1]
    control_dim = reference_controls.shape[1]
    dxs, dus = jax.vmap(jax.jacfwd(constraint_function, (0, 1)), in_axes=[0, 0])(reference_states[:time_horizon], reference_controls)
    n_constraints = dxs[0].shape[0]
    n_state_block = (time_horizon+1) * state_dim
    G = jnp.zeros([n_constraints * time_horizon, (time_horizon + 1) * state_dim + time_horizon * control_dim])
    for (i, (dx, du)) in enumerate(zip(dxs, dus)):
        G = G.at[i*n_constraints:(i+1)*n_constraints, i*state_dim:(i+1)*state_dim].set(dx)
        G = G.at[i*n_constraints:(i+1)*n_constraints, n_state_block+i*control_dim:n_state_block+(i+1)*control_dim].set(du)
    h = -jnp.concatenate(jax.vmap(lambda x, u, dx, du: constraint_function(x, u) - dx @ x - du @ u)(reference_states[:-1], reference_controls, dxs, dus), 0)
    return G, h

def construct_linearized_state_constraints(constraint_function, reference_states, control_dim, slack=False):
    """
    Constructs linearized state constraints for the optimization problem.

    Args:
        constraint_function: A function that computes the constraint values given state.
        reference_states: A (time_horizon+1, state_dim) array of reference states.
        control_dim: The dimension of the control input.
        slack: A boolean indicating whether to add slack variables to the constraints.

    Returns:
        G: A (n_constraints * time_horizon, (time_horizon + 1) * state_dim + time_horizon * control_dim) array representing the linearized constraints.
        h: A (n_constraints * time_horizon,) array representing the constraint bounds.
    """
    time_horizon = reference_states.shape[0] - 1
    state_dim = reference_states.shape[1]
    dxs = jax.vmap(jax.jacfwd(constraint_function, (0)), in_axes=[0])(reference_states)
    n_constraints = dxs[0].shape[0]
    G = jnp.zeros([n_constraints * (time_horizon+1), (time_horizon + 1) * state_dim + time_horizon * control_dim])
    for (i, (dx,)) in enumerate(zip(dxs,)):
        G = G.at[i*n_constraints:(i+1)*n_constraints, i*state_dim:(i+1)*state_dim].set(dx)
    h = -jnp.concatenate(jax.vmap(lambda x, dx: constraint_function(x) - dx @ x)(reference_states, dxs), 0)

    if not slack:
        return G, h, 0

    n_slack = G.shape[0]
    G_with_slack = jnp.zeros([2 * n_slack, G.shape[1] + n_slack])
    G_with_slack = G_with_slack.at[:n_slack, :G.shape[1]].set(G)
    G_with_slack = G_with_slack.at[n_slack:, -n_slack:].set(-jnp.eye(n_slack))
    G_with_slack = G_with_slack.at[:n_slack, -n_slack:].set(-jnp.eye(n_slack))
    h_with_slack = jnp.concatenate([h, jnp.zeros(n_slack)])
    return G_with_slack, h_with_slack, n_slack


@functools.partial(jax.jit, static_argnames=["state_constraint_function", "dynamics", "slack"])
def solve_subproblem_nonlinear_constraint(state_constraint_function,
                                          previous_states,
                                          previous_controls,
                                          dynamics,
                                          A_base,
                                          b_base,
                                          G_ulim,
                                          h_ulim,
                                          Q_base,
                                          q_base,
                                          Qtrs,
                                          Rtrs,
                                          tr_weight,
                                          time_horizon,
                                          slack,
                                          slack_weight):



    # Define the constraint function
    # TODO: update constraint to be state and control constraint
    G_obs, h_obs, n_slack = construct_linearized_state_constraints(state_constraint_function, previous_states, dynamics.control_dim, slack=slack)
    # get penalized trust region linear term
    quad_tr, linear_tr = construct_trust_region_objective(Qtrs, Rtrs, previous_states, previous_controls)
    Q_tr = Q_base + tr_weight * quad_tr
    q_tr = q_base + tr_weight * linear_tr


    G_ulim_slack = expand_to_include_slack(n_slack, G_ulim)
    A_slack = expand_to_include_slack(n_slack, A_base)
    Q_objective = block_diag(Q_tr, slack_weight * jnp.eye(n_slack))
    q_objective = jnp.concatenate([q_tr, jnp.zeros(n_slack)])


    G_slack = jnp.concatenate([G_ulim_slack, G_obs], axis=0)
    h_slack = jnp.concatenate([h_ulim, h_obs], axis=0)

    z = solve_qp_primal(Q_objective,
                 q_objective,
                 A_slack,
                 b_base,
                 G_slack,
                 h_slack,
                 solver_tol=1e-6)
    return z



@functools.partial(jax.jit, static_argnames=["state_constraint_function", "dynamics", "slack", "time_horizon"])
def linearize_and_solve_subproblem(dynamics,
                                   state_constraint_function,
                                   previous_states,
                                   previous_controls,
                                   initial_state,
                                   time,
                                   G_ulim,
                                   h_ulim,
                                   Q_base,
                                   q_base,
                                   Qtrs,
                                   Rtrs,
                                   tr_weight,
                                   time_horizon,
                                   slack,
                                   slack_weight,
                                   dt=0.1):
    """
    Linearizes the dynamics and solves a quadratic programming subproblem.
    Parameters:
        dynamics (object): The dynamics object with a method `discrete_step`.
        state_constraint_function (callable): Function to compute state constraints.
        previous_states (array): Array of previous states.
        previous_controls (array): Array of previous controls.
        initial_state (array): The initial state of the system.
        time (array): Array of time steps.
        G_ulim (array): Control input constraint matrix.
        h_ulim (array): Control input constraint vector.
        Q_base (array): Base quadratic cost matrix.
        q_base (array): Base linear cost vector.
        Qtrs (array): Trust region quadratic cost matrix.
        Rtrs (array): Trust region linear cost matrix.
        tr_weight (float): Weight for the trust region term.
        time_horizon (int): Time horizon for the optimization.
        slack (bool): Whether to include slack variables.
        slack_weight (float): Weight for the slack variables.
        dt (float, optional): Time step for discretization. Default is 0.1.
    Returns:
    array: Solution to the quadratic programming problem.
    """

    discrete_dynamics = functools.partial(dynamics.discrete_step, dt=dt)
    ABCs = jax.vmap(linearize, in_axes=(None, 0, 0, None))(discrete_dynamics, previous_states[:-1], previous_controls, time)
    A_dyn, b_dyn = construct_dynamics_matrix_constraints(ABCs, time_horizon)
    A_init, b_init = construct_initial_state_constraint(initial_state, dynamics.control_dim, time_horizon)
    A_base = jnp.concatenate([A_dyn, A_init], 0)
    b_base = jnp.concatenate([b_dyn, b_init], 0)

    # Define the constraint function
    G_obs, h_obs, n_slack = construct_linearized_state_constraints(state_constraint_function, previous_states, dynamics.control_dim, slack=slack)
    # get penalized trust region linear term
    quad_tr, linear_tr = construct_trust_region_objective(Qtrs, Rtrs, previous_states, previous_controls)
    Q_tr = Q_base + tr_weight * quad_tr
    q_tr = q_base + tr_weight * linear_tr


    G_ulim_slack = expand_to_include_slack(n_slack, G_ulim)
    A_slack = expand_to_include_slack(n_slack, A_base)
    Q_objective = block_diag(Q_tr, slack_weight * jnp.eye(n_slack))
    q_objective = jnp.concatenate([q_tr, jnp.zeros(n_slack)])


    G_slack = jnp.concatenate([G_ulim_slack, G_obs], axis=0)
    h_slack = jnp.concatenate([h_ulim, h_obs], axis=0)

    z = solve_qp_primal(Q_objective,
                 q_objective,
                 A_slack,
                 b_base,
                 G_slack,
                 h_slack,
                 solver_tol=1e-6)
    return z


def solve_sqp(max_iter, dynamics, constraint_function, previous_states, previous_controls, initial_state, time, time_horizon, problem_params):
    for i in range(max_iter):
        # 50 ms
        z = linearize_and_solve_subproblem(dynamics,
                                           constraint_function,
                                           previous_states,
                                           previous_controls,
                                           initial_state,
                                           time,
                                           *problem_params)

        # TODO: figure out jit lax.dynamics slice issue
        stacked_xu = z[:(time_horizon + 1) * dynamics.state_dim  + time_horizon * dynamics.control_dim]
        previous_states, previous_controls = extract_xu(stacked_xu, dynamics.state_dim, dynamics.control_dim, time_horizon)
    return previous_states, previous_controls