import numpy as np
import scipy


# ## Linear System Analytical Solvers

##########################################################################
"""
LU Decomposition

This function will decompose a square matrix into LU Decomposition with the
upper and lower matrices in place of the A matrix.

Required parameters
A - square matrix to decompose

Optional Parameters
None

Return
A - Matrix A that has been decomposed

"""
def lufact(A):
    n = len(A)
    L = np.eye(n)
    
    # Forward elimination
    for k in range(0,n-1):
        for i in range(k+1,n):
            fact = A[i,k] / A[k,k]
            A[i,k] = fact
            for j in range(k+1,n):
                A[i,j] = A[i,j] - fact * A[k,j]
    
    return A

##########################################################################




##########################################################################
"""
LU Solver

This function will take an LU decomposed matrix and a solution vector and
find the answer vector

Required parameters
LU - LU decomposed matrix
b  - solution vector

Optional Parameters
None

Return
x - Answer array

"""
def solveLU(LU,b):
    n = len(LU)
    x = np.zeros(n)
    y = np.zeros(n)
    
    # Forward elimination
    for i in range(n):
        y[i] = b[i]
        for j in range(i):
            y[i] -= LU[i,j] * y[j]
    
    # Back substitution
    x[n-1] = y[n-1] / LU[n-1,n-1]
    for i in range(n-1,-1,-1):
        x[i] = y[i]
        for j in range(i+1,n):
            x[i] = x[i] - LU[i,j] * x[j]
        x[i] = x[i] / LU[i,i]
        
    return x

##########################################################################




##########################################################################
"""
LU Decomposition with Pivoting

This function will decompose a square matrix into LU Decomposition with the
upper and lower matrices in place of the A matrix. This algorithm includes
pivoting.

Required parameters
A - square matrix to decompose

Optional Parameters
None

Return
A  - Matrix A that has been decomposed
rI - Scaled pivot array

"""
def lufact_piv(A):
    n = len(A)
    L = np.eye(n)
    rI = np.arange(0,n)
    
    # Forward elimination
    for k in range(0,n-1):
        
        max_elem_of_each_row = np.amax(np.abs(A[rI[k:],k:]),1) # scale by these
        possible_pivots = A[rI[k:],k] / max_elem_of_each_row   # scaled pivots (elements of cols in row k)
        kMax = np.argmax(np.abs(possible_pivots)) + k          # index of max scaled pivot: note the +k
        (rI[k], rI[kMax]) = (rI[kMax], rI[k])                  # swap the two rows: k with kMax
        
        for i in range(k+1,n):
            fact = A[rI[i],k] / A[rI[k],k]
            A[rI[i],k] = fact
            for j in range(k+1,n):
                A[rI[i],j] = A[rI[i],j] - fact * A[rI[k],j]
    
    return A, rI

##########################################################################


    


##########################################################################
"""
Thomas Algorithm

The function takes 4 parameters, vectors a, b, c, and d, in the following
form:

| a[0]  d[0]    0     0     0  |   | x[0] | = | b[0] |
| c[1]  a[1]  d[1]    0     0  |   | x[1] | = | b[1] |
|   0   c[2]  a[2]  d[2]    0  | * | x[2] | = | b[2] |
|   0     0   c[3]  a[3]  d[3] |   | x[3] | = | b[3] |
|   0     0     0   c[4]  a[4] |   | x[4] | = | b[4] |

Returns the x array with the appropriate solutions.

"""
def Thomas_Algorithm(c, a, d, b):
    n = len(a)
    
    # Elimination of the diagonal
    for i in range(1,n):
        a[i] = a[i] - (c[i-1] / a[i-1]) * d[i-1]
        b[i] = b[i] - (c[i-1] / a[i-1]) * b[i-1]
    
    # Back substitution
    x = np.zeros(n)
    x[-1] = b[-1] / a[-1]
    for i in range(n-2,-1,-1):
        x[i] = (b[i] - d[i] * x[i+1]) / a[i]
    
    return x

##########################################################################






