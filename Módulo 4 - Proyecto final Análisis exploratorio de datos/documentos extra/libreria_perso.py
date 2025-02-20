# Exploración inicial
def exploracion_inicial(df, tipo = None):
    if tipo == 'version_lite':
        print("¿Cuántas filas y columnas hay en el conjunto de datos?")
        num_filas, num_columnas = df.shape
        print("\tHay {:,} filas y {:,} columnas.".format(num_filas, num_columnas))

        print("¿Cuáles son las primeras dos filas del conjunto de datos?")
        display(df.head(2))
        print('\n########################################################################################')
    else:
        print("¿Cuántas filas y columnas hay en el conjunto de datos?")
        num_filas, num_columnas = df.shape
        print("\tHay {:,} filas y {:,} columnas.".format(num_filas, num_columnas))
        print('\n########################################################################################')

        print("¿Cuáles son las primeras cinco filas del conjunto de datos?")
        display(df.head())
        print('\n########################################################################################')

        print("¿Cuáles son las últimas cinco filas del conjunto de datos?")
        display(df.tail())
        print('\n########################################################################################')

        print("¿Cómo puedes obtener una muestra aleatoria de filas del conjunto de datos?")
        display(df.sample(n = 5))
        print('\n########################################################################################')

        print("¿Cuáles son las columnas del conjunto de datos?")
        for i in list(df.columns):
            print('\t - ' + i)
        print('\n########################################################################################')

        print("¿Cuál es el tipo de datos de cada columna?")
        print(df.dtypes)
        print('\n########################################################################################')

        print("¿Cuántas columnas hay de cada tipo de datos?")
        print(df.dtypes.value_counts())
        print('\n########################################################################################')

        print("¿Cómo podríamos obtener información más completa sobre la estructura y el contenido del DataFrame?")
        print(df.info())
        print('\n########################################################################################')

        print("¿Cuántos valores únicos tiene cada columna?")
        print(df.nunique())
        print('\n########################################################################################')

        print("¿Cuáles son las estadísticas descriptivas básicas de todas las columnas?")
        display(df.describe(include = 'all').fillna(''))
        print('\n########################################################################################')

        print("¿Hay valores nulos en el conjunto de datos?")
        print(df.isnull().sum().sort_values(ascending = False))
        print('\n########################################################################################')

        print("¿Cuál es el porcentaje de valores nulos en cada columna?")
        print(round((df.isnull().sum()/len(df)*100), 2).sort_values(ascending = False))
        print('\n########################################################################################')    

# Detección de outliers
## Importar librerias de visualización: 
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# Función para detectar los outliers
def deteccion_outliers (df, variable): 
    columna = df[variable]

    sns.boxplot(
        data = df, #cambiar "df" por el dataframe que se este utilizando
        y=variable, #cambiar "variable" por el nombre de la variable que estemos analizando
    )
    plt.show()

df_sin_outliers = df[~df['ciudad_num'].isin(ciudades_outliers)].reset_index(drop = True) # Revisar los nombres de los DF y columnas. "ciudades_outliers es una variable con una lista de los numeros de las ciudades que tienen outliers"

# Calcular los límites del boxplot    
limite_inferior = Q1 - 1.5*IQR 
limite_superior = Q3 - 1.5*IQR

print(f"Los valores atípicos se definen como aquellos que caen fuera del siguiente rango:")
print(f"\t - Límite inferior (considerado extremadamente bajo): {limite_inferior:.2f}")
print(f"\t - Límite superior (considerado extremadamente alto): {limite_superior:.2f}")


# Barplot: función para graficar en barras
def graficar_barras_px (df, variable_analisis):
    # Contar la frecuencia de la variable de análisis
    volumen = df[variable_analisis].value_counts().reset_index()
    volumen.columns = [variable_analisis, 'Volumen']

    # Crear el gráfico de barras
    fig = px.bar(volumen, x=variable_analisis, y='Volumen', text='Volumen')
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(title_text=f'Gráfico de barras: {variable_analisis}',
                      xaxis_title=variable_analisis,
                      yaxis_title='Volumen',
                      xaxis={'categoryorder':'total descending'})

    # Actualizar el fondo del gráfico a blanco
    fig.update_layout({
        'plot_bgcolor': 'rgba(255, 255, 255, 1)',
        'xaxis': {'showgrid': True, 'gridcolor': 'lightgrey'},
        'yaxis': {'showgrid': True, 'gridcolor': 'lightgrey'}
    })

    fig.show()

# Graficar proporciones: histograma con barras agrupadas por la segunda variable categórica
def graficar_proporciones(df, variable_categorica_1, variable_categorica_2):
    # Crear el histograma con barras agrupadas por la segunda variable categórica
    fig = px.histogram(df, x=variable_categorica_1, color=variable_categorica_2,
                       title='Análisis de múltiples variables categóricas',
                       labels={variable_categorica_1: f'Categoría: {variable_categorica_1}',
                               variable_categorica_2: f'Grupo: {variable_categorica_2}'},
                       text_auto=True,
                       barmode='group')

    # Actualizar títulos del gráfico
    fig.update_layout(yaxis_title='Volúmen',
                      legend_title=variable_categorica_2,
                      bargap=0.2)

    # Actualizar el fondo del gráfico a blanco
    fig.update_layout({
        'plot_bgcolor': 'rgba(255, 255, 255, 1)',
        'xaxis': {'showgrid': True, 'gridcolor': 'lightgrey'},
        'yaxis': {'showgrid': True, 'gridcolor': 'lightgrey'}
    })

    # Mostrar el gráfico
    fig.show()

