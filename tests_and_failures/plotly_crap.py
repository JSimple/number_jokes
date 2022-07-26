def animate(self):
        
        joke_pts = self.setup_pts + self.punchline_pts
        jk_len = len(joke_pts)
        st_len = len(self.setup_pts)
        pl_len = len(self.punchline_pts)
        
        linspace_pts = 1000
        animation_step = linspace_pts//len(joke_pts)
        
        x = np.linspace(0, len(joke_pts), linspace_pts)
        xm = np.min(x) #- 1.5
        xM = np.max(x) #+ 1.5
        
        st_y = self.setup_func(x)
        st_ym = np.min(st_y) #- 1.5
        st_yM = np.max(st_y) #+ 1.5
        
        pl_y = self.punchline_func(x)
        pl_ym = np.min(pl_y) #- 1.5
        pl_yM = np.max(pl_y) #+ 1.5
        
        
        frames = []
        i_frames = 20
        z_frames = 0
        
        for f in range(st_len * i_frames):
            if f % i_frames == 0:
                color = 'red'
                plot_times = 30
            else:
                color = '#0300ab'
                plot_times = 1
            
            fr = go.Frame(data=[go.Scatter(
                x=[x[int(f * animation_step / i_frames)]],
                y=[st_y[int(f * animation_step / i_frames)]],
                mode="markers",
                marker=dict(color=color, size=10)),
            ])
            # fr.update(
            #     layout=dict(yaxis=dict(range=[st_ym,st_yM]))
            # )
            frames += [fr] * plot_times
        
        
        # for f in range(z_frames):
        #     fr = go.Frame(
        #         data=[
        #             go.Scatter(
        #                 x=[x[int(st_len * animation_step)]],
        #                 y=[pl_y[int(f * animation_step / i_frames)]],
        #                 mode="markers",
        #                 marker=dict(color='red', size=10))
        #             ]
        #         )
        #     fr.update(
        #         layout=dict(yaxis=dict(range=[pl_ym,pl_yM]))
        #     )
        #     frames += [fr]
        
            
        for f in range((st_len * i_frames) + z_frames, jk_len * i_frames):
            if f % i_frames == 0:
                color = 'red'
                plot_times = 2
            else:
                color = '#009da6'
                plot_times = 1
            
            fr = go.Frame(
                data=[
                    go.Scatter(
                        x=[x[int(f * animation_step / i_frames)]],
                        y=[pl_y[int(f * animation_step / i_frames)]],
                        mode="markers",
                        marker=dict(color=color, size=10))
                    ]
                # layout = go.Layout(
                #     yaxis=dict(range=[pl_ym, pl_yM], autorange=False, zeroline=False))
            )
            fr.update(
                layout=dict(yaxis=dict(range=[pl_ym,pl_yM]),xaxis=dict(range=[xm,xM]) )
            )
            frames += [fr] * plot_times

        
        st_curve = go.Scatter(x=x, y=st_y,
                    mode="lines",
                    name = 'setup',
                    line=dict(width=2, color="blue"))
        pl_curve = go.Scatter(x=x, y=pl_y,
                    mode="lines",
                    name = 'punchline',
                    line=dict(width=2, color="cyan"))
        
        fig = go.Figure(
            data=[st_curve,st_curve,pl_curve,pl_curve],
            layout=go.Layout(
                xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
                yaxis=dict(range=[st_ym, st_yM], autorange=False, zeroline=False),
                title_text="Joke Visualization", 
                hovermode="closest",
                transition={'duration': 100}, #,'easing': 'linear', 'ordering': 'traces first'},
                updatemenus=[dict(type="buttons",
                                buttons=[dict(label="Play",
                                                method="animate",
                                                args=[None,
                                                      dict(frame = dict(duration = 100,
                                                                        redraw=True))
                                                    ])])]),
            frames= frames
        )
        fig.show()