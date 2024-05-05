import numpy as np
import matplotlib.pyplot as plt 

class spline:
    def __init__(self,tpts ,ypts):
        if len(tpts) != len(ypts):
            raise ValueError("size of tpts array is not the same as ypts")
        self.tpts = tpts
        self.ypts = ypts
        self.A, self.b = self.create_spline_Matrix()
        self.coefs = np.linalg.solve(self.A,self.b)
    def create_spline_Matrix(self): 
        s = 4
        num_eq = (len(self.tpts)-1)*s 

        A = np.zeros(num_eq**2).reshape(num_eq,num_eq) # matrix to solve
   
        b = np.zeros(num_eq).reshape(num_eq,1)
        i = 0 # row index
        j = 0 # col index
        n = 0 # t   index
        
        while i < num_eq - 2:
            if i % s == 1:
                n += 1
            if i % s == 0 or i % s == 1 : # matches the the values a point 
                A[i,j] = 1; A[i,j+1] = self.tpts[n]; A[i,j+2] = self.tpts[n]**2; A[i,j+3] = self.tpts[n]**3 
                b[i] = self.ypts[n]
            if i % s == 2: # matches at the first derivitive. D(1+ t + t**2 + t**3) -> 1 + 2*t +3*t**2 
                A[i,j+1] = 1; A[i,j+2] = 2*self.tpts[n]; A[i,j+3] = 3*self.tpts[n]**2
                A[i,j+s+1] = -1; A[i,j+s+2] = -2*self.tpts[n]; A[i,j+s+3] = -3*self.tpts[n]**2  
            if i % s == 3: # matches at the second derivtive. D(1 + 2*t +3*t**2) -> 2 + 6*t -> 1+ 3*t  
                A[i,j+2] = 1; A[i,j+3] = 3*self.tpts[n]
                A[i,j+s+2] = -1; A[i,j+s+3] = -3*self.tpts[n] 
        
            i += 1
            if i != 0 and i % s == 0: # increments j by the shift amount to simplify the index math
                j += s
        # the loop above will generate 2 equations  less than what we need 
        # so this will set the second derivitive = 0 at the endpoints so we can solve the system   
        A[-2,2] = 1; A[-2,3] = 3*self.tpts[0]
        A[-1,-2] = 1; A[-1,-1] = 3*self.tpts[-1]
        
        return A, b
    def spline(self, x):
        """
                | a_0 + b_0*x + c_0*x**2 + d_0*x**3   if x on [t_0, t_1) 
        S(x) =  | ...
                | a_n + b_n*x + c_n*x**2 + d_n*x**3   if x on [t_n-1, t_n]
        """
        s = 4 
        for i in range(len(self.tpts)-1):
            
            if(self.tpts[i]<= x <=self.tpts[i+1]):
                
                return (self.coefs[s*i, 0] + self.coefs[s*i+1, 0]*x+ self.coefs[s*i+2, 0]*x**2+ self.coefs[s*i+3, 0]*x**3)
        raise ValueError("the Spline is not defined for x =",x) 
            

        
        
