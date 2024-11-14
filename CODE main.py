# Archivos/Main.py

import streamlit as st
import pandas as pd




def main():
    st.title("Página Principal: Buscando Películas")
    #chunksize=621529

    # Cargar los CSV y mostrar las películas disponibles
    dp_chunks = pd.read_csv('Archivos/posters.csv', sep=',', encoding='ISO-8859-1', engine='python', on_bad_lines='skip', chunksize=500)
    dp = next(dp_chunks).fillna(0)

    dm_chunks = pd.read_csv('Archivos/movies.csv', sep=',', encoding='ISO-8859-1', engine='python', on_bad_lines='skip', chunksize=500)
    dm = next(dm_chunks).fillna(0)

    da_chunks = pd.read_csv('Archivos/actors.csv', sep=',', encoding='ISO-8859-1', engine='python', on_bad_lines='skip', chunksize=500)
    da = next(da_chunks).fillna(0)

    dg_chunks = pd.read_csv('Archivos/genres.csv', sep=',', encoding='ISO-8859-1', engine='python', on_bad_lines='skip', chunksize=500)
    dg = next(dg_chunks).fillna(0)

    # Crear una lista de nombres de películas para que el usuario elija
    movie_names = dm['name'].unique()
    movie_selected = st.selectbox("Selecciona una película", movie_names)

    if movie_selected:
        # Buscar los datos relacionados con la película seleccionada
        movie_id = dm[dm['name'] == movie_selected]['id'].values[0]

        # Buscar géneros, actores y la URL del poster para esta película
        movie_genres = dg[dg['id'] == movie_id]['genre'].unique()
        movie_actors = da[da['id'] == movie_id]['name'].unique()
        movie_poster_url = dp[dp['id'] == movie_id]['link'].values[0]

        # Guardar todos los datos seleccionados en session_state para usarlos en la página personal
        st.session_state.selected_movie = {
            'name': movie_selected,
            'id': movie_id,
            'genres': ', '.join(movie_genres),
            'actors': ', '.join(movie_actors),
            'poster_url': movie_poster_url
        }
    
    st.write('Dale dos click al boton despues de sleccionar la pelicula: ')
    # Crear botones para cambiar a la página personal
    if st.button("Buscar"):
        st.session_state.page = "Personal"  # Cambiar a la página personal

#ORDENAR PELICULAS POR GENERO    

    #Df con solo los generos
    name_genre = dg["genre"].unique()

    #Selector de generos
    genre_selection = st.sidebar.selectbox("Seleccione un género", ["Seleccione un género"] + list(name_genre))

    #Mostrar las peliculas del genero especificio
    if genre_selection != "Seleccione un género":  
        genero_movies = dg[dg["genre"] == genre_selection]["id"].unique()
        filtrar_movies = dm[dm["id"].isin(genero_movies)]
        top30 = filtrar_movies.sort_values(by="rating", ascending=False).head(30)

        st.write(f"### Top 30 películas de {genre_selection}")

        #Esto es para las flechas 
        col1, col2 = st.columns([17, 1])  #Ajustar las flechas

        #Boton para atras
        with col1:
            if st.session_state.movie_index > 0: #solo funciona si estas de la 5 pal alante
                if st.button("←", use_container_width=False, key="boton izquierda 1"):  # Flecha hacia la izquierda
                    st.session_state.movie_index -= 5  #retroceder 5

        #Boton spara avanzar 
        with col2:
            if st.session_state.movie_index < len(top30 ) - 5: #solo funciona si estas de la 25 pa atras
                if st.button("→", use_container_width=False, key="boton derecha 1"):  # Flecha hacia la derecha
                    st.session_state.movie_index += 5  # Avanzar 5 películas

        # Seleccionar las 5 películas actuales basadas en el índice
        selected_movies = top30 .iloc[st.session_state.movie_index:st.session_state.movie_index + 5]

        #Estos son las columanas de las imagenes de la pelicula
        columns = st.columns(5)  
        # Mostrar las imágenes y los nombres de las películas
        for index, (col, row) in enumerate(zip(columns, selected_movies.iterrows())):
            movie_name = row[1]["name"]
            movie_poster_url = dp[dp["id"] == row[1]["id"]]["link"].values
            #Esto es para enumerar las peliculas al presionar el botno sin problemas
            Numeracion =  movie_index_text = f"{st.session_state.movie_index + index + 1}.- {movie_name}"

            # Mostrar la imagen en la columna respectiva
            if len(movie_poster_url) > 0:
                col.image(movie_poster_url[0], width=250)  # Mostrar la imagen
            else:
                col.write("Póster no disponible")

            # Mostrar el nombre de la película como un botón
            movie_id = row[1]["id"]

            boton_key = f"movie_button_{movie_id}_{index}"
            
            col.button(Numeracion, key = boton_key)
            #if col.button(f"**{movie_name}**"):
             #Pones la info post presionar botton
                   
            st.write("") #Esto esta para generar mas espacio cuando aparezca con el de los años

