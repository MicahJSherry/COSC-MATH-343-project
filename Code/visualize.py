import numpy as np
import matplotlib.pyplot as plt

def get_interpolated_points(spline, num_pts=50):
    t_pts = np.linspace(spline.t_pts[0], spline.t_pts[-1], num=num_pts)
    y_pts = []

    for t in t_pts:
        y_pts.append(spline.interpolate(t))

    return t_pts, y_pts

def plot_interpolation(spline1, spline2=None, num_pts=50):
    t_pts_s1, y_pts_s1 = get_interpolated_points(spline1, num_pts=num_pts)
    t_pts_s2, y_pts_s2 = None, None
    if spline2 is not None:
        t_pts_s2, y_pts_s2 = get_interpolated_points(spline2, num_pts=num_pts)

    plt.plot(t_pts_s1, y_pts_s1, ".", color="red", markersize=4, label="Interpolated Points (spline 1)")
    plt.plot(spline1.t_pts, spline1.y_pts, "o", color="green", markersize=7, label="Given Points (spline 1)")
    if spline2 is not None:
        plt.plot(t_pts_s2, y_pts_s2, ".", color="blue", markersize=4, label="Interpolated Points (spline 2)")
        plt.plot(spline2.t_pts, spline2.y_pts, "o", color="yellow", markersize=7, label="Given Points (spline 2)")

    plt.title("Cubic spline interpolation")
    plt.legend()
    plt.show()
    plt.savefig("interpolation")

def get_3d_points(spline, num_pts=50):
    a, b = spline.t_pts[0], spline.t_pts[-1]
    all_x = np.linspace(a, b, num=num_pts)
    all_theta = np.linspace(0, 2*np.pi, num=num_pts)

    # this gives us every possible combination of x and theta (rotation angles)
    # see https://stackoverflow.com/questions/36013063/what-is-the-purpose-of-meshgrid-in-numpy
    X, Theta = np.meshgrid(all_x, all_theta)
    # we can then use this to get every possible y and z value in our range of points
    Y, Z = [], []

    for i in range(len(X)):
        y_pts, z_pts = [], []

        # array of floats
        x_pts = X[i]

        # array of floats
        thetas = Theta[i]

        for j in range(len(x_pts)):
            x = x_pts[j]
            theta = thetas[j]

            y_pts.append(spline.interpolate(x)*np.cos(theta))
            z_pts.append(spline.interpolate(x)*np.sin(theta))

        Y.append(y_pts)
        Z.append(z_pts)

    Y = np.array(Y)
    Z = np.array(Z)

    return X, Y, Z

def plot_surfaces(spline1, spline2=None, num_pts=50):
    X1, Y1, Z1 = get_3d_points(spline1, num_pts=num_pts)
    X2, Y2, Z2 = None, None, None
    if spline2 is not None:
        X2, Y2, Z2 = get_3d_points(spline2, num_pts=num_pts)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X1, Y1, Z1, alpha=0.3, color="red", label="spline 1")
    if spline2 is not None:
        ax.plot_surface(X2, Y2, Z2, alpha=0.6, color="green", label="spline 2")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.title("Surfaces of revolution")
    plt.legend()

    plt.show()
    plt.savefig("surface")

