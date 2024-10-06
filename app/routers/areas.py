# areas.py

from fastapi import APIRouter
from crud import create_area, get_areas, get_area, update_area, delete_area

router = APIRouter()

@router.post("/areas/")
def create_area_route(data: dict):
    area_id = create_area(data)
    return {"id": area_id}

@router.get("/areas/")
def get_areas_route():
    return get_areas()

@router.get("/areas/{area_id}")
def get_area_route(area_id: str):
    return get_area(area_id)

@router.put("/areas/{area_id}")
def update_area_route(area_id: str, data: dict):
    update_area(area_id, data)

@router.delete("/areas/{area_id}")
def delete_area_route(area_id: str):
    delete_area(area_id)
