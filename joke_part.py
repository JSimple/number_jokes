from numpy.polynomial import Polynomial as P
from random import *
import json

class PolynomialEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, P):
            return(list(obj.coef))
        return super().default(obj)

class PolynomialJokePart:
    def __init__(self, points: list = [], prev_points: list = [], polynomial = None) -> None:
        self.prev_points = [float(p)for p in prev_points]
        self.points = [float(p)for p in points]
        self.polynomial = polynomial
        self.type = 'polynomial'
    
    def json(self):
        return json.dumps(self.__dict__, cls=PolynomialEncoder)
    
    def clear_attributes(self):
        '''
        Sets all of the JokePart's attributes to empty.
        '''
        self.prev_points = []
        self.points = []
        self.polynomial = P()
    
    def add_points(self, num_points: int = 0):
        '''Generate and append to JokePart's points attribute a specified number of points that follow the JokePart's polynomial attribute
        '''
        all_points_len = len(self.prev_points + self.points)
        for i in range(all_points_len, all_points_len + num_points):
            pt = self.polynomial(i)
            self.points.append(pt)
    
    def add_custom_points(self, points: list = []):
        """Append a list of numbers to the JokePart's points attribute.

        Args:
            points (list, optional): the points to be added. Defaults to [].
        """
        float_points = [float(p)for p in points]
        self.points += float_points

    def fit_polynomial(self):
        '''
        Fits a polynomial function to the JokePart's points attribute.\
        Given n points, the polynomial function will have n terms.
        '''
        all_points = self.prev_points + self.points
        degree = len(all_points)-1
        x = [i for i in range(degree+1)]
        p = P.fit(x,all_points,degree,[])
        # new_coefs = [round(c) for c in p.coef]
        # p = P(new_coefs)
        self.polynomial = p


pjp = PolynomialJokePart()
print(pjp.json())
pjp.add_custom_points([4,2])
print('now with points:\n', pjp.json())
pjp.fit_polynomial()
print('now with a polynomial:\n', pjp.json())