###########################################################################################
"""
Jacobi Algorithm

A is a 2D matrix to be solved, size (n x n)
b is a 1D solution array length n.
x is a 1D guess array length n.
tol is the error tolerance at which the iterations will stop, default to 1e-5
maxit is the maximum number of iterations before our loop will exit with an error message.

Returns the solution array x and the number of iterations required.

"""
def Jacobi(A,b,x,tol=1e-5,maxit=10000):
    RE = np.zeros(maxit)
    for k in range(1,maxit+1):
        x_old = x.copy()
        R = b - np.dot(A,x_old)
        x = x + R / np.diag(A)
        RE[k-1] = np.linalg.norm(R) / np.linalg.norm(x)
        if RE[k-1] <= tol:
            return x, k, RE
    
    # print("Warning, reached {maxit} iterations without convergence to tolerance of {tol}")
    return x, k, RE

###########################################################################################





###########################################################################################
"""
Gauss-Seidel Algorithm

A is a 2D matrix to be solved, size (n x n)
b is a 1D solution array length n.
x is a 1D guess array length n.
tol is the error tolerance at which the iterations will stop, default to 1e-5
maxit is the maximum number of iterations before our loop will exit with an error message.

Returns the solution array x and the number of iterations required.

"""
def Gauss_Seidel(A,b,x,tol=1e-5,maxit=10000):
    n  = len(A)
    R  = np.zeros(n)
    RE = np.zeros(maxit)
    
    for k in range(1,maxit+1):
        for i in range(0,n):
            dot_sum = 0
            for j in range(0,n):
                dot_sum += A[i,j] * x[j]
            R[i] = b[i] - dot_sum
            x[i] = x[i] + R[i] / A[i,i]
        RE[k-1] = np.linalg.norm(R) / np.linalg.norm(x)
        if RE[k-1] <= tol:
            return x, k, RE
            
    # print("Warning, reached {maxit} iterations without convergence to tolerance of {tol}")
    return x, k, RE

###########################################################################################






###########################################################################################
"""
Successive Over-Relaxation(SOR) Algorithm

A is a 2D matrix to be solved, size (n x n)
b is a 1D solution array length n.
x is a 1D guess array length n.
omega is the relaxation number.
tol is the error tolerance at which the iterations will stop, default to 1e-5
maxit is the maximum number of iterations before our loop will exit with an error message.

Returns the solution array x and the number of iterations required.

"""
def SOR(A,b,x,omega = 1.2,tol=1e-5,maxit=10000):
    n  = len(A)
    R  = np.zeros(n)
    RE = np.zeros(maxit)
    
    for k in range(1,maxit+1):
        for i in range(0,n):
            dot_sum = 0
            for j in range(0,n):
                dot_sum += A[i,j] * x[j]
            R[i] = b[i] - dot_sum
            x[i] = x[i] + omega * (R[i] / A[i,i])
        RE[k-1] = np.linalg.norm(R) / np.linalg.norm(x)
        if RE[k-1] <= tol:
            return x, k, RE
            
    # print("Warning, reached {maxit} iterations without convergence to tolerance of {tol}")
    return x, k, RE

###########################################################################################





###########################################################################################
"""
Linear Iterative Solver

This is an iterative solver that allows the user to specify which iterative numerical
method they wish to use to solve their linear system.
method - the method to use. Options are "Jacobi", "Gauss_Seidel", and "SOR". Defaults to Jacobi.
A is a 2D matrix to be solved, size (n x n)
b is a 1D solution array length n.
x is a 1D guess array length n.
omega is the relaxation number. (only for SOR)
tol is the error tolerance at which the iterations will stop, default to 1e-5
maxit is the maximum number of iterations before our loop will exit with an error message. Defaults to 10000.

"""
def Iterative(A,b,x,method = "Jacobi",omega = 1.2,tol = 1e-5, maxit = 10000):
    if (method == "Jacobi"):
        ans = Jacobi(A,b,x)
    elif (method == "Gauss_Seidel"):
        ans = Gauss_Seidel(A,b,x)
    elif (method == "SOR"):
        ans = SOR(A,b,x,omega)
    else:
        print("Valid method not selected. Assuming Jacobi")
        ans = Jacobi(A,b,x)
    return ans

