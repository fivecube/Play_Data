import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv("test.csv")
x_data = list(df['continent'].unique())
x_data_ = iter(df['continent'].unique())


y0 = df[df["continent"] == str(x_data_.__next__())]['gdp per capita'].values
y1 = df[df["continent"] == str(x_data_.__next__())]['gdp per capita'].values
y2 = df[df["continent"] == str(x_data_.__next__())]['gdp per capita'].values
y3 = df[df["continent"] == str(x_data_.__next__())]['gdp per capita'].values
y4 = df[df["continent"] == str(x_data_.__next__())]['population'].values


y_data = [y0, y1, y2, y3]

colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)',
          'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)']

fig = go.Figure()

for xd, yd, cls in zip(x_data, y_data, colors):
    fig.add_trace(go.Box(
        y=yd,
        name=xd,
        boxpoints='all',
        jitter=0.5,
        whiskerwidth=0.2,
        fillcolor=cls,
        marker_size=2,
        line_width=1)
    )

fig.update_layout(
    title="BOX PLOT STATISTICS FOR FILE NAMED test.csv",
    yaxis=dict(
        autorange=True,
        showgrid=True,
        zeroline=True,
        dtick=5,
        gridcolor='rgb(255, 255, 255)',
        gridwidth=1,
        zerolinecolor='rgb(255, 255, 255)',
        zerolinewidth=2,
    ),
    margin=dict(
        l=40,
        r=30,
        b=80,
        t=100,
    ),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
    showlegend=False
)

def get_box_stats():
    return fig