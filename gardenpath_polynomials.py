# polynomial generator rule: rx^n + rx^n-1 ... rx^n-n
from scipy.optimize import curve_fit
from random import *
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from setuptools import setup
import plotly.graph_objects as go
from math import pow

class NumberJoke:
    def __init__(self, setup_terms = 2, setup_length = 4, punchline_terms = 5, punchline_length = 3):

        self.setup_terms = setup_terms
        self.setup_length = setup_length 
        self.punchline_terms = punchline_terms
        self.punchline_length = punchline_length
        
        #### The following attributes get initialized by gen_joke() ####
        #LEAVE COMMENTS
        self.setup = None
        self.setup_pts = None
        self.setup_rule = None
        self.setup_func = None
       
        self.punchline = None
        self.punchline_pts = None
        self.punchline_rule = None
        self.punchline_func = None
        
        self.joke = None
        self.visualization = None
        
        self.validate_params()
        self.gen_joke()
    
    def validate_params(self):
        ## docstrings - use `for var names`
        """_summary_
        Makes sure that the arguments passed to self.config() or to the NumberJoke class will result in a valid joke.
        Setup terms must be greater than 0.
        Setup length must be greater than or equal to setup terms.
        Punchline length must be greater than or equal to punchline terms minus setup length.
        Punchline terms must be greater than setup length.
        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
        """
        if self.setup_terms <= 0:
            raise ValueError ('Setup terms must be greater than 0!')
        if self.setup_length < self.setup_terms:
            raise ValueError ('Setup length must be greater than or equal to setup terms!')
        if self.punchline_length < self.punchline_terms - self.setup_length:
            raise ValueError ('Punchline length must be greater than or equal to punchline terms minus setup length!')
        if self.punchline_terms <= self.setup_length:
            raise ValueError ('Punchline terms must be greater than setup length!')  
    
    def config(self, setup_terms = None, setup_length = None, punchline_terms = None, punchline_length = None): ## is there a way to have it default to the current settings?
        """_summary_

        Args:
            setup_terms (int, optional): the number of terms in your setup rule's polynomial, (e.g. 2 for linear, 5 for quartic). Defaults to None.
            setup_length (int, optional): the number of points in your setup. Defaults to None.
            punchline_terms (int, optional): the number of terms in your punchline rule's polynomial, (e.g. 3 for quadratic, 6 for quintic). Defaults to None.
            punchline_length (int, optional): the number of points in your punchline. Defaults to None.

        Raises:
            exc: if you've entered int values that wouldn't result in a number joke
        """
        old_vals = dict(self.__dict__)
        self.setup_terms = self.setup_terms if setup_terms == None else setup_terms
        self.setup_length = setup_length if setup_length == None else setup_length
        self.punchline_terms = punchline_terms
        self.punchline_length = punchline_length        
        try:
            self.validate_params()
        except ValueError as exc:
            self.__dict__.update(old_vals)
            raise exc     
        self.gen_joke()
    
    def gen_joke(self):
        self.setup_polynomial, self.setup_polynomial_formatter = self.gen_polynomial_form(self.setup_terms)
        self.punchline_polynomial, self.punchline_polynomial_formatter = self.gen_polynomial_form(self.punchline_terms)
       
        self.setup = self.joke_part()
        self.setup_pts = self.setup[0]
        self.setup_rule = self.setup[1]
        self.setup_func = self.setup[2]
       
        self.punchline = self.joke_part(punchline=True)
        self.punchline_pts = self.punchline[0]
        self.punchline_rule = self.punchline[1]
        self.punchline_func = self.punchline[2]
        
        self.joke = (self.setup_pts + ['...'] + self.punchline_pts, 'This joke is funny because first you think the numers follow this rule:\n' + self.setup_rule + '\nbut then the punchline reveals that they actually follow this rule:\n' + self.punchline_rule)
        self.rating = 'unrated'
    
    def gen_polynomial_form(self, terms):
        params = ['param_' + str(i) for i in range(terms)]
        params_str = ', '.join(params)
        def formatter(coefs):
            # error handling
            if terms != len(coefs):
                raise Exception('you need to have the same number of terms as coeficients')
            format = f''
            for t in range(terms):
                if t == 0:
                    format += f'{coefs[t]}'
                elif t == 1:
                    format += f' + {coefs[t]} * x'
                else:
                    format += f' + {coefs[t]} * x^{t}'
            return format

        return eval(f'lambda x, {params_str}: {formatter(params).replace("^","**")}'), formatter
            
    def get_coef(self, pts, punchline = False):
        pts = self.setup_pts + pts if punchline else pts
        polynomial_fn = self.punchline_polynomial if punchline else self.setup_polynomial
        coefs = curve_fit(polynomial_fn, list(range(len(pts))), pts)[0]
        rounded = [round(coef, 2) for coef in coefs]
        return rounded
    
    # generates a list of random input points
    def gen_pts(self, len = 2, mini = -1.0, maxi = 10.0, rounding = 0):
        return [round(mini + (maxi - mini) * random(), rounding) for i in range(len)]
    
    # generates a setup or punchline
    def joke_part(self, punchline = False):
        # define variables according to whether this is a set-up or punchline
        length = self.punchline_length + self.setup_length if punchline else self.setup_length
        rand_pts = self.gen_pts(self.punchline_terms - self.setup_length, -10000, 10000, randint(0,5)) if punchline else self.gen_pts(len = self.setup_terms)
        polynomial_fn = self.punchline_polynomial if punchline else self.setup_polynomial
        formatter = self.punchline_polynomial_formatter if punchline else self.setup_polynomial_formatter
        
        coefs = self.get_coef(rand_pts, punchline)
        
        def jokepart_function(x):
            return polynomial_fn(x, *coefs)
        
        # generate the rest of the points in our joke_part
        start = (len(rand_pts) + self.setup_length) if punchline else len(rand_pts)
        new_pts = []
        for x in range(start,length):
            y = jokepart_function(x)
            new_pts.append(y)
            
        # return the points and the string-formatted rule for our joke part
        return rand_pts + new_pts,formatter(coefs),jokepart_function

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
        
    def visualize(self, show = True):
        
        joke_pts = self.setup_pts + self.punchline_pts
        x = np.linspace(0, len(joke_pts), 1000)
        st_y = self.setup_func(x)
        pl_y = self.punchline_func(x)
        
        fig, ax = plt.subplots(1,2)
        step = 1000//len(joke_pts)
        scaled_rng = range(0,1000,step)
        ax[0].plot(x, st_y, '-b*', markevery = scaled_rng[0:len(self.setup_pts)], label = self.setup_rule)
        st_ymin, st_ymax = ax[0].get_ylim()
        ax[0].plot(x, pl_y, '-c*', markevery = scaled_rng[len(self.setup_pts):], label = self.punchline_rule)
        ax[0].set_ylim(st_ymin,st_ymax)
        
        ax[1].plot(x, st_y, '-b*', markevery = scaled_rng[0:len(self.setup_pts)], label = self.setup_rule)
        ax[1].plot(x, pl_y, '-c*', markevery = scaled_rng[len(self.setup_pts):], label = self.punchline_rule)
        pl_ymin, pl_ymax = ax[1].get_ylim()
        plt.legend()
        plt.show() if show else plt.close('all')
        return (st_ymin,st_ymax,pl_ymin,pl_ymax)
    
    def animated_plot(self):
        # get the set up and punchline range
        st_ymin,st_ymax,pl_ymin,pl_ymax = self.visualize(show = False)
        
        joke_pts = self.setup_pts + self.punchline_pts
        x = np.linspace(0, len(joke_pts), 1000)
        st_y = self.setup_func(x)
        pl_y = self.punchline_func(x)

        # setup_pts * framerate number of frames with st_ymin,st_ymax
        # punchline_pts * framerate number of points * num seconds of traveling btwn joke pts
            # change the ymin and y max per frame
            # increment = (pl_ymin - st_ymin, pl_ymax - st_ymax) / num frames
        
        i_frames = 4
        frames_in_pl = len(self.punchline_pts) * i_frames
        # sty * growthrate ** ply
        # growthrate = ply root frames in pl
        
        y_lims = [(st_ymin, st_ymax)] * len(self.setup_pts) * i_frames
        min_increment = (pl_ymin - st_ymin)/frames_in_pl
        max_increment = (pl_ymax - st_ymax)/frames_in_pl
        y_lims += [(st_ymin + i * min_increment, st_ymax + i * max_increment) for i in range (1,frames_in_pl)]
        
        # Governing equasion: pl_y = st_y * (pl_y_growth_rate ** i)
        # https://www.reddit.com/r/askmath/comments/8cg62x/how_do_i_divide_100_into_12_exponentially/
        ymin_delta = abs(pl_ymin - st_ymin)
        ymax_delta = abs(pl_ymax - st_ymax)
        pl_ymin_growth_rate = ymin_delta ** (1/frames_in_pl)
        pl_ymax_growth_rate = ymax_delta ** (1/frames_in_pl)
            
        for i in range (1,frames_in_pl):
            y_min = st_ymin + (ymin_delta * (pl_ymin_growth_rate ** i))
            y_max = st_ymax + (ymax_delta * (pl_ymax_growth_rate ** i))
            y_lims.append((y_min,y_max))

        print(y_lims)
        
        for i,(ylim_min, ylim_max) in enumerate(y_lims):
            fig, ax = plt.subplots(1,1)
            # step = 1000//len(joke_pts)
            # scaled_rng = range(0,1000,step)
            ax.plot(x, st_y, '-b', label = self.setup_rule)
            ax.plot(x, pl_y, '-c', label = self.punchline_rule)
            ax.set_ylim(ylim_min,ylim_max)
            plt.show()
            #plt.savefig(f'./animated_plot/frame_{i}')
            #saves on disk and then stich together w commandline
            #marker: moving circle 
        #scaled_rng[0:len(self.setup_pts)]
        #scaled_rng[len(self.setup_pts):]
    
    
j = NumberJoke(2,2,5,3)

#j.tell_joke()
j.animated_plot()

        



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