import jax
import jax.numpy as jnp
import matplotlib.pyplot as plt
import equinox


def plot_circles(ax, centers, radii):

    for center, radius in zip(centers, radii):
        circle = plt.Circle(center, radius, fill=False)
        ax.add_artist(circle)
    ax.set_xlim((centers[:, 0] - radii).min() - 1, (centers[:, 0] + radii).max() + 1)
    ax.set_ylim((centers[:, 1] - radii).min() - 1, (centers[:, 1] + radii).max() + 1)
    # ax.set_aspect('equal', 'box')

def plot_halfspace(ax, normal, offset, xlim, ylim):
    """
    Plots a halfspace on a given axis.

    Args:
        ax: The axis to plot on.
        normal: The normal vector of the halfspace.
        offset: The offset of the halfspace.
        xlim: The x-axis limits for the plot.
        ylim: The y-axis limits for the plot.
    """
    x = jnp.linspace(xlim[0], xlim[1], 100)
    y = jnp.linspace(ylim[0], ylim[1], 100)
    X, Y = jnp.meshgrid(x, y)
    Z = normal[0] * X + normal[1] * Y - offset

    ax.contourf(X, Y, Z, levels=[0, jnp.inf], colors=['red'], alpha=0.2)

def expand_to_include_slack(n_slack, matrix):
    n_rows = matrix.shape[0]
    return jnp.concatenate([matrix, jnp.zeros([n_rows, n_slack])], axis=1)


@equinox.filter_jit
def extract_solution(solution, problem):
    plan_horizon = problem.params.planning_horizon
    state_dim = problem.params.dynamics.state_dim
    control_dim = problem.params.dynamics.control_dim
    z_dim = problem.z_dim
    slack_dim = len(solution) - z_dim

    stacked_xu = jax.lax.dynamic_slice(solution, (0,), ((plan_horizon+1)*state_dim + plan_horizon*control_dim,))
    xs = jax.lax.reshape(jax.lax.dynamic_slice(stacked_xu, (0,), ((plan_horizon+1)*state_dim,)), (plan_horizon+1, state_dim))
    us = jax.lax.reshape(jax.lax.dynamic_slice(stacked_xu, ((plan_horizon+1)*state_dim,), (plan_horizon*control_dim,)), (plan_horizon, control_dim))
    slack = jax.lax.dynamic_slice(solution, ((plan_horizon+1)*state_dim + plan_horizon*control_dim,), (slack_dim,))

    return xs, us, slack






# def extract_solution(solution, problem):
#     plan_horizon = problem.params.planning_horizon
#     state_dim = problem.params.dynamics.state_dim
#     control_dim = problem.params.dynamics.control_dim

#     stacked_xu = solution[:-problem.n_slack]
#     xs = stacked_xu[: (plan_horizon + 1) * state_dim].reshape(
#         (plan_horizon + 1, state_dim)
#     )
#     us = stacked_xu[(plan_horizon + 1) * state_dim :].reshape(
#         (plan_horizon, control_dim)
#     )
#     slack = solution[-problem.n_slack:]
#     return xs, us, slack