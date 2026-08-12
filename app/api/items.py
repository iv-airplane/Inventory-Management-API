from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database import get_db
from app.schemas.item import ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["items"])


@router.post("", status_code=201, response_model=ItemRead)
async def add_item(body: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await crud.item.create_item(db, body)


@router.get("", response_model=list[ItemRead])
async def list_items(db: AsyncSession = Depends(get_db)):
    return await crud.item.get_items(db)


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await crud.item.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.patch("/{item_id}/restock", response_model=ItemRead)
async def restock_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await crud.item.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return await crud.item.restock_item(db, item)


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await crud.item.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await crud.item.delete_item(db, item)
