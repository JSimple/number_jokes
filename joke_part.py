from numpy.polynomial import Polynomial as P
from random import *

class PolynomialJokePart:
    def __init__(self, points: list = [], prev_points: list = [], polynomial = None, rounding: int = 2) -> None:
        self.prev_points = [float(p)for p in prev_points]
        self.points = [float(p)for p in points]
        self.all_points = self.prev_points + self.points
        self.polynomial = polynomial
        self.type = 'polynomial'
    
    def clear_attributes(self):
        '''
        Sets all of the JokePart's attributes to empty.
        '''
        self.prev_points = []
        self.points = []
        self.all_points = []
        self.polynomial = P()
        
    def add_points(self, num_points: int = 0, points: list = [], rounding = 5):
        '''
        Append numbers to the JokePart's points attribute.\
        If a list of points is specified, the function will append that list.\
        Otherwise the function will append a specified number of points that follow the JokePart's polynomial attribute. 
        '''
        if points:
            num_points = len(points)
            float_points = [float(p)for p in points]
            self.points += float_points
            self.all_points += float_points
        elif num_points:
            all_points_len = len(self.all_points)
            for i in range(all_points_len, all_points_len + num_points):
                pt = round(self.polynomial(i), rounding)
                self.points.append(pt)
                self.all_points.append(pt)
        else:
            pass
    
    def fit_polynomial(self):
        '''
        Fits a polynomial function to the JokePart's points attribute.\
        Given n points, the polynomial function will have n terms.
        '''
        degree = len(self.all_points)-1
        x = [i for i in range(degree+1)]
        p = P.fit(x,self.all_points,degree,[])
        new_coefs = [round(c) for c in p.coef]
        p = P(new_coefs)
        self.polynomial = p


