from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.schemas.item import ItemCreate


async def create_item(db: AsyncSession, item_in: ItemCreate) -> Item:
    item = Item(**item_in.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def get_items(db: AsyncSession) -> list[Item]:
    result = await db.execute(select(Item))
    return list(result.scalars().all())


async def get_item(db: AsyncSession, item_id: int) -> Item | None:
    return await db.get(Item, item_id)


async def restock_item(db: AsyncSession, item: Item) -> Item:
    item.in_stock = True
    await db.commit()
    await db.refresh(item)
    return item


async def delete_item(db: AsyncSession, item: Item) -> None:
    await db.delete(item)
    await db.commit()
