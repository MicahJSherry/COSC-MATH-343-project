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


xpts = [1, 2, 3, 4]
fpts = [0, 3, 7, 8]
coefs = get_spline_coef(xpts,fpts)
print(spline(1, coefs ,xpts))

print(type(function_Circleizer(f)))

V2 = integrate(function_Circleizer(f),0,1, 9)
V1 = integrate(function_Circleizer(g),0,1, 9) 
print(V2-V1)

