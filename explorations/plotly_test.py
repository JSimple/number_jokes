import plotly.express as px
df = px.data.gapminder()
df = df[(df['continent'] == 'Asia') & (df['year'].isin([1997, 2002, 2007]))]

scales = [2002]

fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
           size="pop", color="continent", hover_name="country",
           log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])

yranges = {2002:[0, 200]}

for f in fig.frames:
    if int(f.name) in yranges.keys():
        f.layout.update(yaxis_range = yranges[int(f.name)])

fig.show()



# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go

# df = pd.DataFrame(
#     {
#         "time": np.tile(pd.date_range("1-jan-2021", freq="1H", periods=12), 10),
#         "x": np.random.uniform(1, 4, 120),
#         "y": np.random.uniform(2, 5, 120),
#     }
# )
# fig = px.scatter(df, x="x", y="y", animation_frame=df["time"].dt.strftime("%H:%M"))

# go.Figure(
#     data=fig.data,
#     frames=[
#         fr.update(
#             layout={
#                 "xaxis": {"range": [min(fr.data[0].x) - 0.1, max(fr.data[0].x) + 0.1]},
#                 "yaxis": {"range": [min(fr.data[0].y) - 0.1, max(fr.data[0].y) + 0.1]},
#             }
#         )
#         for fr in fig.frames
#     ],
#     layout=fig.layout,
# )

# fig.show()

# import plotly.graph_objects as go

# import numpy as np

# # Generate curve data
# x = np.linspace(-10, 10, 200)
# y = x ** 2
# xm = np.min(x) - 1.5
# xM = np.max(x) + 1.5
# ym = np.min(y) - 1.5
# yM = np.max(y) + 1.5
# N = 25
# t = np.linspace(-10, 10, N)
# yy = t ** 2


# # Create figure
# fig = go.Figure(
#     data=[go.Scatter(x=x, y=y,
#                      mode="lines",
#                      line=dict(width=2, color="blue")),
#           go.Scatter(x=x, y=y,
#                      mode="lines",
#                      line=dict(width=2, color="blue"))],
#     layout=go.Layout(
#         xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
#         yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
#         title_text="Kinematic Generation of a Planar Curve", hovermode="closest",
#         updatemenus=[dict(type="buttons",
#                           buttons=[dict(label="Play",
#                                         method="animate",
#                                         args=[None])])]),
#     frames=[go.Frame(
#         data=[go.Scatter(
#             x=[t[k]],
#             y=[yy[k]],
#             mode="markers",
#             marker=dict(color="red", size=10))])

#         for k in range(N)]
# )

# fig.show()