###########################################################################################





##########################################################################
"""
Bisection Iterative Non-linear solver

This function will take a function and will apply the bisecting algorithm
to it until it finds convergence.

Required Parameters:
f - function that you wish to pass to be solved.
a - lower guess value
b - upper guess value
The upper and lower guess values must bracket the solution. If not, the solver
will request new guess values.

Optional Parameters:
tol - tolerance value for the distance from the solution. Default is 1e-5
maxit - maximum number of iterations. Default is 10000

Returns:
c - solution
i - number of iterations

"""
def Bisection(f,a,b,tol = 1e-5,maxit=10000):
    # Setting up initial error
    err = 0.
    
    # Finding the values of the guesses
    fa = f(a)
    fb = f(b)
    
    # Checking to see if we have a solution
    if (fa == 0.):
        return a, 0
    elif (fb == 0.):
        return b, 0
    
    # Checking to see if the guess values brace the function
    if ((fa > 0 and fb > 0) or (fa < 0 and fb < 0)):
        print("Initial a and b values do not brace the funciton. Try different guesses")
        print("Here are the guess values")
        return a, b
    
    for i in range(maxit):
        # Finding new guess c and evaluating function at c
        c  = (a + b) / 2
        fc = f(c)
    
        # Checking to see if c is solution
        if (fc == 0.):
            return c, i+1
    
        # Check sign of c compared to a and b
        if ((fa > 0. and fc < 0.) or (fa < 0. and fc > 0.)):
            b  = c
            fb = fc
        elif ((fb > 0. and fc < 0.) or (fb < 0. and fc > 0.)):
            a  = c
            fa = fc
        
        # Checking if we are within the tolerance
        if ((np.abs(a - b) < tol) or (np.abs(fc) < tol)):
            return c, i+1
    
    print("Did not converge before",maxit,"iterations")
    return c, maxit

##########################################################################





##########################################################################
"""
Regula Falsi Iterative Non-linear solver

This function will take a function and will apply the Regula-Falsi algorithm
to it until it finds convergence.

Required Parameters:
f - function that you wish to pass to be solved.
a - lower guess value
b - upper guess value
The upper and lower guess values must bracket the solution. If not, the solver
will request new guess values.

Optional Parameters:
tol - tolerance value for the distance from the solution. Default is 1e-5
maxit - maximum number of iterations. Default is 10000

Returns:
c - solution
i - number of iterations

"""
def Regula_Falsi(f,a,b,tol = 1e-5,maxit=10000):
    # Setting up initial error
    err = 0.
    
    # Finding the values of the guesses
    fa = f(a)
    fb = f(b)
    
    # Checking to see if we have a solution
    if (fa == 0.):
        return a, 0
    elif (fb == 0.):
        return b, 0
    
    # Checking to see if the guess values brace the function
    if ((fa > 0 and fb > 0) or (fa < 0 and fb < 0)):
        print("Initial a and b values do not brace the funciton. Try different guesses")
        print("Here are the guess values")
        return a, b
    
    for i in range(maxit):
        # Finding fa and fb
        fa = f(a)
        fb = f(b)
        
        # Finding new guess c and evaluating function at c
        c  = a - fa * ((b - a)/(fb - fa))
        fc = f(c)
    
        # Checking to see if c is solution
        if (fc == 0.):
            return c, i+1
    
        # Check sign of c compared to a and b
        if ((fa > 0. and fc < 0.) or (fa < 0. and fc > 0.)):
            b  = c
            fb = fc
        elif ((fb > 0. and fc < 0.) or (fb < 0. and fc > 0.)):
            a  = c
            fa = fc
        
        # Checking if we are within the tolerance
        if ((np.abs(a - b) < tol) or (np.abs(fc) < tol)):
            return c, i+1
    
    print("Did not converge before",maxit,"iterations")
    return c, maxit

##########################################################################






