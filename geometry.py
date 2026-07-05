import numpy as np
from .safe_eval import make_function


def dA(A, axis, step):
    return np.gradient(A, step, axis=axis, edge_order=2)


def dot(A,B): return np.sum(A*B, axis=-1)
def norm(A): return np.linalg.norm(A, axis=-1)

def compute_geometry(X, du, dv):
    Xu = dA(X, 0, du); Xv = dA(X, 1, dv)
    Xuu = dA(Xu, 0, du); Xuv = dA(Xu, 1, dv); Xvv = dA(Xv, 1, dv)
    cross = np.cross(Xu, Xv)
    W = norm(cross)
    eps = 1e-10
    N = cross / np.maximum(W[...,None], eps)
    E = dot(Xu, Xu); F = dot(Xu, Xv); G = dot(Xv, Xv)
    e = dot(Xuu, N); f = dot(Xuv, N); g = dot(Xvv, N)
    den = np.maximum(E*G-F**2, eps)
    H = (e*G - 2*f*F + g*E)/(2*den)
    K = (e*g - f**2)/den
    area_density = np.sqrt(den)
    return {'Xu':Xu,'Xv':Xv,'N':N,'E':E,'F':F,'G':G,'e':e,'f':f,'g':g,'H':H,'K':K,'area_density':area_density}


def apply_variation(X, N, U, V, h_expr, t):
    fh, parsed = make_function(h_expr)
    h = np.asarray(fh(U,V) + 0*U, dtype=float)
    return X + t*h[...,None]*N, h, parsed


def total_area(area_density, du, dv):
    return float(np.nansum(area_density)*du*dv)
