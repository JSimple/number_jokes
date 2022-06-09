# polynomial generator rule: rx^n + rx^n-1 ... rx^n-n
from scipy.optimize import curve_fit
from random import random
from time import sleep

class NumberJoke:
    def __init__(self):
        
        self.setup_polynomial, self.setup_polynomial_formatter = self.gen_polynomial_form(2)
        self.punchline_polynomial, self.punchline_polynomial_formatter = self.gen_polynomial_form(5)
       
        self.setup = self.joke_part()
        self.setup_pts = self.setup[0]
        self.setup_rule = self.setup[1]
       
        self.punchline = self.joke_part(punchline=True)
        self.punchline_pts = self.punchline[0]
        self.punchline_rule = self.punchline[1]
        
        self.joke = (self.setup_pts + ['...'] + self.punchline_pts, 'This joke is funny because first you think the numers follow this rule:\n' + self.setup_rule + '\nbut then the punchline reveals that they actually follow this rule:\n' + self.punchline_rule)
        self.rating = 'unrated'
    
    def gen_polynomial_form(self, terms = 2):
        
        def formatter(coefs):
            # error handling
            if terms != coefs:
                raise Exception('you need to have the same number of terms as coeficients')
            power = terms - 1
            format = f''
            while power > 0:
                if power == 0:
                    format += f'{coefs[power]}'
                elif power == 1:
                    format += f'+ {coefs[power]} * x'
                else:
                    format += f' + {coefs[power]} * x^{power}'
                power -= 1
            return format
        
        coef_var_names = ['coef_' + str(i) for i in range(terms)]

        def polyomial_form(x, *coef_var_names):
            power = terms - 1
            output =  0
            
            while power >= 0:
                output += coef_var_names[power] * x**power
            
            return output
        
        return polyomial_form, formatter
        
    # def gen_polynomial_form(self, terms = 2):
    #     if terms == 2:
    #         def formatter(coefs):
    #             return f'{coefs[0]} + {coefs[1]} * x'
    #         return (lambda x, a, b: a + b*x), formatter
    #     elif terms == 5:
    #         def formatter(coefs):
    #             return f'{coefs[0]} + {coefs[1]} * x + {coefs[2]} * x^2 + {coefs[3]} * x^3 + {coefs[4]} * x^4'
    #         return (lambda x, a, b, c, d, e: a + b*x + c*x**2 + d*x**3 + e*x**4), formatter
    #     else:
    #         print("this function is still hardcoded")
            
    def get_coef(self, pts, punchline = False):
        polynomial_fn = self.punchline_polynomial if punchline else self.setup_polynomial
        coefs = curve_fit(polynomial_fn, list(range(len(pts))), pts)[0]
        rounded = [round(coef, 2) for coef in coefs]
        return rounded
    
    # generates a list of random input points
    def gen_pts(self, len = 2):
        return [round(random()* 50, 0) for i in range(len)]
    
    # generates a setup or punchline
    def joke_part(self, punchline = False, length = 4):
        
        # define variables according to whether this is a set-up or punchline
        length = (length * 2) if punchline else length
        pts = self.setup_pts + self.gen_pts(len = 1) if punchline else self.gen_pts()
        coefs = self.get_coef(pts, punchline)
        polynomial_fn = self.punchline_polynomial if punchline else self.setup_polynomial
        formatter = self.punchline_polynomial_formatter if punchline else self.setup_polynomial_formatter
        
        # generate the rest of the points in our joke_part
        pts_len = len(pts)
        for x in range(pts_len,length):
            y = polynomial_fn(x, *coefs)
            pts.append(y)
            
        # generate the string formatted rule for our setup
        rule = formatter(coefs)
        return_pts = pts[pts_len:] if punchline else pts
        return return_pts,rule

        #change so that punchline just gives us the punchline pts alone
    
    def tell_joke(self, suspense = 1):
        for n in self.setup_pts:
            sleep(2 * suspense)
            print('\n' + str(n))
        sleep(2 * suspense)
        print('\n...')
        sleep(1.5 * suspense)
        for n in self.punchline_pts:
            sleep(suspense)
            print('\n' + str(n))
        sleep(0.5 * suspense)
        print('\n !! :-)')
        sleep(4 * suspense)
        print('\nThis joke was funny because first you thought the numers followed this rule:')
        sleep(1.5 * suspense)     
        print('\n y = ' + self.setup_rule)
        sleep(2.5 * suspense)
        print('\nbut then the punchline revealed that they actually follow this rule:')
        sleep(1.5 * suspense)     
        print('\n y = ' + self.punchline_rule)
        sleep(3 * suspense)
        rating = input('\nHow would you rate this joke on a scale of 1 (bad) to 10 (joke of the month)?\n')
        self.rating = rating
        print('\nThanks for your input!')
        
    
        
            

## write a gen punchline fn
## un-hard code things one by one            
    
    
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
