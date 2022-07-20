from math import factorial
import sympy as sym

x = sym.Symbol('i')

def TaylorPolynomial(model,degree):
    Derivatives = [model]
    for i in range(1,degree+1):
        Derivatives.append(sym.diff(Derivatives[-1]))

    polynomial = 0
    for i in range(degree+1):
        polynomial += (Derivatives[i].subs(x,0)/factorial(i))*(x**i)
    return polynomial

print('The 4th degree Taylor Polynomial for sin(x) is', TaylorPolynomial(sym.sin(x),4))
print('The 4th degree Taylor Polynomial for cos(x) is', TaylorPolynomial(sym.cos(x),4))
print('The 4th degree Taylor Polynomial for tan(x) is', TaylorPolynomial(sym.tan(x),4))
print('The 4th degree Taylor Polynomial for e^x is', TaylorPolynomial(sym.exp(x),4))
print('The 4th degree Taylor Polynomial for x**8 + 7*x**5 + 3*x**4 + x + 1 is', TaylorPolynomial(x**8 + 7*x**5 + 3*x**4 + x + 1,4))

print(''' Let's take a look at sin(x). ''')
print('The 7th degree Taylor Polynomial for sin(x) is', TaylorPolynomial(sym.sin(x),7))
print('They coincide over')