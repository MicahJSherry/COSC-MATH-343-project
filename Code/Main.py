from Quadrature import *
from spline import *
from visualize import *
from numpy import pi

def function_Circleizer(f):
    """ Given a funtion return a new Function that will calculate the Area of a circle with radius f(x) 
    """
    def C(x):
        return np.pi * f(x)**2
    return C

def sample(f,x0, xn, numPoints):
    """ returns 2 lists of x points and y points sampled from a given function """
    xpts = np.linspace(x0,xn, numPoints)
    ypts = f(xpts)
    
    return xpts, ypts

def foo(f1,x0, xn, numPoints, numinterval, f2=None):

    if f2 == None:
        tpts, fpts = sample(f1, x0, xn, numPoints)
        #print(tpts,fpts)
        s = spline(tpts,fpts)

        V = integrate(function_Circleizer(s.spline), tpts[0], tpts[-1], numinterval)
        plot_interpolation(s)
        plot_surfaces(s,num_pts = 100, make_gif=True)
        return V
    else:
        tpts, f1pts = sample(f1, x0, xn, numPoints)
        tpts, f2pts = sample(f2, x0, xn, numPoints)
        #print(tpts,fpts)
        s1 = spline(tpts,f1pts)
        s2 = spline(tpts,f2pts)

        V1 = integrate(function_Circleizer(s1.spline), tpts[0], tpts[-1], numinterval)
        V2 = integrate(function_Circleizer(s2.spline), tpts[0], tpts[-1], numinterval)
        plot_interpolation(spline1=s1,spline2=s2)

        plot_surfaces(spline1=s1,spline2=s2,num_pts = 100, make_gif=True)
        return V1 - V2 

"""Example 1 true vol 9*np.pi**2"""
def f1(x):
    return np.sin(x) + 2 

x, y =  sample(f1, 0, 8*pi, 100)

s = spline(x,y)
#print(foo(f1,0, 2*np.pi, 10, 10))
areas  = grid_refinement(function_Circleizer(s.spline), 0, 8*pi, max_iters=5)
errors = calc_errors(areas, 36*pi**2) 
alphas = calc_alphas(errors, 2)
print(alphas)

"""Example 2
def g1(x):
    return 1/(x)
def g2(x):
    return 1/(x+2)
print(foo(g1,1, 10, 30, 10, f2 =g2))
"""