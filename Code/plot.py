# Visualizing the 3D solid of revolution
# obtained by rotating the region bounded by two functions in a specific interval on the x-axis
# around some vertical/horizontal line
# see https://www.youtube.com/watch?v=hYVAHFKIOLk for what visualization should (ideally) look like
# see https://www.youtube.com/watch?v=ydyXf01WNYA for explanation of washer method and theory
# see https://www.youtube.com/watch?v=PI4C5CQkBiQ for how to (using circles) map a 2D graph to a 3D space
# see https://en.wikiversity.org/wiki/Cubic_Spline_Interpolation for a brief explanation of cubic spline interpolation

"""
The project:
    1.  user picks n points representing 2 functions (f1, f2) in xy plane
    2.  cubic splines are used to approximate f1 and f2
    3.  user chooses an interval [a,b] where f1 is always above f2
    4.  n-point composite gaussian quadrature is used to approximate
        the washer method, which is just a definite integral of the volume of a thin circular washer
    5.  the cubic spline functions for the n points of f1 and f2 are plotted in a 3D space
        to give us a visual of the surfaces of revolution (the space between them is naturally the solid of revolution)
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

def f1(x):
    return (0.5*x)+1

def f2(x):
    return 0.5*np.sqrt(x)

def test1(f1, f2, a, b, num_pts=50):
    """
    We take in 2 non-piecewise functions, f1 and f2
    f1 must still be above f2 for some interval of interest

    For this test, our goal is just to plot the surfaces of revolution
    of the aforementioned non-piecewise functions from [a,b]
    rotating about the x axis
    """
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    
    # defining our interval of interest (boundary region)
    lower_lim, upper_lim = a, b

    u = np.linspace(lower_lim, upper_lim, num=num_pts)
    v = np.linspace(0, 2*np.pi, num_pts)
    U, V = np.meshgrid(u, v)

    X = U
    
    Y1 = f1(U)*np.cos(V)
    Z1 = f1(U)*np.sin(V)

    Y2 = f2(U)*np.cos(V)
    Z2 = f2(U)*np.sin(V)

    ax.plot_surface(X, Y1, Z1, alpha=0.3, color='red', label="f1 surface")
    ax.plot_surface(X, Y2, Z2, alpha=0.6, color='blue', label="f2 surface")
    ax.set_xlabel('Y')
    ax.set_ylabel('X')
    ax.set_zlabel('Z')

    plt.legend()
    plt.show()

def test2(f1, f2, a, b, num_pts=50):
    """
    We take in 2 non-piecewise functions, f1 and f2
    f1 must still be above f2 for some interval of interest

    For this test, our goal is just to plot the surfaces of revolution
    of the aforementioned non-piecewise functions from [a,b]
    rotating about the y axis
    """
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    
    # defining our interval of interest (boundary region); a, b
    lower_lim, upper_lim = a, b

    v = np.linspace(lower_lim, upper_lim, num=num_pts)
    u = np.linspace(0, 2*np.pi, num_pts)
    V, U = np.meshgrid(v, u)

    Y1 = f1(V) * np.cos(U)
    X1 = f1(V) * np.sin(U)
    Z1 = f1(V)

    Y2 = f2(V) * np.cos(U)
    X2 = f2(V) * np.sin(U)
    Z2 = f2(V)

    ax.plot_surface(X1, Y1, Z1, alpha=0.3, color='red', label="f1 surface")
    ax.plot_surface(X2, Y2, Z2, alpha=0.6, color='blue', label="f2 surface")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.legend()
    plt.show()

def test3(f1, f2, a, b, num_pts=50):
    """
    We take in 2 non-piecewise functions, f1 and f2
    f1 must still be above f2 for some interval of interest

    For this test, our goal is to plot the surfaces of revolution
    of the aforementioned non-piecewise functions from [a,b]
    rotating about the x axis, as well as a visualization of the washer
    """
    
    def plot_washer(x, v, ax, f1):
        y_outer = f1(x) * np.cos(v)
        z_outer = f1(x) * np.sin(v)
        
        ax.plot(x * np.ones_like(v), y_outer, z_outer, color='green', label="Washer")
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    
    # defining our interval of interest (boundary region); a, b
    lower_lim, upper_lim = a, b

    u = np.linspace(lower_lim, upper_lim, num=num_pts)
    v = np.linspace(0, 2*np.pi, num_pts)
    U, V = np.meshgrid(u, v)

    X = U
    
    Y1 = f1(U)*np.cos(V)
    Z1 = f1(U)*np.sin(V)

    Y2 = f2(U)*np.cos(V)
    Z2 = f2(U)*np.sin(V)

    ax.plot_surface(X, Y1, Z1, alpha=0.3, color='red', label="f1 surface")
    ax.plot_surface(X, Y2, Z2, alpha=0.6, color='blue', label="f2 surface")
    # plot the washer at the midpoint of the boundary region
    plot_washer((lower_lim+upper_lim)/2.0, v, ax, f1)
    ax.set_xlabel('Y')
    ax.set_ylabel('X')
    ax.set_zlabel('Z')

    plt.legend()
    plt.show()

def test4(f1, f2, a, b, num_pts=50):
    """
    Same as test2 (so rotation about the y axis)
    except we include a visualization of the disc
    in the 3D plot as well
    """
    pass

def f3(x):
    return 2*x

def f4(x):
    return -.75*x**3+(2.75*x)+1

def f5(x):
    return (.75*x**3)-(4.5*x**2)+(7.25*x)-.5

def test5(upper_fns: dict, lower_fns: dict, num_pts=50, upper_colors=list(mcolors.TABLEAU_COLORS.keys()), lower_colors=list(mcolors.BASE_COLORS.keys())):
    """
    We take in 2 dictionaries, where
    upper_fns maps a tuple representing its closed interval [a,b] to the function over that interval
    lower_fns is the same thing as upper_fns, except each of its functions
    should be below the functions in upper_fns

    For this test, our goal is just to plot the surfaces of revolution
    of the aforementioned piecewise functions from [a,b]
    rotating about the x axis
    """

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    v = np.linspace(0, 2*np.pi, num_pts)

    for i, (interval, fn) in enumerate(upper_fns.items(), start=1):
        lower_lim, upper_lim = interval[0], interval[1]
        u = np.linspace(lower_lim, upper_lim, num=num_pts)
        U, V = np.meshgrid(u, v)

        X = U
        
        Y1 = fn(U)*np.cos(V)
        Z1 = fn(U)*np.sin(V)

        ax.plot_surface(X, Y1, Z1, alpha=0.3, color=upper_colors[i])

    for i, (interval, fn) in enumerate(lower_fns.items(), start=1):
        lower_lim, upper_lim = interval[0], interval[1]
        u = np.linspace(lower_lim, upper_lim, num=num_pts)
        U, V = np.meshgrid(u, v)

        X = U
        
        Y1 = fn(U)*np.cos(V)
        Z1 = fn(U)*np.sin(V)

        ax.plot_surface(X, Y1, Z1, alpha=0.6, color=lower_colors[i])
    
    ax.set_xlabel('Y')
    ax.set_ylabel('X')
    ax.set_zlabel('Z')

    plt.show()

#test5({(0,1):f1, (1,2):f1, (2,3):f1, (3,4):f1}, {(0,1):f2, (1,2):f2, (2,3):f2, (3,4):f2})
#test5({(0,1):f4, (1,2):f5}, {})
test2(f1, f2, 0, 5)
