#puede:
#buscar peliculas por generos - actores
#hacer listas de peliculas q ya viste / quieres ver
#dejar reseñas de peliculas y ver las reseñas de otras personas
#poner donde se puede ver cada pelicula
#poner el trailer, sinopsis y promedio de reseñas
#en google un wn tenia una forma de poner archivos grandes en github no me acuerdo como era

import requests
import pandas as pd
import streamlit as st

# Lee el archivo CSV de posters
dp = pd.read_csv('Archivos/posters.csv', sep=',')
print(dp.head())  # Muestra las primeras filas para ver el contenido
st.write(dp.head())  # Muestra las primeras filas para ver el contenido

# Extrae las URLs de las imágenes (segunda columna, índice 1)
image_urls = dp.iloc[:, 1]

# Mostrar las primeras 5 imágenes usando Streamlit
for url in image_urls[:5]:  # Tomamos solo las primeras 5 imágenes
# Limitar la cantidad de imágenes mostradas a las primeras 5 para evitar sobrecargar el navegador
for url in image_urls[:5]:  # Solo mostramos las primeras 5 imágenes
    st.image(url)  # Streamlit mostrará la imagen directamente desde la URL

# Función para buscar películas por nombre, género o actor
    return df

# Cargar el archivo CSV de películas (con codificación y manejo de errores)
df = pd.read_csv('Archivos/movies.csv', sep=',', encoding='ISO-8859-1', engine='python', on_bad_lines='skip').fillna(0)
# Usamos `chunksize` para cargar el CSV en partes pequeñas
df_chunks = pd.read_csv('Archivos/movies.csv', sep=',', encoding='ISO-8859-1', engine='python', on_bad_lines='skip', chunksize=5000)
# Leer solo el primer chunk para evitar sobrecargar el servidor
df = next(df_chunks).fillna(0)

# Entrada del usuario para buscar una película
pelicula_buscar = st.text_input('Buscar película por nombre:')
# Filtrar el DataFrame basado en los criterios de búsqueda
sapa = buscar_pelicula(df, nombre=pelicula_buscar, genero=genero_buscar, actor=actor_buscar)

# Mostrar los resultados filtrados
# Mostrar los resultados filtrados limitados a las primeras 10 filas
if not sapa.empty:
    st.write(sapa)
    st.write(sapa.head(10))  # Muestra solo las primeras 10 filas para evitar grandes tablas
else:
    st.write("No se encontraron resultados para la búsqueda.")
  st.write('Por favor, escribe una reseña.')

# Mostrar trailers, sinopsis y reseñas promedio (si los tienes en tu CSV)
# Limitar el número de filas para mostrar trailers y reseñas
if 'trailer' in df.columns and 'synopsis' in df.columns and 'average_rating' in df.columns:
    for index, row in sapa.iterrows():
    for index, row in sapa.head(5).iterrows():  # Limitar a las primeras 5 películas
        st.write(f"**Trailer**: {row['trailer']}")
        st.write(f"**Sinopsis**: {row['synopsis']}")
        st.write(f"**Promedio de reseñas**: {row['average_rating']}")