##########################################################################
"""
Fixed Point Iterative Non-linear solver

This function will take a function and will apply the Fixed-Point Iterative
solver algorithm to it until it finds convergence. The function to be solved
must be in the form x_new = g(x_old), and will only converge if the slope
of g is less than 1.

Required Parameters:
g - function that you wish to pass to be solved.
guess - initial guess value

Optional Parameters:
tol - tolerance value for the distance from the solution. Default is 1e-5
maxit - maximum number of iterations. Default is 10000

Returns:
x - solution
i - number of iterations

"""
def Fixed_Point(g, guess, tol = 1e-5, maxit=10000):
    x_old = guess
    
    for i in range(maxit + 1):
        x_new = g(x_old)
        err = abs((x_new - x_old) / x_old)
        if (abs(x_new - x_old) < tol):
            return x, i+1
        x_old = x_new
    
    print("Did not converge before",maxit,"iterations.")
    return x_new, maxit

##########################################################################






##########################################################################
"""
Secant Method Iterative Non-linear solver

This function will take a function and will apply the Secant Method algorithm
to it until it finds convergence.

Required Parameters:
f - function that you wish to pass to be solved.
a - lower guess value
b - upper guess value

Optional Parameters:
tol - tolerance value for the distance from the solution. Default is 1e-5
maxit - maximum number of iterations. Default is 10000

Returns:
c - solution
i - number of iterations

"""
def Secant(f,a,b,tol = 1e-5,maxit=10000):
    # Setting up initial error
    err = 0.
    
    # Finding the values of the guesses
    fa = f(a)
    fb = f(b)
    
    # Checking to see if we have a solution
    if (fa == 0.):
        return a, 0
    elif (fb == 0.):
        return b, 0
    
    # Iterating for solution    
    for i in range(maxit):
        # Finding fa and fb
        fa = f(a)
        fb = f(b)
        
        # Finding new guess c and evaluating function at c
        c  = a - fa * ((b - a)/(fb - fa))
        fc = f(c)
    
        # Checking to see if c is solution
        if (fc == 0.):
            return c, i+1
    
        # Replace old value with new value
        a = b
        b = c
        
        # Checking if we are within the tolerance
        if ((np.abs(a - b) < tol) or (np.abs(fc) < tol)):
            return c, i+1
    
    print("Did not converge before",maxit,"iterations")
    return c, maxit

##########################################################################






##########################################################################
"""
Newton's Method Iterative Non-linear solver

This function will take a function and will apply Newton's Method algorithm
until it finds convergence.

Required Parameters:
f     - Function that you wish to pass to be solved
guess - Initial guess value

Optional Parameters:
getJac - functon to call to get Jacobian. If no function passed, numerical
         method will be called
tol    - tolerance value for the distance from the solution. Default is 1e-12
maxit  - maximum number of iterations. Default is 1000

Returns:
x_new - Solution
i     - Number of iterations

"""
def Newton(f, guess, tol=1E-12, maxit=1000): 
    # Initialize x
    x = guess
    
    # Start iterating on the guess to get convergence
    for i in range(maxit):
        # Getting the f vector
        f_old = f(guess)
        
        # Get numerical derivative
        Δx = x * 1e-8
        df = (f(x + Δx) - f(x - Δx)) / abs(2 * Δx)
                
        # Compute the new x value
        x = guess - f_old / df
        
        # Evaluate the error
        err = np.linalg.norm(x - guess) / np.linalg.norm(x)
        if (err < tol):
            return x, i+1
        
        # Update the guess
        guess = x
        
    print(f"Did not converge before {maxit} iterations")
    return x, maxit

##########################################################################






##########################################################################
"""
Generic 1st Order ODE Solver IVP with Explicit Euler's Method

Required parameters:
dy - differential equation to be solved
y0 - initial value
t  - time array upon which to find points

Optional Parameters:
none

Return:
y - solution array with answer

"""
def Explicit_Euler(dy,y0,t):
    # Defining n
    n = len(t)
    
    # Creating the y array
    y    = np.zeros(n)
    y[0] = y0
    
    # Applying Explicit Euler Method
    for i in range(1,n):
        Δt = t[i] - t[i-1]
        y[i] = y[i-1] + Δt * dy(y[i-1],t[i-1])
    
    return y

##########################################################################






