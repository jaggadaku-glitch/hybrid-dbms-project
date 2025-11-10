from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from db import SessionLocal, engine
import models
from decision import should_store_in_mongo
import config
from pymongo import MongoClient
import json, uuid
from sqlalchemy import text

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hybrid MySQL+Mongo Demo")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

mongo_client = MongoClient(config.MONGO_URI)
mongo_db = mongo_client[config.MONGO_DB]
mongo_col = mongo_db[config.MONGO_COLLECTION]

class ItemOut(BaseModel):
    id: str
    title: Optional[str]
    data: Optional[dict]
    text: Optional[str]
    mongo_doc_id: Optional[str]

@app.post("/items", response_model=ItemOut)
async def create_item(title: Optional[str] = Form(None),
                      text: Optional[str] = Form(None),
                      data_json: Optional[str] = Form('{}'),
                      file: Optional[UploadFile] = File(None)):
    data = json.loads(data_json or "{}")
    payload = {'title': title, 'text': text, 'data': data, 'has_file': bool(file)}
    store_in_mongo = should_store_in_mongo(payload)
    new_id = str(uuid.uuid4())
    mongo_id = None
    structured_json_value = None if store_in_mongo else data
    insert_sql = text("INSERT INTO records (id, title, structured_json, mongo_doc_id) VALUES (:id, :title, :structured, :mongo_id)")
    with SessionLocal() as db:
        db.execute(insert_sql, {"id": new_id, "title": title, "structured": structured_json_value, "mongo_id": None})
        db.commit()
    if store_in_mongo:
        doc = {"title": title, "data": data, "text": text}
        if file:
            content = await file.read()
            doc["file_name"] = file.filename
            doc["file_bytes_hex"] = content.hex()
        res = mongo_col.insert_one(doc)
        mongo_id = str(res.inserted_id)
        with SessionLocal() as db:
            update_sql = text("UPDATE records SET mongo_doc_id = :mongo_id WHERE id = :id")
            db.execute(update_sql, {"mongo_id": mongo_id, "id": new_id})
            db.commit()
    return ItemOut(id=new_id, title=title, data=(None if store_in_mongo else data), text=text, mongo_doc_id=mongo_id)

@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: str):
    select_sql = text("SELECT id, title, structured_json, mongo_doc_id FROM records WHERE id = :id")
    with SessionLocal() as db:
        row = db.execute(select_sql, {"id": item_id}).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Not found")
        id_, title, structured_json, mongo_doc_id = row
    data = structured_json
    text = None
    if mongo_doc_id:
        from bson.objectid import ObjectId
        doc = mongo_col.find_one({"_id": ObjectId(mongo_doc_id)})
        if doc:
            data = doc.get("data")
            text = doc.get("text")
    return ItemOut(id=str(id_), title=title, data=data, text=text, mongo_doc_id=mongo_doc_id)
