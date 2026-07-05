import numpy as np
import plotly.graph_objects as go


def make_plot(U,V,X,color_values,title,color_title,show_normals=False,N=None, stride=8):
    fig = go.Figure()
    fig.add_trace(go.Surface(x=X[...,0], y=X[...,1], z=X[...,2], surfacecolor=color_values,
                             colorscale='Viridis', colorbar=dict(title=color_title), showscale=True, opacity=0.96))
    if show_normals and N is not None:
        ii = range(0, X.shape[0], stride); jj = range(0, X.shape[1], stride)
        scale = 0.25
        for i in ii:
            for j in jj:
                p = X[i,j]; n = N[i,j]
                fig.add_trace(go.Scatter3d(x=[p[0], p[0]+scale*n[0]], y=[p[1], p[1]+scale*n[1]], z=[p[2], p[2]+scale*n[2]], mode='lines', line=dict(width=3), showlegend=False))
    fig.update_layout(title=title, height=690, scene=dict(aspectmode='data'), margin=dict(l=0,r=0,t=40,b=0))
    return fig
