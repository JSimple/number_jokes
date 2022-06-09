# polynomial generator rule: rx^n + rx^n-1 ... rx^n-n
# figure out again how scipy fit line works
from scipy.optimize import curve_fit
from random import random
#res = curve_fit(lambda x, a, b, c, d, e: a*x**4 + b*x**3 + c*x**2 + d*x + e, list(range(5)), [4, 6, 8, 10, 13])

# num1 = round(random()* 10, 0) 
# num2 = round(random()* 10, 0)  + 10
# print(num1, num2)
# coefs = curve_fit(lambda x, a, b: a + b*x, list(range(2)), [num1, num2])

# print(coefs)

class NumberJoke:
    def __init__(self):
        self.setup_polynomial, self.setup_polynomial_formatter = self.gen_polynomial()
        self.setup_pts = self.gen_setup()[0]
        self.setup_rule = self.gen_setup()[1]
        self.punchline_polynomial, self.setup_polynomial_formatter = self.gen_punchline_polynomial()
        
    def gen_polynomial(self, terms = 2):
        def formatter(coefs):
            return f'{coefs[0]} + {coefs[1]} * x'
        return (lambda x, a, b: a + b*x), formatter
    def gen_punchline_polynomial(self, terms = 5):
        def formatter(coefs):
            return f'{coefs[0]} + {coefs[1]} * x + {coefs[2]} * x^2 + {coefs[3]} * x^3 + {coefs[4]} * x^4'
        return (lambda x, a, b, c, d, e: a + b*x + c*x**2 + d*x**3 + e*x**4), formatter
    def setup_coef(self, pts):
        coefs = curve_fit(self.setup_polynomial, list(range(len(pts))), pts)[0]
        rounded = [round(coef, 2) for coef in coefs]
        return rounded
    def gen_setup(self, length = 4):
        pts = [2,4]
        setup_pts = pts[:]
        coefs = self.setup_coef(pts)
        # generate the rest of the points in our setup
        for x in range(len(pts),length):
            y = self.setup_polynomial(x, *coefs)
            setup_pts.append(y)
        # generate the string formatted rule for our setup
        rule = self.setup_polynomial_formatter(coefs)
        return setup_pts,rule
    ## write a gen punchline fn
        
            

            
    
    
# 2, 4, 6, 8 ... 100, 150
        
# a + b*x
# coef1 + coef2*x
# where x is len(setup_pts + n)

# set up rule: y = a*x + b
# set up: [y1, y2, y3, y4 ...]
# punchline rule: y = ax^4 + bx^3 + cx^2 + dx + e


# **generate set up**
# randomize 2 y values
# fit a linear ploynomial to that (use scipy function)
# find 2 more points on that line
# we'll have 4 pts in our series (that's the set up)
# **Generate punchline**
# generate one more random y value
# pass all 5 of our y values to that scipy fit function
# then we get a quartic polynomial rule
# then we can find however many more points we want to use in our punchline


# first fit a linear polynomial to 2 points, 
# then find the point at x = 3 and x = 4, 
# then generate a random point at x = 5
# then fit a quintic to those 5 points
# write a polynomial to string function
# write a visualization for the joke using mat plot lib


# create a JokePart class
# has a function
# a string representation of the function
# a series of y values where x = 1, 2 ... depending on complexity of function (linear, quadratic, etc.)
