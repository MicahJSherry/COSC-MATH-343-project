from Quadrature import integrate
from spline import *

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

def f(x):
    return np.sin(x) +2



tpts, fpts = sample(f,0,np.pi * 2,5)

s = spline(tpts,fpts)

xpts = np.linspace(0,2*np.pi)
ypts = []
for x in xpts:
    ypts.append(s.spline(x))

plt.plot(xpts,ypts)
plt.show()


V3 = integrate(function_Circleizer(s.spline),xpts[0],xpts[-1], 10)
print("V3 =",V3, type(V3))



