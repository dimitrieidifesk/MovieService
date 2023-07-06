from http import HTTPStatus
from typing import Dict, List, Optional
from uuid import UUID

from core.config import CommonQueryParams
from fastapi import APIRouter, Depends, HTTPException, Request
from models.movie import Movie, MovieDetail
from services.movie_service import MovieService, get_movie_service

router = APIRouter()


@router.get(
    "",
    response_model=List[Movie],
    response_description="Cписок фильмов, собранных парсером",
    summary="Список фильмов",
    description="Список фильмов с пагинацией, " "сортировкой по рейтингу.",
)
async def get_movies(
    movie_service: MovieService = Depends(get_movie_service),
    sort: str = "-rating",
    commons: CommonQueryParams = Depends(CommonQueryParams),
) -> Optional[List[Dict[str, Movie]]]:
    movies = await movie_service.get_data_list(
        sort, commons.page_number, commons.page_size
    )
    if not movies:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films Not Found")
    return [
        Movie(
            id=movie["id"],
            title=movie["title"],
            rating=movie["rating"],
        )
        for movie in movies
    ]


@router.get(
    "/info/{movie_id}",
    response_model=MovieDetail,
    response_description="Подробная информация по фильму",
    summary="Поиск фильма по ID",
    description="Подробная информация по фильму",
)
async def movie_info(
    movie_id: UUID,
    movie_service: MovieService = Depends(get_movie_service),
) -> Optional[Dict[str, Movie]]:
    movie = await movie_service.get_data_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films Not Found")
    return MovieDetail(
        id=movie["id"],
        title=movie["title"],
        type=movie["type"],
        rating=movie["rating"],
        description=movie["description"],
    )


@router.get(
    "/search",
    response_model=List[Movie],
    description="Полнотекстовый поиск по фильмам",
    summary="Список найденных фильмов",
)
async def search_films(
    movie_service: MovieService = Depends(get_movie_service),
    query: str = "",
    commons: CommonQueryParams = Depends(CommonQueryParams),
) -> Optional[List[Dict[str, Movie]]]:
    movies = await movie_service.search_movie(
        query, commons.page_number, commons.page_size
    )
    if not movies:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films Not Found")
    return [
        Movie(
            id=movie["id"],
            title=movie["title"],
            rating=movie["rating"],
        )
        for movie in movies
    ]
