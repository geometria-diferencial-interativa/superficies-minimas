import sympy as sp
import numpy as np

u, v = sp.symbols('u v')
_ALLOWED = {
    'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
    'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
    'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt,
    'abs': sp.Abs, 'pi': sp.pi, 'E': sp.E,
    'u': u, 'v': v
}

def make_function(expr: str):
    expr = (expr or '0').replace('^', '**')
    parsed = sp.sympify(expr, locals=_ALLOWED)
    free = parsed.free_symbols
    if not free.issubset({u, v}):
        raise ValueError('Use apenas as variáveis u e v.')
    return sp.lambdify((u, v), parsed, modules=['numpy']), sp.sstr(parsed)
