from __future__ import annotations

from typing import Union

from fastapi import APIRouter, UploadFile
from starlette.requests import Request
from starlette.responses import FileResponse

from apps.permissions import IsAdminPermission
from core import settings
from core.permissions import permissions

router = APIRouter(prefix="/api")


@router.get("/test/")
@permissions([IsAdminPermission])
async def test(request: Request) -> dict:
    print(request.user)
    return {"success": True}


@router.post("/upload/")
async def upload_file(file: UploadFile, request: Request) -> dict:
    with open(f"{settings.STATIC_ROOT}{file.filename}", "wb") as destination:
        destination.write(file.file.read())
    return {"success": True}


@router.get("/download/")
async def download_file(request: Request):
    filename = request.query_params.get("name")
    if not filename:
        return {"message": "No filename provided", "success": False}
    try:
        return FileResponse(f"{settings.STATIC_ROOT}{filename}")
    except:
        return {"message": "File not found", "success": False}
