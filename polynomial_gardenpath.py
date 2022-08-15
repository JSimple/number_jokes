from math import log2
from .joke_part import PolynomialJokePart as JP
from numpy.polynomial import Polynomial as P
from random import *
import json

class PGPEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, JP):
            return({
                'prev_points' : obj.prev_points,
                'points' : obj.points,
                'polynomial' : list(obj.polynomial.coef),
                })
        return super().default(obj)

class PolynomialGardenpath():
    
    def __init__(self, random_seed = None) -> None:
                
        if not random_seed:
            random_seed = random()

        seed(random_seed)
        self.joke_parts = []
    
    def clear(self):
        self.joke_parts = []
    
    def json(self):
        return json.dumps(self.__dict__, cls=PGPEncoder)
    
    def _all_points(self):
        all_points = []
        
        if self.joke_parts:
            all_points = self.joke_parts[-1].prev_points + self.joke_parts[-1].points
            
        return all_points
    
    def add_joke_part_w_points(self, starting_points: list, auto_fill: int = 0):
        """Creates a new section (JokePart) of the joke, using a list of numbers, and appends it to the PolynomialGardenpath's joke_parts attribute.
        
        Args:
            starting_points : a list of numbers that will be used to determine the JokePart's polynomial
            auto_fill : an integer representing how many more points to fill in after starting_points. These points are filled in using the JokePart's polynomial.
        """
        # gather all the points from all the previous jokeparts
        prev_points = self._all_points()
        jp = JP(starting_points, prev_points)
        #give the joke part a polynomial function fitted to all the joke's points so far
        jp.fit_polynomial()
        # add points untill desired length
        if auto_fill:
            jp.add_points(auto_fill)
        # append to joke_parts
        self.joke_parts.append(jp)
        
    def add_joke_part_w_polynomial(self, polynomial, num_pts):
        """Creates a new section (JokePart) of the joke, using a numpy Polynomial and a number of points, and appends the JokePart to the PolynomialGardenpath's joke_parts attribute.
        
        Args:
            polynomial : a numpy Polynomial used to determine the points in the JokePart
            num_pts : the number of points in the desired joke part
        """
        # parameter error handling
        terms = len(polynomial.coef)
        if num_pts < terms:
            raise ValueError ('The number of points in the JokePart must be greater than or equal to the number of terms in its polynomial.')
        
        # create jokepart with desired number of points
        prev_points = self._all_points
        jp = JP(prev_points= prev_points, polynomial=polynomial)
        jp.add_points(num_pts)
        # append to joke_parts
        self.joke_parts.append(jp.points)
    
    def _gen_value_range(self, start = 1, scaling_factor = 1000):
        """Helper function for functions that use _gen_pts. Creates a tuple representing a vlaue range, based on thow many JokeParts are in the joke and a scaling factor.
        """
        scaling_order = log2(len(self.joke_parts) + 1)
        maxi = start * 10 * (scaling_factor ** scaling_order)
        mini = (maxi * -1) + 9
        
        return (mini,maxi)
    
    def _gen_pts(self, len: int = 2, val_range: tuple = (-1.0,10.0), rounding: int = 0):
        """Utility function that generates a list of random points.
        
        Args:
            len (int, optional): length of list. Defaults to 2.
            val_range (tuple, optional): the range for the values in the list. Defaults to (-1.0,10.0).
            rounding (int, optional): how many significant digits below the decimal point each number has. Defaults to 0.

        Returns:
            None
        """
        mini, maxi = val_range
        return [round(mini + (maxi - mini) * random(), rounding) for i in range(len)]
    
    def _gen_polynomial(self, degree: int = 1, coef_range: tuple = (-10.0,10.0)):
        """Utility function that generates a random polynomial that can be used to create JokeParts.

        Args:
            degree (int, optional): the polynomial's highest degree. Defaults to 1.
            coef_range (tuple, optional): the value range for the polynomial's coeficients. Defaults to (-10.0,10.0).

        Returns:
            _type_: _description_
        """
        terms = degree + 1
        coefs = self._gen_pts(terms,coef_range)
        p = P(coefs)
        return p
    
    def _validate_gen_params(self, jp_degree_and_length):
        """Makes sure that valid parameters are being passed to random joke generation methods.

        Args:
            jp_degree_and_length (list of tuples): _description_
        """
        prev_total_length = len(self._all_points())
        
        for degree, length in jp_degree_and_length:
            assert (degree >= 0 and length > 0),"A JokePart must have a positive length and a polynomial with a positive degree."
            assert (prev_total_length <= degree),"A JokePart must have a polynomial with an equal or higher degree to the total number of points in the joke leading up to it."
            assert (degree < prev_total_length + length),"A JokePart's polynomial degree must be smaller than the number of points in the joke up to and including the JokePart."
            prev_total_length += length 
    
    def add_gen_joke_parts(self, jp_degree_and_length: list, rounding = 0):
        """_summary_

        Args:
            jp_degree_and_length (list, optional): _description_. Defaults to [(2,4),(5,3)].
        """
        # Validate parameters
        self._validate_gen_params(jp_degree_and_length)
        
        # generate each joke part
        joke_prev_points = self._all_points()
        for i,(degree,length) in enumerate(jp_degree_and_length): 
            random_points = self._gen_pts(degree + 1 - len(joke_prev_points), self._gen_value_range(), rounding)
            jp = JP(random_points, joke_prev_points)
            jp.fit_polynomial()
            jp.add_points(length - len(random_points))
            joke_prev_points += jp.points
            self.joke_parts.append(jp)
    
    def gen_joke(self, jp_degree_and_length = [(1,4),(4,3)], rounding = 0):
        """Generates a new polynomial gardenpath number joke, and sets it as as self.joke_parts.

        Args:
            jp_degree_and_length (list, optional): A list of tuples representing parameters (length, polynomial degree) for each of the joke's JokeParts. Defaults to [(1,4),(4,3)].
            range_scaling (int, optional): _description_. Defaults to 3.
            rounding (int, optional): _description_. Defaults to 1.
        """
        self.clear()
        self.add_gen_joke_parts(jp_degree_and_length, rounding)
    
        
# pgp = PolynomialGardenpath()

# pgp.gen_joke()
# # for jp in pgp.joke_parts:
# #     print(jp.points,jp.polynomial)
# pgp.add_gen_joke_parts([(8,3),(11,4)])
# # for jp in pgp.joke_parts:
# #     print(jp.points,jp.polynomial)    
# print(pgp._all_points())
# my_json = pgp.json()
# parsed = json.loads(my_json)
# print(json.dumps(parsed, indent=4, sort_keys=True))
    
# Joke Param Structure
        # setup:
        #   - generation method: 
        #       - polynomial
        #           - num_pts
        #           - coefs
        #               - random
        #                   - coef range
        #               - custom
        #           
        #       - points
        #           - autofill
        #               - custom
        #               - random
        #           - starting points
        #               - custom
        #               - random
        #                   - num points
        #                   - point range
        #
        # punchlines:
        #       - autofill
        #           - custom
        #           - random
        #       - starting points
        #           - custom
        #           - random
        #               - num points
        #               - point range
        #