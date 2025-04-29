from fastapi import FastAPI, Path
from pydantic import BaseModel
import pandas as pd
import ast

app = FastAPI()

try:
    df = pd.read_csv("dataset_concatenado.csv")
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    try:
        df_credits = pd.read_csv("credits.csv")
    except FileNotFoundError:
        df_credits = None
        print("Error: No se encontró el archivo credits.csv. Algunas funciones no estarán disponibles.")
except FileNotFoundError:
    df = None
    df_credits = None
    print("Error: No se encontró el archivo dataset_concatenado.csv. La API no funcionará correctamente.")

# --- Funciones Adicionales ---
def cantidad_filmaciones_mes(mes: str):
    meses_espanol = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    mes_num = meses_espanol.get(mes.lower())
    if mes_num is None:
        return {"mensaje": f"Mes '{mes}' no válido. Debe ser un mes en español."}
    cantidad = len(df[df['release_date'].dt.month == mes_num].dropna(subset=['release_date']))
    return {"mensaje": f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes.capitalize()}"}

def cantidad_filmaciones_dia(dia: str):
    dias_espanol = {
        'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3,
        'viernes': 4, 'sábado': 5, 'domingo': 6
    }
    dia_num = dias_espanol.get(dia.lower())
    if dia_num is None:
        return {"mensaje": f"Día '{dia}' no válido. Debe ser un día de la semana en español."}
    cantidad = len(df[df['release_date'].dt.dayofweek == dia_num].dropna(subset=['release_date']))
    return {"mensaje": f"{cantidad} cantidad de películas fueron estrenadas en los días {dia.capitalize()}"}

def score_titulo(titulo_de_la_filmacion: str):
    if df is None:
        return {"mensaje": "Error: DataFrame no cargado."}
    titulo_busqueda = titulo_de_la_filmacion.lower().strip()
    pelicula = df[df['title'].str.lower().str.strip() == titulo_busqueda]
    if pelicula.empty:
        return {"mensaje": f"No se encontró la película '{titulo_de_la_filmacion}'."}
    titulo = pelicula['title'].iloc[0]
    anio_estreno = pelicula['release_date'].dt.year.iloc[0] if pd.notna(pelicula['release_date'].iloc[0]) else None
    score = pelicula['popularity'].iloc[0]
    return {"mensaje": f"La película '{titulo}' fue estrenada en el año {anio_estreno} con un score de {score}."}

def votos_titulo(titulo_de_la_filmacion: str):
    if df is None:
        return {"mensaje": "Error: DataFrame no cargado."}
    pelicula = df[df['title'].str.lower() == titulo_de_la_filmacion.lower()]
    if pelicula.empty:
        return {"mensaje": f"No se encontró la película '{titulo_de_la_filmacion}'."}
    cantidad_votos = pelicula['vote_count'].iloc[0]
    promedio_votos = pelicula['vote_average'].iloc[0]
    anio_estreno = pelicula['release_date'].dt.year.iloc[0] if pd.notna(pelicula['release_date'].iloc[0]) else None
    if cantidad_votos < 2000:
        return {"mensaje": f"La película '{pelicula['title'].iloc[0]}' no cumple con el mínimo de 2000 valoraciones."}
    return {"mensaje": f"La película '{pelicula['title'].iloc[0]}' fue estrenada en el año {anio_estreno}. La misma cuenta con un total de {cantidad_votos} valoraciones, con un promedio de {promedio_votos}."}

def get_actor(nombre_actor: str):
    if df_credits is None or df is None:
        return {"mensaje": "Error: DataFrames 'df' o 'df_credits' no cargados."}
    peliculas_actor = df_credits[df_credits['name'].str.lower() == nombre_actor.lower()]
    if peliculas_actor.empty:
        return {"mensaje": f"No se encontró al actor '{nombre_actor}' o no tiene películas en el dataset."}
    ids_peliculas_actor = peliculas_actor['id'].unique().tolist()
    peliculas_actor_movies = df[df['id'].isin(ids_peliculas_actor)].copy()
    retorno_promedio = peliculas_actor_movies['return'].mean() if not peliculas_actor_movies.empty else 0
    retorno_total = peliculas_actor_movies['return'].sum() if not peliculas_actor_movies.empty else 0
    return {
        "mensaje": f"El actor {nombre_actor.capitalize()} ha participado de {len(peliculas_actor_movies)} cantidad de filmaciones, el mismo ha conseguido un retorno de {retorno_total} con un promedio de {retorno_promedio:.2f} por filmación."
    }