##########################################################################
"""
Generic 1st Order ODE Solver IVP with Implicit Euler's Method

Required parameters:
dy - differential equation to be solved
y0 - initial value
t  - time array upon which to find points

Optional Parameters:
none

Return:
y - solution array with answer

"""
def Implicit_Euler(dy,y0,t):
    # Defining n
    n = len(t)
    
    # Creating the y array
    y    = np.zeros(n)
    y[0] = y0
    
    # Defining the Implicit Euler function
    def Imp_Func(y_new):
        resid = y[i-1] + Δt * dy(y_new,t[i]) - y_new
        return resid
    
    # Calling Newton's Method to solve for each point
    for i in range(1,n):
        Δt = t[i] - t[i-1]
        y[i] = Newton(Imp_Func,y[i-1])[0]
    
    return y

##########################################################################






##########################################################################
"""
Generic 1st Order ODE Solver IVP with Modified Method

Required parameters:
dy - differential equation to be solved
y0 - initial value
t  - time array upon which to find points

Optional Parameters:
none

Return:
y - solution array with answer

"""
def Modified_Midpoint(dy,y0,t):
    # Defining n
    n = len(t)
    
    # Creating the y array
    y    = np.zeros(n)
    y[0] = y0
    
    # Applying Explicit Euler Method
    for i in range(1,n):
        # Use Explicit Euler's Method to take a half step
        Δt     = t[i] - t[i-1]
        y_half = y[i-1] + Δt / 2 * dy(y[i-1],t[i-1])
        t_half = (t[i] + t[i-1]) / 2
        
        # Take real full step using half step slope
        y[i] = y[i-1] + Δt * dy(y_half,t_half)
    
    return y

##########################################################################






##########################################################################
"""
Generic 1st Order ODE Solver with Runge Kutta Method

Required parameters:
dy - differential equation to be solved
y0 - initial value
t  - time array upon which to find points

Optional Parameters:
none

Return:
y - solution array with answer

"""
def Runge_Kutta(dy,y0,t):
    # Defining n
    n = len(t)
    
    # Creating the y array
    y      = np.zeros((len(t), len(y0)))
    y[0,:] = y0
    
    # Applying Explicit Euler Method
    for i in range(1,n):
        h    = t[i] - t[i-1]
        S1   = dy(y[i-1,:],             t[i-1])
        S2   = dy(y[i-1,:] + h / 2 * S1,t[i-1] + h / 2)
        S3   = dy(y[i-1,:] + h / 2 * S2,t[i-1] + h / 2)
        S4   = dy(y[i-1,:] + h     * S3,t[i-1] + h)
        y[i,:] = y[i-1,:] + h / 6 * (S1 + 2 * S2 + 2 * S3 + S4)
    
    return y

##########################################################################







##########################################################################
"""
Redlich-Kwong Equation of State

This function will solve for the Redlich-Kwong Equation of State. To learn
what the Redlich-Kwong Equation of State is, go to this website:
https://en.wikipedia.org/wiki/Redlich%E2%80%93Kwong_equation_of_state

Required Parameters
P_r - Reduced pressure of the system
T_r - Reduced temperature of the system

Optional Parameters
None

Returns
Z - compressibility factor

"""
def Redlich_Kwong(P_r,T_r):
    # RK Values
    σ   = 1
    ϵ   = 0
    Ω   = 0.08664
    Ψ   = 0.42748

    # Calculated values
    α = T_r ** -0.5
    β = Ω * P_r / T_r
    q = Ψ * α / (Ω * T_r)
    
    # Function to iterate to find Z value
    def findZ(Z):
        resid = 1 + β - q * β * (Z - β) / ((Z + ϵ * β) * (Z + σ * β)) - Z
        return resid
    
    # Iteratively solve for Z
    Z_guess = 1.0
    Z = Newton(findZ, Z_guess)[0]
    
    return Z

##########################################################################






