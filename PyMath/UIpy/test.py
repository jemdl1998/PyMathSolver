from sympy import Symbol
from scipy.optimize import fsolve,ridder, root_scalar
from math import log,exp,sin,cos,tan
def fun(V):
    x=V
    fx=1-x/(1-x)**2
    return fx
print(root_scalar(fun,x0=0))