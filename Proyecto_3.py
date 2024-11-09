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
dp = pd.read_csv('posters.csv', sep=',')
# Extrae las URLs de las imágenes (segunda columna, índice 1)
image_urls = dp.iloc[:, 1]
# Limitar la cantidad de imágenes mostradas a las primeras 5 para evitar sobrecargar el navegador

for url in image_urls[:5]:  # Solo mostramos las primeras 5 imágenes
    st.image(url)  # Streamlit mostrará la imagen directamente desde la URL
# Función para buscar películas por nombre, género o actor
def buscar_pelicula(df, nombre=None, genero=None, actor=None):
    if nombre:
        df = df[df['name'].str.contains(nombre, case=False, na=False)]
    if genero:
        df = df[df['genres'].str.contains(genero, case=False, na=False)]
    if actor:
        df = df[df['actors'].str.contains(actor, case=False, na=False)]
    return df
# Cargar el archivo CSV de películas (con codificación y manejo de errores)
# Usamos `chunksize` para cargar el CSV en partes pequeñas
df_chunks = pd.read_csv('movies.csv', sep=',', encoding='ISO-8859-1', engine='python', on_bad_lines='skip', chunksize=5000)
# Leer solo el primer chunk para evitar sobrecargar el servidor
df = next(df_chunks).fillna(0)
# Entrada del usuario para buscar una película
pelicula_buscar = st.text_input('Buscar película por nombre:')
genero_buscar = st.text_input('Buscar por género:')
actor_buscar = st.text_input('Buscar por actor:')
# Filtrar el DataFrame basado en los criterios de búsqueda
sapa = buscar_pelicula(df, nombre=pelicula_buscar, genero=genero_buscar, actor=actor_buscar)
# Función para dejar reseñas (almacena en una lista o archivo)
if st.button('Dejar una reseña'):
    reseña = st.text_area('Escribe tu reseña:')
    if reseña:
        # Aquí puedes almacenar las reseñas, por ejemplo, en un archivo o base de datos
        st.write(f'Reseña guardada: {reseña}')
    else:
        st.write('Por favor, escribe una reseña.')
# Mostrar trailers, sinopsis y reseñas promedio (si los tienes en tu CSV)
# Limitar el número de filas para mostrar trailers y reseñas
if 'trailer' in df.columns and 'synopsis' in df.columns and 'average_rating' in df.columns:
    for index, row in sapa.head(5).iterrows():  # Limitar a las primeras 5 películas
        st.write(f"**Trailer**: {row['trailer']}")
        st.write(f"**Sinopsis**: {row['synopsis']}")
        st.write(f"**Promedio de reseñas**: {row['average_rating']}")
