import numpy as np
import matplotlib.pyplot as plt
import imageio
import tempfile

def get_interpolated_points(spline, num_pts=50):
    tpts = np.linspace(spline.tpts[0], spline.tpts[-1], num=num_pts)
    ypts = []

    for t in tpts:
        ypts.append(spline.spline(t))

    return tpts, ypts

def plot_interpolation(spline1, spline2=None, num_pts=50):
    tpts_s1, ypts_s1 = get_interpolated_points(spline1, num_pts=num_pts)
    tpts_s2, ypts_s2 = None, None
    if spline2 is not None:
        tpts_s2, ypts_s2 = get_interpolated_points(spline2, num_pts=num_pts)

    plt.plot(tpts_s1, ypts_s1, ".", color="red", markersize=4, label="Interpolated Points (spline 1)")
    plt.plot(spline1.tpts, spline1.ypts, "o", color="green", markersize=7, label="Given Points (spline 1)")
    if spline2 is not None:
        plt.plot(tpts_s2, ypts_s2, ".", color="blue", markersize=4, label="Interpolated Points (spline 2)")
        plt.plot(spline2.tpts, spline2.ypts, "o", color="yellow", markersize=7, label="Given Points (spline 2)")

    plt.title("Cubic spline interpolation")
    plt.legend()
    plt.savefig("interpolation")

    plt.close()

def get_3d_points(spline, num_pts=50):
    a, b = spline.tpts[0], spline.tpts[-1]
    all_x = np.linspace(a, b, num=num_pts)
    all_theta = np.linspace(0, 2*np.pi, num=num_pts)

    # this gives us every possible combination of x and theta (rotation angles)
    # see https://stackoverflow.com/questions/36013063/what-is-the-purpose-of-meshgrid-in-numpy
    X, Theta = np.meshgrid(all_x, all_theta)
    # we can then use this to get every possible y and z value in our range of points
    Y, Z = [], []

    for i in range(len(X)):
        ypts, z_pts = [], []

        # array of floats
        x_pts = X[i]

        # array of floats
        thetas = Theta[i]

        for j in range(len(x_pts)):
            x = x_pts[j]
            theta = thetas[j]

            ypts.append(spline.spline(x)*np.cos(theta))
            z_pts.append(spline.spline(x)*np.sin(theta))

        Y.append(ypts)
        Z.append(z_pts)

    Y = np.array(Y)
    Z = np.array(Z)

    return X, Y, Z

def plot_surfaces(spline1, spline2=None, num_pts=50, incl_washer=True, make_gif=False, elevation_angle=20, rotation_degress=10, fps=10):
    X1, Y1, Z1 = get_3d_points(spline1, num_pts=num_pts)
    X2, Y2, Z2 = None, None, None
    if spline2 is not None:
        X2, Y2, Z2 = get_3d_points(spline2, num_pts=num_pts)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X1, Y1, Z1, alpha=0.3, color="red", label="Spline 1")
    if spline2 is not None:
        ax.plot_surface(X2, Y2, Z2, alpha=0.6, color="blue", label="Spline 2")

    if incl_washer:
        # we assume spline1 is the outer surface and spline2 the inner
        # and plot the washer just at its midpoint
        x = (spline1.tpts[0]+spline1.tpts[-1])/2.0
        all_thetas = np.linspace(0, 2*np.pi, num=num_pts)
        y_outer = spline1.spline(x)*np.cos(all_thetas)
        z_outer = spline1.spline(x)*np.sin(all_thetas)
        ax.plot(x*np.ones_like(all_thetas), y_outer, z_outer, alpha=0.85, color="green", label="Washer")

        if spline2 is not None:
            y_inner = spline2.spline(x)*np.cos(all_thetas)
            z_inner = spline2.spline(x)*np.sin(all_thetas)
            ax.plot(x*np.ones_like(all_thetas), y_inner, z_inner, alpha=0.85, color="green")
            for i in range(len(all_thetas)):
                ax.plot([x,x], [y_inner[i],y_outer[i]], [z_inner[i],z_outer[i]], alpha=0.85, color="green")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    plt.title("Surfaces of revolution")
    plt.legend()
    plt.savefig("surface")

    if make_gif:
        with tempfile.TemporaryDirectory() as temp_gif_frames:
            frames = []
            for angle in range(0, 360, rotation_degress):
                ax.view_init(elevation_angle, angle)
                filename = f"{temp_gif_frames}/frame_{angle}.png"
                plt.savefig(filename)
                frames.append(imageio.imread(filename))

            imageio.mimsave("surface_rotation.gif", frames, "GIF", fps=fps)

    plt.close()

def plot_errors(errors, x_scale="log", y_scale="linear"):
    subints = list(errors.keys())
    raw_errors = list(errors.values())

    plt.plot(subints, raw_errors, marker=".", color="red")
    for i in range(len(subints)):
        plt.text(subints[i]+.001, raw_errors[i]+.01, subints[i])
    plt.xscale(x_scale)
    plt.yscale(y_scale)
    plt.title("Errors over Subintervals")
    plt.savefig("error_plot")

    plt.close()


