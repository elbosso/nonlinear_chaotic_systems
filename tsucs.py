from ipywidgets import interact, interactive, HBox, Layout,VBox
import numpy as np
from scipy import integrate

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

def solve_tsucs(numberOfTrajectories=10, min_x0=-20.0, max_x0=20.0, anglex=0.0, angley=30.0, max_time=4.0,a=40.0,b=55.0,c=11.0/6.0,d=0.16,e=0.65,f=10):

    fig = plt.figure(figsize=(8, 6), dpi=80)
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.axis('off')

    # prepare the axes limits
    ax.set_xlim((-40, 40))
    ax.set_ylim((-60, 60))
    ax.set_zlim((-555, 55))
    
    def tsucs_deriv(x_y_z, t0, a=a,b=b,c=c,d=d, e=e,f=f):
        """Compute the time-derivative of a Sprott system M."""
        x, y, z = x_y_z
        return [a*(y-x)+d*x*z, b*x-x*z+f*y, -e*x*x+x*y+c*z]

    # Choose random starting points, uniformly distributed from min_x0 to max_x0
    np.random.seed(1)
    span=max_x0-min_x0
    x0 = min_x0 + span * np.random.random((numberOfTrajectories, 3))

    # Solve for the trajectories
    t = np.linspace(0, max_time, int(250*max_time))
    x_t = np.asarray([integrate.odeint(tsucs_deriv, x0i, t)
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