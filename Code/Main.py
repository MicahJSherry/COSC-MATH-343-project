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

tpts = [0, 1, 2, 3, 4]
fpts = [0, 2, 4, 6, 8]
test_spline = spline(tpts,fpts)
xpts = np.linspace(tpts[0],tpts[-1])
ypts = []

for x in xpts:
    ypts.append(test_spline.spline(x))
plt.plot(tpts,fpts,"*")
plt.plot(xpts,ypts,"k")
plt.show()
def f1(x):
    return test_spline.spline(x)
function_Circleizer(f1)



V3 = integrate(function_Circleizer(f1),tpts[0],tpts[-1], 10)
print("V3 =",V3, type(V3))