##########################################################################
"""
Peng-Robinson Equation of State

This function will solve for the Peng-Robinson Equation of State. To learn
what the Peng-Robinson Equation of State is, go to this website:
https://en.wikipedia.org/wiki/Cubic_equations_of_state

Required Parameters
P_r - Reduced pressure of the system in 
T_r - Reduced temperature of the system
ω   - acentric factor

Optional Parameters
None

Returns
Z - compressibility factor

"""
def Peng_Robinson(P_r, T_r, ω, guess = 1.0):
    # RK Values
    σ   = 1 + 2 ** 0.5
    ϵ   = 1 - 2 ** 0.5
    Ω   = 0.07880
    Ψ   = 0.45724
    Z_c = 0.30740

    # Calculated values
    α = (1 + (0.37464 + 1.54226 * ω - 0.26992 * ω ** 2) * (1 - T_r ** 0.5)) ** 2
    β = Ω * P_r / T_r
    q = Ψ * α / (Ω * T_r)
    
    # Function to iterate to find Z value
    def findZ(Z):
        resid = 1 + β - q * β * (Z - β) / ((Z + ϵ * β) * (Z + σ * β)) - Z
        return resid
    
    # Iteratively solve for Z
    Z = Newton(findZ, guess)[0]
        
    return Z

##########################################################################






##########################################################################
"""
ΔH Ideal Gas Solver

This function will solve for the ΔH of a system given a change in
temperature.

Required Parameters
T_initial - Initial temperature in Kelvin
T_final   - Final temperature in Kelvin
CP_val    - Array of the [A,B,C,D] coefficients from Table C.1 in our
            thermodynamics textbook. Just the values, the function will
            handle the exponents on its own.

Optional Parameters
R - Universal Gas Constant. Default is 8.31447 J / mol * K

Returns
ΔH - ΔH value

"""
def ΔH_Ideal(T_initial, T_final, CP_val, R = 8.31447):    
    # Extracting values from array
    A = CP_val[0]
    B = CP_val[1] * 1e-3
    C = CP_val[2] * 1e-6
    D = CP_val[3] * 1e+5
    
    # Function for C_P
    def C_P(T):
        C_P = A + (B * T) + C * (T ** 2) + D * (T ** -2)
        return C_P

    # Integrating over the bounds to get a ΔH
    ΔH = R * scipy.integrate.quad(C_P,T_initial,T_final)[0]
    
    return ΔH

##########################################################################







##########################################################################
"""
ΔS Ideal Gas Solver

This function will solve for the ΔH of a system given a change in
temperature.

Required Parameters
T_initial - Initial temperature in Kelvin
T_final   - Final temperature in Kelvin
P_initial - Initial pressure. Units must be consistent with P_final
P_final   - Final pressure. Units must be consistent with P_initial
CP_val    - Array of the [A,B,C,D] coefficients from Table C.1 in our
            thermodynamics textbook. Just the values, the function will
            handle the exponents on its own.

Optional Parameters
R - Universal gas constant. Default parameter is 8.31447 J / mol * K

Returns
ΔS - ΔS value without being multiplied by R - you get to choose the units

"""
def ΔS_Ideal(T_initial, T_final, P_initial, P_final, CP_val, R = 8.31447):
    # Extracting values from array
    A = CP_val[0]
    B = CP_val[1] * 1e-3
    C = CP_val[2] * 1e-6
    D = CP_val[3] * 1e+5
    
    # Function for C_P
    def C_P(T):
        C_P = A / T + B + C * T + D * (T ** -3)
        return C_P

    # Integrating over the bounds to get a ΔS
    ΔS = R * (scipy.integrate.quad(C_P,T_initial,T_final)[0] - np.log(P_final / P_initial))
    
    return ΔS

##########################################################################







##########################################################################
"""
Generalized Compressibility-Factor Correlation for H_resid

This function will find the residual enthalpy at a certain state given the
input conditions.

Required parameters
T   - Temperature of interest
T_c - Critical temperature of species of interest
P   - Pressure of interest
P_c - Critical pressure of species of interest
ω   - Acentric factor of species of interest

Optional Parameters
R - Universal Gas Constant. Default value is 8.31447 J / mol * K

Return
H_resid - Residual enthapy

"""
def GCFC_H_resid(T, T_c, P, P_c, ω, R = 8.31447):
    # Reduced temperature and pressure
    T_r = T / T_c
    P_r = P / P_c
    
    # B values
    B_0  = 0.083 - 0.422 / (T_r ** 1.6)
    B_1  = 0.139 - 0.172 / (T_r ** 4.2)
    dB_0 =         0.675 / (T_r ** 2.6)
    dB_1 =         0.722 / (T_r ** 5.2)
    
    # H_resid
    H_resid = R * T_c * P_r * (B_0 - T_r * dB_0 + ω * (B_1 - T_r * dB_1))
    
    return H_resid

