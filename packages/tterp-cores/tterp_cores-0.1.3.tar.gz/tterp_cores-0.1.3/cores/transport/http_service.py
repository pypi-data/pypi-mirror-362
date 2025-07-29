from typing import Generic, TypeVar

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ValidationError

from cores.interface.index import IUseCase

# Define type variables
Entity = TypeVar("Entity")
CreateDTO = TypeVar("CreateDTO", bound=BaseModel)
UpdateDTO = TypeVar("UpdateDTO", bound=BaseModel)
Cond = TypeVar("Cond", bound=BaseModel)


# Define PagingDTO
class PagingDTO(BaseModel):
    page: int = Query(1, ge=1)
    limit: int = Query(10, ge=1)


# Base HTTP Service
class BaseHttpService(Generic[Entity, CreateDTO, UpdateDTO, Cond]):
    def __init__(self, use_case: IUseCase[CreateDTO, UpdateDTO, Entity, Cond]):
        self.use_case = use_case

    async def create_api(self, data: CreateDTO):
        result = await self.use_case.create(data)
        return {"data": result}

    async def get_detail_api(self, id: str):
        result = await self.use_case.get_detail(id)
        if result is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"data": result}

    async def update_api(self, id: str, data: UpdateDTO):
        result = await self.use_case.update(id, data)
        return {"data": result}

    async def delete_api(self, id: str):
        result = await self.use_case.delete(id)
        return {"data": result}

    async def list_api(self, cond: Cond, paging: PagingDTO = Depends()):
        try:
            result = await self.use_case.list(cond, paging)
            return {
                "data": result,
                "paging": paging.dict(),
                "filter": cond.dict(),
            }
        except ValidationError as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid input: {e.errors()}"
            )


# Example Router Integration
def create_router(service: BaseHttpService):
    router = APIRouter()

    @router.post("/", response_model=dict)
    async def create(data: CreateDTO):
        return await service.create_api(data)

    @router.get("/{id}", response_model=dict)
    async def get_detail(id: str):
        return await service.get_detail_api(id)

    @router.put("/{id}", response_model=dict)
    async def update(id: str, data: UpdateDTO):
        return await service.update_api(id, data)

    @router.delete("/{id}", response_model=dict)
    async def delete(id: str):
        return await service.delete_api(id)

    @router.get("/", response_model=dict)
    async def list(cond: Cond, paging: PagingDTO = Depends()):
        return await service.list_api(cond, paging)

    return router
    return router
