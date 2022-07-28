from joke_part import PolynomialJokePart as JP
from numpy.polynomial import Polynomial as P

class PolynomialGardenpath:
    
    def __init__(self) -> None:
        self.joke_parts = []
    
    
    def _add_joke_part_w_points(self, starting_points: list, auto_fill: int = 0):
        '''
        Creates a new section (JokePart) of the joke, using a list of numbers, and appends it to the PolynomialGardenpath's joke_parts attribute.
        
        Parameters:
            starting_points : a list of numbers that will be used to determine the JokePart's polynomial
            auto_fill : an integer representing how many more points to fill in after starting_points. These points are filled in using the JokePart's polynomial.
        '''
        # gather all the points from all the previous jokeparts
        prev_points = [] if not self.joke_parts else self.joke_parts[-1].all_points
        jp = JP(starting_points, prev_points)
        
        #give the joke part a polynomial function fitted to all the joke's points so far
        jp.fit_polynomial()
        
        # add points untill desired length
        if auto_fill:
            jp.add_points(auto_fill)
        
        # append to joke_parts
        self.joke_parts.append(jp)
        
    def _add_joke_part_w_polynomial(self,polynomial, num_pts):
        '''
        Creates a new section (JokePart) of the joke, using a numpy Polynomial and a number of points, and appends the JokePart to the PolynomialGardenpath's joke_parts attribute.
        
        Parameters:
            polynomial : a numpy Polynomial used to determine the points in the JokePart
            num_pts : the number of points in the desired joke part
        '''
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
        self.joke_parts.append(jp)
    
    #TODO: define generate setup, add as many punchlines as you want
        
    