##########################################################################







##########################################################################
"""
Generalized Compressibility-Factor Correlation for S_resid

This function will find the residual entropy at a certain state given the
input conditions.

Required parameters
T   - Temperature of interest
T_c - Critical temperature of species of interest
P   - Pressure of interest
P_c - Critical pressure of species of interest
ω   - Acentric factor of species of interest

Optional Parameters
R - Universal Gas Constant. Default value is 8.31447 J / mol * K

Return
S_resid - Residual enthapy

"""
def GCFC_S_resid(T, T_c, P, P_c, ω, R = 8.31447):
    # Reduced temperature and pressure
    T_r = T / T_c
    P_r = P / P_c
    
    # B values
    dB_0 = 0.675 / (T_r ** 2.6)
    dB_1 = 0.722 / (T_r ** 5.2)
    
    # S_resid
    S_resid = -R * P_r * (dB_0 + ω * dB_1)
    
    return S_resid

##########################################################################





##########################################################################
"""
These are fugacity functions to find the fucacity coefficients of a system

"""
def Z_func(T, ρ, T_c, P_c, ω):
    R = 8.31447 # J/mol*K or m**3*Pa / mol*K
    
    # Reduce Temperature
    T_r = T / T_c
    
    # PR Values
    σ = 1 + (2 ** 0.5)
    ϵ = 1 - (2 ** 0.5)
    Ω = 0.07780
    Ψ = 0.45724
    
    # Calculated values
    α = (1 + (0.37464 + 1.54226 * ω - 0.26992 * (ω ** 2)) * (1 - T_r ** 0.5)) ** 2
    b = Ω * R * T_c / P_c
    q = Ψ * α / (Ω * T_r)
    
    Z = 1.0 / (1.0 - ρ * b) - q * ρ * b / ((1.0 + ϵ * ρ * b) * (1.0 + σ * ρ * b))
    
    return Z

##########################################################################
def ρ_func(T, P, T_c, P_c, ω, guess = 20.):
    R = 8.31447 # J/mol*K or m**3*Pa / mol*K
    
    # Function to solve for
    def find_ρ(ρ):
        resid = Z_func(T, ρ, T_c, P_c, ω) - P / (ρ * R * T)
        return resid
    
    ρ_guess = guess
    ρ = scipy.optimize.fsolve(find_ρ, ρ_guess)[0]
    
    return ρ # mol / m**3

##########################################################################
def Gibbs_Residual_RT(T, P, guess, T_c, P_c, ω):
    ρ_Gibbs = ρ_func(T, P, guess, T_c, P_c, ω)
    Z_Gibbs = Z_func(T, ρ_Gibbs, T_c, P_c, ω)
    
    # Integral term
    def integrate(ρ_integrate):
        integrand = (Z_func(T, ρ_integrate) - 1.0) / ρ_integrate
        return integrand
    
    Integral_term = scipy.integrate.quad(integrate, 0., ρ_Gibbs, limit = 1000)[0]
    
    # The rest
    Other_terms = Z_Gibbs - 1.0 - np.log(Z_Gibbs)
    
    # Everything
    Everything = Integral_term + Other_terms
    
    return Everything

##########################################################################
def ϕ_vapor_func(T, P, T_c, P_c, ω):
    R = 8.31447 # J/mol*K or m**3*Pa / mol*K
    
    vapor_guess = P / (R * T)
    Gibbs_Residual_vapor = Gibbs_Residual_RT(T, P, vapor_guess, T_c, P_c, ω)
    ϕ_val = np.exp(Gibbs_Residual_vapor)
    
    return ϕ_val

