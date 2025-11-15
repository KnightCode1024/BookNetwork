from fastapi import APIRouter, Depends

from dependencies.auth import get_current_user


router = APIRouter(prefix="/authors", tags=["Author"])


@router.get("/{author_id}/")
def get_author_by_id(user = Depends(get_current_user)):
    return {"message": "ok"}

@router.get("/")
def get_all_authors(user = Depends(get_current_user)):
    return {"message": "ok"}

@router.post("/author/")
def create_author(user = Depends(get_current_user)):
    return {"message": "ok"}

@router.delete("/{id}/")
def delete_author(user = Depends(get_current_user)):
    return {"message": "ok"}

@router.patch("/{id}/")
def partial_update_author(user = Depends(get_current_user)):
    return {"message": "ok"}


@router.put("/{id}/")
def update_author(user = Depends(get_current_user)):
    return {"message": "ok"}