#ORDENAR PELICULAS EN FILTRO DE AÑOS 

    # Años de cada pelicula
    years = dm['date'].unique()

    # Slider con rango de años
    year_range = st.sidebar.slider(
        'Selecciona un rango de años',
        min_value=min(years),  
        max_value=max(years),  
        value=(min(years), max(years)),  #Rango
        step=1
    )

    # Filtrar las películas dentro del rango seleccionado
    filtered_movies = dm[(dm['date'] >= year_range[0]) & (dm['date'] <= year_range[1])]
    top30_years = filtered_movies.sort_values(by="rating", ascending=False).head(30)

    #Caso de que no hayan peliculas en el rango
    if filtered_movies.empty:
        st.write(f"No hay películas disponibles para el rango de años {year_range[0]} - {year_range[1]}.")
    else:
        st.write(f"### Mejores 30 Películas del año {year_range[0]} hasta {year_range[1]}:")

        # IDS de las peliculas del rango
        movie_ids = filtered_movies['id'].unique()

        # Filtrar el df por esos ids
        filtered_details = dm[dm['id'].isin(movie_ids)]

        # Inicializamos la variable de estado para las películas si no existe
        if "movie_index" not in st.session_state:
            st.session_state.movie_index = 0  # Comenzamos desde la primera película

       #Esto es para las flechas 
        col1, col2 = st.columns([17, 1])  

        #Boton atnerior
        with col1:
            if st.session_state.movie_index > 0:
                if st.button("←", use_container_width=False, key="boton izquierda"):  
                    st.session_state.movie_index -= 5  

        #Boton siguiente
        with col2:
            if st.session_state.movie_index < len(top30_years) - 5:
                if st.button("→", use_container_width=False,key="boton derecha"): 
                    st.session_state.movie_index += 5  

        #Mostrar las 5 mejores peliculas
        selected_movies = top30_years.iloc[st.session_state.movie_index:st.session_state.movie_index + 5]

        #Estos son las columanas de las imagenes de la pelicula
        columns = st.columns(5)  
        
        for index, (col, row) in enumerate(zip(columns, selected_movies.iterrows())):
            movie_name = row[1]["name"]
            movie_poster_url = dp[dp["id"] == row[1]["id"]]["link"].values
            Numeracion =  movie_index_text = f"{st.session_state.movie_index + index + 1}.- {movie_name}"
           
            if len(movie_poster_url) > 0:
                col.image(movie_poster_url[0], width=250)  
            else:
                col.write("Póster no disponible")

            movie_id = row[1]["id"]
            button_key = f"movie_button_{index}"
        
            if col.button(Numeracion, key= button_key): 
                # Aquí puedes agregar cualquier lógica que necesites cuando se presione el botón
                st.write("agregar info de la pelicula con una funcion")