##########################################################################
def ϕ_liquid_func(T, P, T_c, P_c, ω):
    liquid_guess = 40000.
    Gibbs_Residual_liquid = Gibbs_Residual_RT(T, P, liquid_guess, T_c, P_c, ω)
    ϕ_val = np.exp(Gibbs_Residual_liquid)
    
    return ϕ_val

##########################################################################







##########################################################################
"""
Vapor Pressure

This function will solve for vapor pressure of a pure species in the
liquid phase using the DIPPR fit. The DIPPR fit equation is of the
following form:

Y = e**(A + B/T + C*ln(T) + D*(T**E))

Y returns the liquid vapor pressure in Pa

Required Parameters
T     - temperature in K
DIPPR - DIPPR coefficients for the pure component species

Optional Parameters
None

Returns
Y - liquid vapor pressure in Pa

"""
def P_sat_DIPPR(T, DIPPR):
    # Extracting the DIPPR coefficients
    A = DIPPR[0]
    B = DIPPR[1]
    C = DIPPR[2]
    D = DIPPR[3]
    E = DIPPR[4]
    F = DIPPR[5]
    G = DIPPR[6]
    
    # Solving the correlation
    Y = np.exp(A + B / T + C * np.log(T) + D * (T ** E))
    
    return Y

##########################################################################







##########################################################################
"""
Liquid Density

This function will solve for liquid density of a pure species in the
liquid phase using the DIPPR fit. The DIPPR fit equation is of the
following form:

Y = A / (B**(1 + (1 - T/C)**D))

Y returns the liquid density in kmol / m**3

Required Parameters
T     - temperature in K
DIPPR - DIPPR coefficients for the pure component species

Optional Parameters
None

Returns
Y - liquid density in kmol / m**3

"""
def liq_den_DIPPR(T, DIPPR):
    # Extracting the DIPPR coefficients
    A = DIPPR[0]
    B = DIPPR[1]
    C = DIPPR[2]
    D = DIPPR[3]
    E = DIPPR[4]
    F = DIPPR[5]
    G = DIPPR[6]
    
    # Solving the correlation
    Y = A / (B**(1 + (1 - T/C)**D))
    
    return Y

##########################################################################







##########################################################################
"""
Wilson Function

This function will solve for liquid activity coefficients for a two
component system.

Required Parameters
x_1 - liquid mole fraction
T   - temperature in K
Wilson_params - parameters for the Wilson correlation in an array
                [V_1, V_2, a_12, a_21]

Optional Parameters
None

Returns
γ_1 - activity coefficient for species 1
γ_2 - activity coefficient for species 2

"""
def Wilson_func(x_1, T, Wilson_params):
    R = 8.31447 # J/mol*K or m**3*Pa / mol*K
    
    # Extracting Wilson parameters
    V_1  = Wilson_params[0]
    V_2  = Wilson_params[1]
    a_12 = Wilson_params[2]
    a_21 = Wilson_params[3]
    
    # Defining x_2
    x_2 = 1.0 - x_1
    
    # Calculating Λ Values
    Λ_12 = V_2 / V_1 * np.exp(-a_12 / (R * T))
    Λ_21 = V_1 / V_2 * np.exp(-a_21 / (R * T))
    
    # Creating the right hand side
    rhs_1_pt_1 = -np.log(x_1 + x_2 * Λ_12)
    rhs_1_pt_2 = x_2 * (Λ_12 / (x_1 + x_2 * Λ_12) - Λ_21 / (x_1 * Λ_21 + x_2))
    rhs_1      = rhs_1_pt_1 + rhs_1_pt_2
    
    rhs_2_pt_1 = -np.log(x_2 + x_1 * Λ_21)
    rhs_2_pt_2 = x_1 * (Λ_21 / (x_2 + x_1 * Λ_21) - Λ_12 / (x_2 * Λ_12 + x_1))
    rhs_2      = rhs_2_pt_1 + rhs_2_pt_2
    
    # Finding our activity values
    γ_1 = np.exp(rhs_1)
    γ_2 = np.exp(rhs_2)
    
    return γ_1, γ_2

##########################################################################

