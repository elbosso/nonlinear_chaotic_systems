from ipywidgets import interact, interactive, HBox, Layout,VBox

import numpy as np
from scipy import integrate

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

def solve_bouali(numberOfTrajectories=10, min_x0=0.0, max_x0=1.0, anglex=0.0, angley=30.0, max_time=14.0, alpha=2.6, beta=0.005, a=4.0,b=1.0,c=1.5,s=1.5):

    fig = plt.figure(figsize=(8, 6), dpi=80)
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.axis('off')

    # prepare the axes limits
    ax.set_xlim((-5, 5))
    ax.set_ylim((-10, 10))
    ax.set_zlim((5, 25))
    
    def bouali_deriv(x_y_z, t0, alpha=alpha, beta=beta, a=a,b=b,c=c,s=s):
        """Compute the time-derivative of a Bouali system."""
        x, y, z = x_y_z
        return [x*(a-y)+alpha*z,-y*(b-x*x),-x*(c-s*z)-beta*z]

    # Choose random starting points, uniformly distributed from min_x0 to max_x0
    np.random.seed(1)
    span=max_x0-min_x0
    x0 = min_x0 + span * np.random.random((numberOfTrajectories, 3))

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