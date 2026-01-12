from typing import Sequence

from fastapi import APIRouter
from sqlalchemy import select

from app.api.deps import SessionDep
from app.core.models.models import MissionModel, TargetModel, SpyCatModel
from app.core.schemas.mission_schemas import (
    TargetUpdateSchema,
    MissionCreateSchema,
    MissionModelResponse,
    MissionResponse
)


def map_model_response(model: MissionModel) -> MissionModelResponse:
    return MissionModelResponse.model_validate(model)


router: APIRouter = APIRouter(
    prefix="/missions",
    tags=["v1.missions"]
)


@router.get(path="", response_model=list[MissionModelResponse])
async def get_missions(session: SessionDep) -> Sequence[MissionModelResponse]:
    return session.execute(select(MissionModel)).scalars().all()


@router.get(path="/{mission_id}")
async def get_mission_by_id(mission_id: int, session: SessionDep) -> MissionModelResponse:
    res = (session.execute(select(MissionModel).where(MissionModel.id == mission_id))
           .scalars()
           .first())
    res2 = (session.execute(select(MissionModel).where(MissionModel.id == mission_id))
            .scalars().one())

    print("===================================")
    print(res)
    print("////////////////////////")
    print(res2)
    print("===================================")
    return res


@router.post(path="", response_model=MissionResponse)
async def create_mission(
        mission_data: MissionCreateSchema,
        session: SessionDep
) -> dict[str, str | MissionModelResponse]:
    new_mission: MissionModel = MissionModel(
        targets=[
            TargetModel(**target.model_dump())
            for target in mission_data.targets
        ]
    )

    session.add(instance=new_mission)
    session.commit()
    session.refresh(instance=new_mission)

    return {
        "message": "New mission was created",
        "data": map_model_response(model=new_mission)
    }


@router.patch(path="/{mission_id}/assign/{cat_id}", response_model=MissionResponse)
async def assign_cat_to_mission(
        mission_id: int,
        cat_id: int,
        session: SessionDep
) -> dict[str, str | MissionModelResponse]:
    mission: MissionModel = session.execute(
        select(MissionModel).where(MissionModel.id == mission_id)
    ).scalars().first()

    cat: SpyCatModel = session.execute(
        select(SpyCatModel).where(SpyCatModel.id == cat_id)
    ).scalars().first()

    mission.assigned_cat_id = cat_id
    cat.is_available = False

    session.commit()
    session.refresh(instance=mission)

    return {
        "message": f"Cat with id {cat_id} was assigned to mission with id {mission_id}",
        "data": map_model_response(model=mission)
    }


@router.patch(path="/{mission_id}/targets/{target_id}", response_model=MissionResponse)
async def update_mission_target_data(
        mission_id: int,
        target_id: int,
        target_data: TargetUpdateSchema,
        session: SessionDep
) -> dict[str, str | MissionModelResponse]:
    mission: MissionModel = session.execute(
        select(MissionModel).where(MissionModel.id == mission_id)
    ).scalars().first()

    target: TargetModel = session.execute(
        select(TargetModel).where(TargetModel.id == target_id)
    ).scalars().first()

    target.notes, target.is_completed = target_data.model_dump().values()

    count_completed = len([target for target in mission.targets if target.is_completed])
    mission.is_completed = count_completed == len(mission.targets)
    mission.assigned_spy_cat.is_available = mission.is_completed

    session.commit()
    session.refresh(instance=mission)

    return {
        "message": f"Mission with id {mission_id} was updated with new target status",
        "data": map_model_response(model=mission)
    }


@router.delete(path="/{mission_id}", response_model=MissionResponse)
async def delete_mission(
        mission_id: int,
        session: SessionDep
) -> dict[str, str | MissionModelResponse]:
    mission: MissionModel = session.execute(
        select(MissionModel).where(MissionModel.id == mission_id)
    ).scalars().first()

    response_data = map_model_response(model=mission)

    session.delete(instance=mission)
    session.commit()

    return {
        "message": f"Mission with id {mission_id} was deleted",
        "data": response_data
    }
