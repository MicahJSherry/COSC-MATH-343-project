




import numpy as np 
import matplotlib.pyplot as plt 
def GaussianQuadrature(f,a,b): 
        """ a quadrature routine that was defined on [-1,1]
            works by linearly mapping points on [a,b] to [-1,1]"""
        w = [0.347854845137454,   0.652145154862546, 
            0.652145154862546, 0.347854845137454]
   
        x = [-0.861136311594053, -0.339981043584856, 
            0.339981043584856, 0.861136311594053]
        slope = (b-a)/2 
        def map(x):
            # derived from the point-slope form of a line
            return slope * (x+1) + a
        area = 0
        for i in range(len(w)):
            area += slope*w[i] * f(map(x[i]))
        return area

def integrate(f,A,B, numInt=10):
    """ 
    a quadrature routine that breaking the interval of [A,B]
    into many subintervals then uses gausian quadrature on all the subintervals
    """
    
    if (numInt<1): 
        raise ValueError("Cannot have a number of intervals less than 1")
    
    x_points= np.linspace(A,B,numInt+1)
    #print(x_points)
    area = 0
    for i in range(len(x_points)-1):
        area += GaussianQuadrature(f,x_points[i],x_points[i+1])
    return area