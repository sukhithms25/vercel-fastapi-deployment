from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import ItemModel, ItemCreate, ItemUpdate, ItemResponse
from app.database import get_db

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(data: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item."""
    item = ItemModel(name=data.name, description=data.description, price=data.price)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/", response_model=list[ItemResponse])
async def list_items(db: Session = Depends(get_db)):
    """List all items."""
    return db.query(ItemModel).order_by(ItemModel.id).all()


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a single item by ID."""
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, data: ItemUpdate, db: Session = Depends(get_db)):
    """Update an existing item."""
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item by ID."""
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
