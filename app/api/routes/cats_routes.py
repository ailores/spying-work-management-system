from typing import Any, Sequence

from fastapi import APIRouter
from sqlalchemy import select

from app.api.deps import SessionDep
from app.core.models import SpyCatModel
from app.core.schemas.cat_schemas import SpyCatSchema, SpyCatUpdate, SpyCatResponse, SpyCatModelResponse


def map_model_response(model: SpyCatModel) -> SpyCatModelResponse:
    return SpyCatModelResponse.model_validate(model)


router: APIRouter = APIRouter(
    prefix="/cats",
    tags=["v1.cats"]
)


@router.get(path="", response_model=list[SpyCatModelResponse])
async def get_cats(session: SessionDep) -> Sequence[Any]:
    return session.execute(select(SpyCatModel)).scalars().all()


@router.get(path="/{cat_id}", response_model=SpyCatModelResponse)
async def get_cat_by_id(cat_id: str, session: SessionDep) -> SpyCatModelResponse:
    return (session.execute(select(SpyCatModel).where(SpyCatModel.id == cat_id))
            .scalars()
            .first())


@router.post(path="", response_model=SpyCatResponse)
async def create_cat(cat_data: SpyCatSchema, session: SessionDep) -> dict[str, str | SpyCatModelResponse]:
    new_cat: SpyCatModel = SpyCatModel(**cat_data.model_dump())
    session.add(instance=new_cat)
    session.commit()
    session.refresh(instance=new_cat)
    return {
        "message": "New cat was created",
        "data": map_model_response(model=new_cat)
    }


@router.delete(path="/{cat_id}", response_model=SpyCatResponse)
async def delete_cat(cat_id: int, session: SessionDep) -> dict[str, str | SpyCatModelResponse]:
    cat: SpyCatModel = session.execute(select(SpyCatModel).where(SpyCatModel.id == cat_id)).scalars().first()
    session.delete(instance=cat)
    session.commit()
    return {
        "message": f"Cat with id {cat_id} was deleted",
        "data": map_model_response(model=cat)
    }


@router.put(path="/{cat_id}", response_model=SpyCatResponse)
async def update_cat(cat_id: int, cat_data: SpyCatUpdate, session: SessionDep) -> dict[str, str | SpyCatModelResponse]:
    cat: SpyCatModel = session.execute(select(SpyCatModel).where(SpyCatModel.id == cat_id)).scalars().first()
    cat.salary = cat_data.salary
    session.commit()
    return {
        "message": f"Cat with id {cat_id} was updated with new {cat_data}",
        "data": map_model_response(model=cat)
    }
