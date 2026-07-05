import streamlit as st
import numpy as np
import pandas as pd
from modules.surfaces import make_grid, surface, default_domain
from modules.geometry import compute_geometry, apply_variation, total_area
from modules.plotter import make_plot

st.set_page_config(page_title='Geometria Diferencial Interativa', layout='wide')
st.title('Geometria Diferencial Interativa')
st.caption('Superfícies mínimas, curvatura média, curvatura gaussiana e variação normal de área')

with st.sidebar:
    st.header('1. Escolha a superfície')
    name = st.selectbox('Superfície', ['Plano','Esfera','Cilindro','Catenoide','Helicoide','Scherk','Enneper','Toro','Personalizada'])
    params = {}
    if name in ['Esfera','Cilindro','Toro']:
        params['R'] = st.slider('R', 0.2, 3.0, 1.0, 0.1)
    if name in ['Catenoide','Helicoide','Scherk']:
        params['a'] = st.slider('a', 0.2, 3.0, 1.0, 0.1)
    if name == 'Toro':
        params['r'] = st.slider('r', 0.1, 1.5, 0.35, 0.05)
    custom = {}
    if name == 'Personalizada':
        st.markdown('Use expressões em `u` e `v`: `sin`, `cos`, `cosh`, `sinh`, `exp`, `log`, `sqrt`, `pi`.')
        custom['x'] = st.text_input('x(u,v)', 'u')
        custom['y'] = st.text_input('y(u,v)', 'v')
        custom['z'] = st.text_input('z(u,v)', 'sin(u)*cos(v)')
    st.header('2. Domínio')
    u0,u1,v0,v1 = default_domain(name)
    umin = st.number_input('u mínimo', value=float(u0))
    umax = st.number_input('u máximo', value=float(u1))
    vmin = st.number_input('v mínimo', value=float(v0))
    vmax = st.number_input('v máximo', value=float(v1))
    n = st.slider('Resolução', 35, 130, 70, 5)
    st.header('3. Variação normal')
    h_expr = st.text_input('h(u,v)', 'sin(u)*cos(v)')
    t = st.slider('t em X_t = X + t h N', -1.0, 1.0, 0.0, 0.05)
    st.header('4. Visualização')
    color_by = st.selectbox('Colorir por', ['H: curvatura média','K: curvatura gaussiana','Densidade de área','h(u,v)','z'])
    show_normals = st.checkbox('Mostrar vetores normais', value=False)

try:
    U,V = make_grid(umin, umax, vmin, vmax, n)
    du = (umax-umin)/(n-1); dv = (vmax-vmin)/(n-1)
    X = surface(name, U, V, params, custom)
    geom = compute_geometry(X, du, dv)
    Xt, h, h_parsed = apply_variation(X, geom['N'], U, V, h_expr, t)
    geom_t = compute_geometry(Xt, du, dv)
    area0 = total_area(geom['area_density'], du, dv)
    areat = total_area(geom_t['area_density'], du, dv)

    st.markdown(r'''Nesta versão, o estudante escolhe uma superfície parametrizada $X(u,v)$, altera parâmetros e aplica uma variação normal
    $$X_t(u,v)=X(u,v)+t\,h(u,v)N(u,v).$$
    Ao mesmo tempo, observa numericamente $H$, $K$ e a área aproximada.''')

    col1,col2,col3,col4 = st.columns(4)
    col1.metric('Área de X', f'{area0:.4f}')
    col2.metric('Área de X_t', f'{areat:.4f}', f'{areat-area0:+.4f}')
    col3.metric('média |H_t|', f'{np.nanmean(np.abs(geom_t["H"])):.4e}')
    col4.metric('média K_t', f'{np.nanmean(geom_t["K"]):.4e}')

    if color_by.startswith('H'):
        C = geom_t['H']; ct = 'H'
    elif color_by.startswith('K'):
        C = geom_t['K']; ct = 'K'
    elif color_by.startswith('Densidade'):
        C = geom_t['area_density']; ct = 'dA'
    elif color_by.startswith('h'):
        C = h; ct = 'h'
    else:
        C = Xt[...,2]; ct = 'z'

    left,right = st.columns([2.2,1])
    with left:
        st.plotly_chart(make_plot(U,V,Xt,C,f'{name}: superfície variada X_t',ct,show_normals,geom_t['N']), use_container_width=True)
    with right:
        st.subheader('Leitura geométrica')
        st.write(f'Função de variação:  **h(u,v) = {h_parsed}**')
        st.write('Quando `t=0`, vemos a superfície inicial. Quando `t` muda, cada ponto desloca-se na direção normal com intensidade dada por `h(u,v)`.')
        st.write('Para superfícies mínimas, espera-se observar `H` próximo de zero, salvo erros numéricos e efeitos de borda.')
        st.latex(r'H=\frac{eG-2fF+gE}{2(EG-F^2)}')
        st.latex(r'K=\frac{eg-f^2}{EG-F^2}')

    st.subheader('Área aproximada em função de t')
    ts = np.linspace(-1,1,21)
    vals = []
    for tau in ts:
        Xtau,_,_ = apply_variation(X, geom['N'], U, V, h_expr, float(tau))
        gtau = compute_geometry(Xtau, du, dv)
        vals.append(total_area(gtau['area_density'], du, dv))
    st.line_chart(pd.DataFrame({'t':ts,'Área aproximada':vals}).set_index('t'))

except Exception as e:
    st.error('Não foi possível gerar a superfície. Verifique domínio, parâmetros e expressões digitadas.')
    st.exception(e)
