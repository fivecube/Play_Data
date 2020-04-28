import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
from dash.exceptions import PreventUpdate


def cluster_function(value):
    np.random.seed(1)
    fig = go.Figure()
    buttons_list = []
    if value is None:
        raise PreventUpdate
    if int(value)>= 2:
        x0 = np.random.normal(2, 0.4, 400)
        y0 = np.random.normal(2, 0.4, 400)
        x1 = np.random.normal(3, 0.6, 600)
        y1 = np.random.normal(6, 0.4, 400)
        fig.add_trace(
            go.Scatter(
                x=x0,
                y=y0,
                mode="markers",
                marker=dict(color="DarkOrange")
            )
        )
        fig.add_trace(
            go.Scatter(
                x=x1,
                y=y1,
                mode="markers",
                marker=dict(color="Crimson")
            )
        )

        cluster0 = [dict(type="circle",
                         xref="x", yref="y",
                         x0=min(x0), y0=min(y0),
                         x1=max(x0), y1=max(y0),
                         line=dict(color="DarkOrange"))]
        cluster1 = [dict(type="circle",
                         xref="x", yref="y",
                         x0=min(x1), y0=min(y1),
                         x1=max(x1), y1=max(y1),
                         line=dict(color="Crimson"))]

        buttons_list.append(dict(label="None",
                             method="relayout",
                             args=["shapes", []]))
        buttons_list.append( dict(label="Cluster 0",
                             method="relayout",
                             args=["shapes", cluster0]))
        buttons_list.append(dict(label="Cluster 1",
                     method="relayout",
                     args=["shapes", cluster1]))
        fig.update_layout(
            title_text="Highlight Clusters",
            showlegend=False,
        )
    if int(value) >= 3:
        x2 = np.random.normal(4, 0.2, 200)
        y2 = np.random.normal(4, 0.4, 200)
        fig.add_trace(
            go.Scatter(
                x=x2,
                y=y2,
                mode="markers",
                marker=dict(color="RebeccaPurple")
            )
        )
        cluster2 = [dict(type="circle",
                         xref="x", yref="y",
                         x0=min(x2), y0=min(y2),
                         x1=max(x2), y1=max(y2),
                         line=dict(color="RebeccaPurple"))]
        buttons_list.append(dict(label="Cluster 2",
                         method="relayout",
                         args=["shapes", cluster2]))

    else:
        pass
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                buttons=buttons_list,
            )
        ]
    )
    return html.Div([
            dcc.Graph(figure=fig)
        ])
