from joke_part import PolynomialJokePart as JP
from numpy.polynomial import Polynomial as P
from random import random
import json

#TODO: allpoints bug. refactor to remove allpoints from PJP

class PGPEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, JP):
            return({
                'prev_points' : obj.prev_points,
                'points' : obj.points,
                'all_points' : obj.all_points,
                'polynomial' : {
                    'coef' : list(obj.polynomial.coef),
                    'str' : str(obj.polynomial)
                }
            })
        return super().default(obj)

class PolynomialGardenpath():
    
    def __init__(self) -> None:
        self.joke_parts = []
    
    def clear(self):
        self.joke_parts = []
    
    def json(self):
        return json.dumps(self.__dict__, cls=PGPEncoder)
    
    def add_joke_part_w_points(self, starting_points: list, auto_fill: int = 0):
        """Creates a new section (JokePart) of the joke, using a list of numbers, and appends it to the PolynomialGardenpath's joke_parts attribute.
        
        Args:
            starting_points : a list of numbers that will be used to determine the JokePart's polynomial
            auto_fill : an integer representing how many more points to fill in after starting_points. These points are filled in using the JokePart's polynomial.
        """
        # gather all the points from all the previous jokeparts
        print ('jokeparts: ', self.joke_parts)
        if not self.joke_parts:
            prev_points = []
        else:
            last_joke_part = self.joke_parts[-1]
            prev_points = last_joke_part.all_points

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
        jp = JP(polynomial=polynomial)
        prev_points = [] if not self.joke_parts else self.joke_parts[-1].all_points
        jp.all_points = prev_points
        jp.add_points(num_pts)

        # append to joke_parts
        self.joke_parts.append(jp.points)
    
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
        prev_total_length = 0
        if self.joke_parts:
            prev_total_length = len(self.joke_parts[-1].all_points)
        
        for degree, length in jp_degree_and_length:
            assert (degree >= 0 and length > 0),"A JokePart must have a positive length and a polynomial with a positive degree."
            assert (prev_total_length <= degree),"A JokePart must have a polynomial with an equal or higher degree to the total number of points in the joke leading up to it."
            assert (degree < prev_total_length + length),"A JokePart's polynomial degree must be smaller than the number of points in the joke up to and including the JokePart."
            prev_total_length += length
    
    def _get_all_points(self):
        all_points = []
        if self.joke_parts:
            all_points = self.joke_parts[-1].all_points
        
        return all_points
        
    
    def add_gen_joke_parts(self, jp_degree_and_length: list, range_scaling = 1, rounding = 0):
        """_summary_

        Args:
            jp_degree_and_length (list, optional): _description_. Defaults to [(2,4),(5,3)].
        """
        # Validate parameters
        self._validate_gen_params(jp_degree_and_length)
        
        # generate each joke part
        all_prev_points = self._get_all_points()
        biggest_point_so_far = 0
        if all_prev_points:
            biggest_point_so_far = max(max(all_prev_points,key=abs))
        random_points_range = (-5,10)
        for i,(degree,length) in enumerate(jp_degree_and_length):
            if biggest_point_so_far:
                random_point_max = biggest_point_so_far ** range_scaling
                random_points_range = (-1 * random_point_max , random_point_max) 
            random_points = self._gen_pts(degree + 1 - len(all_prev_points), random_points_range, rounding)
            jp = JP(random_points, all_prev_points)
            jp.fit_polynomial()
            jp.add_points(length - len(random_points))
            all_prev_points += jp.points
            biggest_point_in_jp = max(jp.points,key=abs)
            biggest_point_so_far = max([biggest_point_so_far,biggest_point_in_jp],key=abs)
            self.joke_parts.append(jp)
    
    def gen_joke(self, jp_degree_and_length = [(1,4),(4,3)], range_scaling = 3, rounding = 0):
        """Generates a new polynomial gardenpath number joke, and sets it as as self.joke_parts.

        Args:
            jp_degree_and_length (list, optional): A list of tuples representing parameters (length, polynomial degree) for each of the joke's JokeParts. Defaults to [(1,4),(4,3)].
            range_scaling (int, optional): _description_. Defaults to 3.
            rounding (int, optional): _description_. Defaults to 1.
        """
        self.clear()
        self.add_gen_joke_parts(jp_degree_and_length, range_scaling, rounding)
    
        
pgp = PolynomialGardenpath()

pgp.gen_joke([(0,1),(1,1)])
# for jp in pgp.joke_parts:
#     print(jp.points,jp.polynomial)
pgp.add_gen_joke_parts([(2,1),(3,1)])
# for jp in pgp.joke_parts:
#     print(jp.points,jp.polynomial)    
print(pgp._get_all_points())
my_json = pgp.json()
parsed = json.loads(my_json)
print(json.dumps(parsed, indent=4, sort_keys=True))
    
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