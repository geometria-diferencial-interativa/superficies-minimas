# Geometria Diferencial Interativa

Plataforma em Streamlit para visualizar superfícies parametrizadas, curvatura média, curvatura gaussiana e variações normais de área.

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar

Coloque estes arquivos em um repositório do GitHub e publique no Streamlit Community Cloud.

## Fórmulas usadas

A superfície inicial é X(u,v). A variação normal é

X_t(u,v) = X(u,v) + t h(u,v) N(u,v).

As curvaturas são calculadas numericamente pelas formas fundamentais:

H = (eG - 2fF + gE)/(2(EG-F^2))
K = (eg-f^2)/(EG-F^2)
