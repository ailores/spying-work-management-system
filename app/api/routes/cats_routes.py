from typing import Sequence

import httpx
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from starlette import status

from app.api.deps import SessionDep
from app.config.config import settings
from app.core.models.models import SpyCatModel
from app.core.schemas.cat_schemas import SpyCatCreateSchema, SpyCatUpdate, SpyCatResponse, SpyCatModelResponse


def map_model_response(model: SpyCatModel) -> SpyCatModelResponse:
    return SpyCatModelResponse.model_validate(model)


router: APIRouter = APIRouter(
    prefix="/cats",
    tags=["v1.cats"]
)


@router.get(
    path="",
    response_model=list[SpyCatModelResponse],
    status_code=status.HTTP_200_OK
)
async def get_cats(session: SessionDep) -> Sequence[SpyCatModelResponse]:
    return session.execute(select(SpyCatModel)).scalars().all()


@router.get(
    path="/{cat_id}",
    response_model=SpyCatModelResponse,
    status_code=status.HTTP_200_OK
)
async def get_cat_by_id(cat_id: str, session: SessionDep) -> SpyCatModelResponse:
    cat = session.execute(
        select(SpyCatModel).where(SpyCatModel.id == cat_id)
    ).scalars().first()

    if cat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cat not found"
        )

    return cat


@router.post(
    path="",
    response_model=SpyCatResponse,
    status_code=status.HTTP_201_CREATED)
async def create_cat(
        cat_data: SpyCatCreateSchema,
        session: SessionDep
) -> dict[str, str | SpyCatModelResponse]:
    breeds = httpx.get(settings.CATS_BREEDS_API_URL).json()
    breeds_name_list = [breed["name"].lower() for breed in breeds]

    if not cat_data.breed.lower() in breeds_name_list:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Breed name not valid"
        )

    new_cat: SpyCatModel = SpyCatModel(**cat_data.model_dump())

    session.add(instance=new_cat)
    session.commit()
    session.refresh(instance=new_cat)

    return {
        "message": "New cat was created",
        "data": map_model_response(model=new_cat)
    }


@router.delete(
    path="/{cat_id}",
    response_model=SpyCatResponse,
    status_code=status.HTTP_200_OK
)
async def delete_cat(
        cat_id: int,
        session: SessionDep
) -> dict[str, str | SpyCatModelResponse]:
    cat: SpyCatModel = session.execute(
        select(SpyCatModel).where(SpyCatModel.id == cat_id)
    ).scalars().first()

    if cat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cat not found"
        )

    session.delete(instance=cat)
    session.commit()
    return {
        "message": f"Cat with id {cat_id} was deleted",
        "data": map_model_response(model=cat)
    }


@router.patch(
    path="/{cat_id}",
    response_model=SpyCatResponse,
    status_code=status.HTTP_200_OK
)
async def update_cat(
        cat_id: int,
        cat_data: SpyCatUpdate,
        session: SessionDep
) -> dict[str, str | SpyCatModelResponse]:
    cat: SpyCatModel = session.execute(
        select(SpyCatModel).where(SpyCatModel.id == cat_id)
    ).scalars().first()

    if cat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cat not found"
        )

    cat.salary = cat_data.salary
    session.commit()
    return {
        "message": f"Cat with id {cat_id} was updated with new {cat_data}",
        "data": map_model_response(model=cat)
    }
