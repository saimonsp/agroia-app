# app/crud.py
from app.db.database import get_db
from app.db.database import db

async def create_item(collection_name, item_data):
    collection = db[collection_name]
    result = await collection.insert_one(item_data)
    return result.inserted_id

async def get_item(collection_name, item_id):
    collection = db[collection_name]
    item = await collection.find_one({"_id": item_id})
    return item

async def update_item(collection_name, item_id, item_data):
    collection = db[collection_name]
    result = await collection.update_one({"_id": item_id}, {"$set": item_data})
    return result.modified_count

async def delete_item(collection_name, item_id):
    collection = db[collection_name]
    result = await collection.delete_one({"_id": item_id})
    return result.deleted_count
