# polynomial generator rule: rx^n + rx^n-1 ... rx^n-n
from scipy.optimize import curve_fit
from random import *
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from setuptools import setup
import plotly.graph_objects as go

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
        
    def visualize(self):
        
        joke_pts = self.setup_pts + self.punchline_pts
        x = np.linspace(0, len(joke_pts), 1000)
        st_y = self.setup_func(x)
        pl_y = self.punchline_func(x)
        
        fig, ax = plt.subplots(1,2)
        step = 1000//len(joke_pts)
        scaled_rng = range(0,1000,step)
        ax[0].plot(x, st_y, '-b*', markevery = scaled_rng[0:len(self.setup_pts)], label = self.setup_rule)
        ymin, ymax = ax[0].get_ylim()
        ax[0].plot(x, pl_y, '-c*', markevery = scaled_rng[len(self.setup_pts):], label = self.punchline_rule)
        ax[0].set_ylim(ymin,ymax)
        
        ax[1].plot(x, st_y, '-b*', markevery = scaled_rng[0:len(self.setup_pts)], label = self.setup_rule)
        ax[1].plot(x, pl_y, '-c*', markevery = scaled_rng[len(self.setup_pts):], label = self.punchline_rule)
        
        plt.legend()
        return (plt.show())
    
    
    ##### TO DO: animate in matplotlib?
    ##### https://matplotlib.org/stable/gallery/animation/strip_chart.html
    
    # def animated_vis(self):
    #     joke_pts = self.setup_pts + self.punchline_pts
    #     fig, ax = plt.subplots(1,2)
    #     x = np.linspace(0, len(joke_pts), 1000)
    #     st_y = self.setup_func(x)
    #     pl_y = self.punchline_func(x)
    #     st_line, = ax[0].plot(x, st_y)
    #     pl_line, = ax[1].plot(x, pl_y)
        
        
        
        
        
        
    # def animate(self):
        
    #     joke_pts = self.setup_pts + self.punchline_pts
    #     jk_len = len(joke_pts)
    #     st_len = len(self.setup_pts)
    #     pl_len = len(self.punchline_pts)
        
    #     linspace_pts = 1000
    #     animation_step = linspace_pts//len(joke_pts)
        
    #     x = np.linspace(0, len(joke_pts), linspace_pts)
    #     xm = np.min(x) #- 1.5
    #     xM = np.max(x) #+ 1.5
        
    #     st_y = self.setup_func(x)
    #     st_ym = np.min(st_y) #- 1.5
    #     st_yM = np.max(st_y) #+ 1.5
        
    #     pl_y = self.punchline_func(x)
    #     pl_ym = np.min(pl_y) #- 1.5
    #     pl_yM = np.max(pl_y) #+ 1.5
        
        
    #     frames = []
    #     i_frames = 20
    #     z_frames = 0
        
    #     for f in range(st_len * i_frames):
    #         if f % i_frames == 0:
    #             color = 'red'
    #             plot_times = 30
    #         else:
    #             color = '#0300ab'
    #             plot_times = 1
            
    #         fr = go.Frame(data=[go.Scatter(
    #             x=[x[int(f * animation_step / i_frames)]],
    #             y=[st_y[int(f * animation_step / i_frames)]],
    #             mode="markers",
    #             marker=dict(color=color, size=10)),
    #         ])
    #         # fr.update(
    #         #     layout=dict(yaxis=dict(range=[st_ym,st_yM]))
    #         # )
    #         frames += [fr] * plot_times
        
        
    #     # for f in range(z_frames):
    #     #     fr = go.Frame(
    #     #         data=[
    #     #             go.Scatter(
    #     #                 x=[x[int(st_len * animation_step)]],
    #     #                 y=[pl_y[int(f * animation_step / i_frames)]],
    #     #                 mode="markers",
    #     #                 marker=dict(color='red', size=10))
    #     #             ]
    #     #         )
    #     #     fr.update(
    #     #         layout=dict(yaxis=dict(range=[pl_ym,pl_yM]))
    #     #     )
    #     #     frames += [fr]
        
            
    #     for f in range((st_len * i_frames) + z_frames, jk_len * i_frames):
    #         if f % i_frames == 0:
    #             color = 'red'
    #             plot_times = 2
    #         else:
    #             color = '#009da6'
    #             plot_times = 1
            
    #         fr = go.Frame(
    #             data=[
    #                 go.Scatter(
    #                     x=[x[int(f * animation_step / i_frames)]],
    #                     y=[pl_y[int(f * animation_step / i_frames)]],
    #                     mode="markers",
    #                     marker=dict(color=color, size=10))
    #                 ]
    #             # layout = go.Layout(
    #             #     yaxis=dict(range=[pl_ym, pl_yM], autorange=False, zeroline=False))
    #         )
    #         fr.update(
    #             layout=dict(yaxis=dict(range=[pl_ym,pl_yM]),xaxis=dict(range=[xm,xM]) )
    #         )
    #         frames += [fr] * plot_times

        
    #     st_curve = go.Scatter(x=x, y=st_y,
    #                 mode="lines",
    #                 name = 'setup',
    #                 line=dict(width=2, color="blue"))
    #     pl_curve = go.Scatter(x=x, y=pl_y,
    #                 mode="lines",
    #                 name = 'punchline',
    #                 line=dict(width=2, color="cyan"))
        
    #     fig = go.Figure(
    #         data=[st_curve,st_curve,pl_curve,pl_curve],
    #         layout=go.Layout(
    #             xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
    #             yaxis=dict(range=[st_ym, st_yM], autorange=False, zeroline=False),
    #             title_text="Joke Visualization", 
    #             hovermode="closest",
    #             transition={'duration': 100}, #,'easing': 'linear', 'ordering': 'traces first'},
    #             updatemenus=[dict(type="buttons",
    #                             buttons=[dict(label="Play",
    #                                             method="animate",
    #                                             args=[None,
    #                                                   dict(frame = dict(duration = 100,
    #                                                                     redraw=True))
    #                                                 ])])]),
    #         frames= frames
    #     )
    #     #fig.update_layout(transition = {'duration': 1}, title_text = 'Joke') # make transitions faster
    #     ##fig.update_yaxes(autorange=True)
    #     fig.show()
    #     #### TODO: https://stackoverflow.com/questions/69584171/is-there-a-way-to-dynamically-change-a-plotly-animation-axis-scale-per-frame

        
        

        
    
#j = NumberJoke(2,2,5,3)

#j.tell_joke()
# j.visualize()
#j.animate()     

        



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