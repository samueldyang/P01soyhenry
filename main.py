from fastapi import FastAPI, Path
from pydantic import BaseModel
import pandas as pd
import ast

app = FastAPI()

df = pd.read_csv("dataset_concatenado.csv")

#definimos la función de recomendación
def recomendacion(titulo: str, df: pd.DataFrame, top_n: int = 5):
    try:
        #obtenemos la lista de géneros de la película de entrada
        genres_str = df[df['title'] == titulo]['genres'].iloc[0]
        input_genres = [g['name'] for g in ast.literal_eval(genres_str)]
    except (IndexError, ValueError, TypeError):
        return {"error": f"No se encontró la película '{titulo}' o el formato de géneros es incorrecto."}

    #calculamos la similitud basada en la cantidad de géneros en común
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

    #ordenamos las películas por la cantidad de géneros en común (descendente)
    similarity_scores.sort(key=lambda item: item[1], reverse=True)

    #devolvemos los nombres de las top_n películas más similares
    recommended_movies = [item[0] for item in similarity_scores[:top_n]]
    return {"recomendaciones": recommended_movies}

#definimos el modelo de datos para la respuesta
class RecomendacionesResponse(BaseModel):
    recomendaciones: list

#definimos la ruta en FastAPI
@app.get("/recomendacion/{titulo}", response_model=RecomendacionesResponse)
async def obtener_recomendaciones(titulo: str = Path(..., description="El título de la película para obtener recomendaciones")):
    return recomendacion(titulo, df)