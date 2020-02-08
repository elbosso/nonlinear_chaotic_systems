from ipywidgets import interact, interactive, HBox, Layout,VBox

import numpy as np
from scipy import integrate

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

def solve_bouali(numberOfTrajectories=10, anglex=0.0, angley=30.0, max_time=14.0, alpha=3.0, beta=2.2, gamma=1.0,mu=0.001):

    fig = plt.figure(figsize=(8, 6), dpi=80)
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.axis('off')

    # prepare the axes limits
    ax.set_xlim((-15, 15))
    ax.set_ylim((-30, 30))
    ax.set_zlim((5, 55))
    
    def bouali_deriv(x_y_z, t0, alpha=alpha, beta=beta, gamma=gamma,mu=mu):
        """Compute the time-derivative of a Bouali system."""
        x, y, z = x_y_z
        return [alpha*x*(1-y)-beta*z,-gamma*y*(1-x*x),mu*x]

    # Choose random starting points, uniformly distributed from -15 to 15
    np.random.seed(1)
    x0 = -0.0 + 1.0 * np.random.random((numberOfTrajectories, 3))

    # Solve for the trajectories
    t = np.linspace(0, max_time, int(250*max_time))
    x_t = np.asarray([integrate.odeint(bouali_deriv, x0i, t)
                      for x0i in x0])
    
    # choose a different color for each trajectory
    colors = plt.cm.viridis(np.linspace(0, 1, numberOfTrajectories))

    mins={"x":[],"y":[],"z":[]}
    maxs={"x":[],"y":[],"z":[]}
    for i in range(len(x_t)):
        x, y, z = x_t[i,:,:].T
        mins["x"]+=[min(x)]
        maxs["x"]+=[max(x)]
        mins["y"]+=[min(y)]
        maxs["y"]+=[max(y)]
        mins["z"]+=[min(z)]
        maxs["z"]+=[max(z)]
    # prepare the axes limits
    ax.set_xlim((min(mins["x"]),max(maxs["x"])))
    ax.set_ylim((min(mins["y"]),max(maxs["y"])))
    ax.set_zlim((min(mins["z"]),max(maxs["z"])))

    for i in range(numberOfTrajectories):
        x, y, z = x_t[i,:,:].T
        lines = ax.plot(x, y, z, '-', c=colors[i])
        plt.setp(lines, linewidth=1)

    ax.view_init(angley, anglex)
    plt.show()

    return t, x_t