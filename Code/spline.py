import numpy as np
import matplotlib.pyplot as plt 

def get_spline_coef(t,y, return_matrix=False):
    """cubic spline method 
      
    the goal of this funtion is to generate the coeffecients for a peicewise defined funtion that will fit a given set of points 
    the funcion will be of the form:
          | a_0 + b_0*t + c_0*t**2 + d_0*t**3   if t on [t_0, t_1) 
    S(t) =| ...
          | a_n + b_n*t + c_n*t**2 + d_n*t**3   if t on [t_n-1, t_n]
    
    """
    s = 4 # number of equations per spline and the shift amount for the matrix equations 
    num_eq = (len(t)-1)*s #  
    
    A = np.zeros(num_eq**2).reshape(num_eq,num_eq) # matrix to solve
   
    b = np.zeros(num_eq).reshape(num_eq,1)
    i = 0 # row index
    j = 0 # col index
    n = 0 # t   index
    
    while i < num_eq - 2:
        if i % s == 1:
            n += 1
        if i % s == 0 or i % s == 1 : # matches the the values a point 
            A[i,j] = 1; A[i,j+1] = t[n]; A[i,j+2] = t[n]**2; A[i,j+3] = t[n]**3 
            b[i] = y[n]
        if i % s == 2: # matches at the first derivitive. D(1+ t + t**2 + t**3) -> 1 + 2*t +3*t**2 
            A[i,j+1] = 1; A[i,j+2] = 2*t[n]; A[i,j+3] = 3*t[n]**2
            A[i,j+s+1] = -1; A[i,j+s+2] = -2*t[n]; A[i,j+s+3] = -3*t[n]**2  
        if i % s == 3: # matches at the second derivtive. D(1 + 2*t +3*t**2) -> 2 + 6*t -> 1+ 3*t  
            A[i,j+2] = 1; A[i,j+3] = 3*t[n]
            A[i,j+s+2] = -1; A[i,j+s+3] = -3*t[n] 
    
        i += 1
        if i != 0 and i % s == 0: # increments j by the shift amount to simplify the index math
            j += s
    # the loop above will generate 2 equations  less than what we need 
    # so this will set the second derivitive = 0 at the endpoints so we can solve the system   
    A[-2,2] = 1; A[-2,3] = 3*t[0]
    A[-1,-2] = 1; A[-1,-1] = 3*t[-1]
    
    coefs = np.linalg.solve(A,b)
    if return_matrix:
        return coefs,A,b 
    return coefs

def spline(x, coefs, t):
    """
          | a_0 + b_0*x + c_0*x**2 + d_0*x**3   if x on [t_0, t_1) 
    S(x) =| ...
          | a_n + b_n*x + c_n*x**2 + d_n*x**3   if x on [t_n-1, t_n]
    """
    s = 4 
    for i in range(len(t)-1):
        if(t[i]<= x <=t[i+1]):
            return coefs[s*i] + coefs[s*i+1]*x+ coefs[s*i+2]*x**2+ coefs[s*i+3]*x**3
    return 0
        