def get_director(nombre_director: str):
    if df_credits is None or df is None:
        return {"mensaje": "Error: DataFrames 'df' o 'df_credits' no cargados."}
    peliculas_director = df_credits[(df_credits['job'] == 'Director') & (df_credits['name'].str.lower() == nombre_director.lower())]
    if peliculas_director.empty:
        return {"mensaje": f"No se encontró al director '{nombre_director}' o no tiene películas en el dataset."}
    ids_peliculas_director = peliculas_director['movie_id'].tolist()
    peliculas_director_movies = df[df['id'].isin(ids_peliculas_director)].copy()
    peliculas_director_movies['release_date'] = pd.to_datetime(peliculas_director_movies['release_date'], errors='coerce')
    retorno_promedio = peliculas_director_movies['return'].mean() if not peliculas_director_movies.empty else 0
    retorno_total = peliculas_director_movies['return'].sum() if not peliculas_director_movies.empty else 0
    lista_peliculas = []
    for index, row in peliculas_director_movies.iterrows():
        lista_peliculas.append({
            "titulo": row["title"],
            "fecha_lanzamiento": row["release_date"].strftime("%Y-%m-%d") if pd.notna(row['release_date']) else None,
            "retorno_individual": row["return"],
            "costo": row["budget"],
            "ganancia": row["revenue"]
        })
    return {
        "mensaje": f"El director {nombre_director.capitalize()} ha dirigido {len(peliculas_director_movies)} cantidad de filmaciones, el mismo ha conseguido un retorno de {retorno_total} con un promedio de {retorno_promedio:.2f} por filmación.",
        "peliculas": lista_peliculas
    }

# --- Sistema de Recomendación ---
def recomendacion(titulo: str, df: pd.DataFrame, top_n: int = 5):
    if df is None or 'genres' not in df.columns or 'title' not in df.columns:
        return {"error": "El sistema de recomendación no está inicializado correctamente."}
    try:
        genres_str = df[df['title'] == titulo]['genres'].iloc[0]
        input_genres = [g['name'] for g in ast.literal_eval(genres_str)]
    except (IndexError, ValueError, TypeError):
        return {"error": f"No se encontró la película '{titulo}' o el formato de géneros es incorrecto."}
    similarity_scores = []
    for index, row in df.iterrows():
        if row['title'] == titulo:
            continue
        try:
            other_genres_str = row['genres']
            other_genres = [g['name'] for g in ast.literal_eval(other_genres_str)]
            common_genres = len(set(input_genres) & set(other_genres))
            similarity_scores.append((row['title'], common_genres))
        except (ValueError, TypeError):
            continue
    similarity_scores.sort(key=lambda item: item[1], reverse=True)
    recommended_movies = [item[0] for item in similarity_scores[:top_n]]
    return {"recomendaciones": recommended_movies}

class RecomendacionesResponse(BaseModel):
    recomendaciones: list

# --- Rutas en FastAPI ---
@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API de Películas!"}

@app.get("/cantidad_filmaciones_mes/{mes}")
async def get_cantidad_filmaciones_mes(mes: str = Path(..., description="Mes en español (ej: enero)")):
    return cantidad_filmaciones_mes(mes)

@app.get("/cantidad_filmaciones_dia/{dia}")
async def get_cantidad_filmaciones_dia(dia: str = Path(..., description="Día de la semana en español (ej: lunes)")):
    return cantidad_filmaciones_dia(dia)

@app.get("/score_titulo/{titulo_de_la_filmacion}")
async def get_score_titulo(titulo_de_la_filmacion: str = Path(..., description="Título de la filmación")):
    return score_titulo(titulo_de_la_filmacion)

@app.get("/votos_titulo/{titulo_de_la_filmacion}")
async def get_votos_titulo(titulo_de_la_filmacion: str = Path(..., description="Título de la filmación")):
    return votos_titulo(titulo_de_la_filmacion)

@app.get("/get_actor/{nombre_actor}")
async def get_actor_endpoint(nombre_actor: str = Path(..., description="Nombre del actor")):
    return get_actor(nombre_actor)

@app.get("/get_director/{nombre_director}")
async def get_director_endpoint(nombre_director: str = Path(..., description="Nombre del director")):
    return get_director(nombre_director)

@app.get("/recomendacion/{titulo}", response_model=RecomendacionesResponse)
async def obtener_recomendaciones(titulo: str = Path(..., description="El título de la película para obtener recomendaciones")):
    return recomendacion(titulo, df)
