import numpy as np
from .safe_eval import make_function


def make_grid(umin, umax, vmin, vmax, n):
    u = np.linspace(umin, umax, n)
    v = np.linspace(vmin, vmax, n)
    return np.meshgrid(u, v, indexing='ij')


def surface(name, U, V, params, custom=None):
    a = params.get('a', 1.0)
    R = params.get('R', 1.0)
    r = params.get('r', 0.35)
    if name == 'Plano':
        X = U; Y = V; Z = 0*U
    elif name == 'Esfera':
        X = R*np.cos(U)*np.sin(V); Y = R*np.sin(U)*np.sin(V); Z = R*np.cos(V)
    elif name == 'Cilindro':
        X = R*np.cos(U); Y = R*np.sin(U); Z = V
    elif name == 'Catenoide':
        X = a*np.cosh(V/a)*np.cos(U); Y = a*np.cosh(V/a)*np.sin(U); Z = V
    elif name == 'Helicoide':
        X = V*np.cos(U); Y = V*np.sin(U); Z = a*U
    elif name == 'Scherk':
        X = U; Y = V; Z = (1/a)*np.log(np.clip(np.cos(a*V),1e-6,None)/np.clip(np.cos(a*U),1e-6,None))
    elif name == 'Enneper':
        X = U - U**3/3 + U*V**2; Y = V - V**3/3 + V*U**2; Z = U**2 - V**2
    elif name == 'Toro':
        X = (R + r*np.cos(V))*np.cos(U); Y = (R + r*np.cos(V))*np.sin(U); Z = r*np.sin(V)
    elif name == 'Personalizada':
        fx,_ = make_function(custom.get('x','u'))
        fy,_ = make_function(custom.get('y','v'))
        fz,_ = make_function(custom.get('z','0'))
        X, Y, Z = fx(U,V), fy(U,V), fz(U,V)
        X = np.asarray(X + 0*U, dtype=float); Y = np.asarray(Y + 0*U, dtype=float); Z = np.asarray(Z + 0*U, dtype=float)
    else:
        raise ValueError(name)
    return np.stack([X, Y, Z], axis=-1)


def default_domain(name):
    if name in ['Esfera','Toro']:
        return 0, 2*np.pi, 0.05, np.pi-0.05
    if name in ['Cilindro','Catenoide']:
        return 0, 2*np.pi, -2, 2
    if name == 'Helicoide':
        return -2*np.pi, 2*np.pi, -2, 2
    if name == 'Scherk':
        return -1.2, 1.2, -1.2, 1.2
    return -2, 2, -2, 2
