import numpy as np
import plotly.graph_objects as go


def _finite_minmax(A):
    A = np.asarray(A, dtype=float)
    vals = A[np.isfinite(A)]
    if vals.size == 0:
        return -1.0, 1.0
    q1, q2 = np.nanpercentile(vals, [2, 98])
    if np.isclose(q1, q2):
        q1, q2 = float(np.nanmin(vals)), float(np.nanmax(vals))
    if np.isclose(q1, q2):
        q1, q2 = q1 - 1.0, q2 + 1.0
    return float(q1), float(q2)


def make_plot(
    U,
    V,
    X,
    color_values,
    title,
    color_title,
    show_normals=False,
    N=None,
    stride=8,
    point_index=None,
    show_tangent=False,
    Xu=None,
    Xv=None,
):
    """Cria a visualização 3D da superfície.

    Além da superfície, pode mostrar vetores normais, um ponto escolhido e,
    nesse ponto, as direções tangentes Xu e Xv.
    """
    cmin, cmax = _finite_minmax(color_values)
    fig = go.Figure()
    fig.add_trace(
        go.Surface(
            x=X[..., 0],
            y=X[..., 1],
            z=X[..., 2],
            surfacecolor=color_values,
            colorscale="Viridis",
            colorbar=dict(title=color_title),
            cmin=cmin,
            cmax=cmax,
            showscale=True,
            opacity=0.96,
            name="Superfície",
        )
    )

    if show_normals and N is not None:
        ii = range(0, X.shape[0], stride)
        jj = range(0, X.shape[1], stride)
        scale = 0.22
        for i in ii:
            for j in jj:
                p = X[i, j]
                n = N[i, j]
                if np.all(np.isfinite(p)) and np.all(np.isfinite(n)):
                    fig.add_trace(
                        go.Scatter3d(
                            x=[p[0], p[0] + scale * n[0]],
                            y=[p[1], p[1] + scale * n[1]],
                            z=[p[2], p[2] + scale * n[2]],
                            mode="lines",
                            line=dict(width=3),
                            showlegend=False,
                            hoverinfo="skip",
                        )
                    )

    if point_index is not None:
        i, j = point_index
        p = X[i, j]
        if np.all(np.isfinite(p)):
            fig.add_trace(
                go.Scatter3d(
                    x=[p[0]],
                    y=[p[1]],
                    z=[p[2]],
                    mode="markers+text",
                    marker=dict(size=7),
                    text=["P"],
                    textposition="top center",
                    name="Ponto P",
                )
            )

            if N is not None:
                n = N[i, j]
                if np.all(np.isfinite(n)):
                    fig.add_trace(
                        go.Scatter3d(
                            x=[p[0], p[0] + 0.55 * n[0]],
                            y=[p[1], p[1] + 0.55 * n[1]],
                            z=[p[2], p[2] + 0.55 * n[2]],
                            mode="lines",
                            line=dict(width=7),
                            name="N(P)",
                        )
                    )

            if show_tangent and Xu is not None and Xv is not None:
                for vec, label in [(Xu[i, j], "Xu(P)"), (Xv[i, j], "Xv(P)")]:
                    length = np.linalg.norm(vec)
                    if np.isfinite(length) and length > 1e-12:
                        vec = vec / length
                        fig.add_trace(
                            go.Scatter3d(
                                x=[p[0] - 0.45 * vec[0], p[0] + 0.45 * vec[0]],
                                y=[p[1] - 0.45 * vec[1], p[1] + 0.45 * vec[1]],
                                z=[p[2] - 0.45 * vec[2], p[2] + 0.45 * vec[2]],
                                mode="lines",
                                line=dict(width=6),
                                name=label,
                            )
                        )

    fig.update_layout(
        title=title,
        height=700,
        scene=dict(aspectmode="data"),
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=0.01, xanchor="left", x=0.01),
    )
    return fig
