from Quadrature import integrate
from spline import *



def f(x):
    return 2
def g(x):
    return 1
def function_Circleizer(f):
    """ Given a funtion return a new Function that will calculate the Area of a circle with radius f(x) 
    """
    def C(x):
        return np.pi * f(x)**2
    return C


tpts = [1, 2, 3, 4]
fpts = [0, 3, 7, 8]
coefs = get_spline_coef(tpts,fpts)

xpts = np.linspace(tpts[0],tpts[-1])
ypts = []
for x in xpts:
    ypts.append(spline(x,coefs, tpts))
plt.plot(tpts,fpts, "*")
plt.plot(xpts,ypts, "k")
plt.show()

def f1(x):
    return spline(x,coefs, tpts)
function_Circleizer(f1)

V3 = integrate(function_Circleizer(f1),0,4, 9)
print(V3)

V2 = integrate(function_Circleizer(f),0,1, 9)
V1 = integrate(function_Circleizer(g),0,1, 9) 
print(V2-V1)

