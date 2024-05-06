import numpy as np 

def gaussian_quadrature(f, a, b): 
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

        area = 0.0
        for i in range(len(w)):
            area += slope*w[i] * f(map(x[i]))

        return area

def integrate(f, a, b, num_subints=10):
    """ 
    performs 4-point composite Gaussian Quadrature by
    breaking the given interval [a,b] into num_subints subintervals
    and returning the sum of the 4-point quadrature routine on each subinterval
    """
    
    if (num_subints < 1): 
        raise ValueError("Cannot have a number of subintervals less than 1")
    
    x_pts = np.linspace(a, b, num_subints+1)
    
    area = 0.0
    for i in range(len(x_pts)-1):
        area += gaussian_quadrature(f, x_pts[i], x_pts[i+1])
    
    return area


def grid_refinement(f, a, b, refinement_factor=2, max_iters=5):
    areas = {} 

    for i in range(max_iters):
        num_subints = refinement_factor**i
        areas[num_subints] = integrate(f, a, b, num_subints=num_subints)
        print(num_subints)
    return areas

def calc_errors(areas, true_integral):
    errors = {} 

    for subints, area in areas.items():
        errors[subints] = np.abs(true_integral-area)

    return errors

def calc_alphas(errors, refinement_factor):
    alphas = []

    raw_errors = list(errors.values())
    
    for i in range(len(raw_errors)-1):

        alphas.append(np.log(raw_errors[i]/raw_errors[i+1])/np.log(refinement_factor))

    return alphas