# Graficar histograma
def graficar_histograma_px (df, variable_analisis):
    fig = px.histogram(df, x=variable_analisis, nbins=20,
                       title=f'Distribución de: {variable_analisis}')

    # Calcular media y mediana
    mean_val = df[variable_analisis].mean()
    median_val = df[variable_analisis].median()

    # Añadir línea vertical para la media
    fig.add_vline(x=mean_val, line_dash="dash", line_color="red",
                  annotation_text=f"Media: {mean_val:.2f}", annotation_position="top right")

    # Añadir línea vertical para la mediana
    fig.add_vline(x=median_val, line_dash="dot", line_color="green",
                  annotation_text=f"Mediana: {median_val:.2f}", annotation_position="top left")

    fig.update_layout(xaxis_title=variable_analisis, yaxis_title='Frecuencia')
    fig.show()

# Gráfico de dispersión: graficamos la correlación
def graficar_correlacion(df, variable_x, variable_y):
    # Crear el gráfico de dispersión usando Plotly Express para visualizar la correlación
    fig = px.scatter(df, x=variable_x, y=variable_y,
                     trendline='ols',  # Añade una línea de regresión
                     labels={variable_x: variable_x, variable_y: variable_y},
                     title=f'Correlación entre {variable_x} y {variable_y}')

    # Actualizar el fondo del gráfico a blanco y ajustar la cuadrícula
    fig.update_layout({
        'plot_bgcolor': 'rgba(255, 255, 255, 1)',
        'xaxis': {'showgrid': True, 'gridcolor': 'lightgrey'},
        'yaxis': {'showgrid': True, 'gridcolor': 'lightgrey'}
    })

    # Mostrar el gráfico
    fig.show()

# Gráfico Pie chart: gráfico de tartas
def graficar_pie_chart(df, variable_analisis):
  df_ = df[variable_analisis].value_counts().reset_index()
  df_.columns = [
      variable_analisis,
      'Volúmen'
  ]

  fig = px.pie(
      df_,
      names=variable_analisis,
      values='Volúmen',
      title=variable_analisis,
      width=800,
      height=500
  )
  fig.show()

# Gráfico Histograma bivariable
def graficar_histograma_bivariable_px (df, variable_analisis, variable_categorica=None, bins=20, show_mean_median=True):
    # Crear el histograma con la opción de segmentar por variable categórica
    if variable_categorica:
        fig = px.histogram(df, x=variable_analisis, color=variable_categorica, nbins=bins,
                           title=f'Distribución de {variable_analisis} por {variable_categorica}')
    else:
        fig = px.histogram(df, x=variable_analisis, nbins=bins,
                           title=f'Distribución de: {variable_analisis}')

    # Opcional: Calcular y mostrar líneas de media y mediana
    if show_mean_median:
        mean_val = df[variable_analisis].mean()
        median_val = df[variable_analisis].median()

        # Añadir línea vertical para la media
        fig.add_vline(x=mean_val, line_dash="dash", line_color="red",
                      annotation_text=f"Media: {mean_val:.2f}", annotation_position="top right")

        # Añadir línea vertical para la mediana
        fig.add_vline(x=median_val, line_dash="dot", line_color="green",
                      annotation_text=f"Mediana: {median_val:.2f}", annotation_position="top left")

    # Actualizar títulos del gráfico
    fig.update_layout(xaxis_title=variable_analisis, yaxis_title='Frecuencia',
                      plot_bgcolor='rgba(255, 255, 255, 1)',
                      xaxis_showgrid=True, xaxis_gridcolor='lightgrey',
                      yaxis_showgrid=True, yaxis_gridcolor='lightgrey')

    # Mostrar el gráfico
    fig.show()

# 

# Analizar str y convertirlo en un objeto de fecha
## Importar la libreria necesaria para parser 

from dateutil import parser

## Función para cambiar el str a obj fecha
def try_parse_date(date_str):
    try:
        return parser.parse(date_str)
    except (ValueError, TypeError):
        return None


# La función encontrar_similar_sin_print(valor, valores_validos) busca el valor más similar a valor dentro de una lista de valores válidos (valores_validos) 
# utilizando process.extractOne(), que proviene de la biblioteca fuzzywuzzy o rapidfuzz.
## Importar la libreria necesaria para process.extractOne
from fuzzywuzzy import process

## Función para encontrar el valor más similar a "valor"
### Esta función devuelve una tupla (mejor_coincidencia, puntuación_de_similitud)
### Extrae el valor más similar y la puntuación de similitud.
### Si la puntuación es menor a 80, devuelve "revisar", lo que indica que la similitud no es suficiente.
### Si la puntuación es 80 o más, devuelve el valor más similar encontrado.

def encontrar_similar_sin_print (valor, valores_validos):
    resultado = process.extractOne(valor, valores_validos)
    valor_similar = resultado[0]
    probabilidad = resultado[1]

    if probabilidad < 80:
        return 'revisar'
    else:
        return valor_similar



