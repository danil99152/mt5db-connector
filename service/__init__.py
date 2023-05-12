# from fastapi import FastAPI
# from sqlalchemy import create_engine, Column, Integer, String, event
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# app = FastAPI()
#
# # SQLAlchemy configuration
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
#
# # Define a database model
# class Item(Base):
#     __tablename__ = "items"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#
# # Create the database tables
# Base.metadata.create_all(bind=engine)
#
# # Define a function to handle the after_insert event
# def handle_after_insert(mapper, connection, target):
#     print("New row inserted with id:", target.id)
#
# # Register the after_insert event for the Item model
# event.listen(Item, "after_insert", handle_after_insert)
#
# # Define a function to add new items to the database
# @app.post("/items")
# async def create_item(name: str):
#     db = SessionLocal()
#     try:
#         item = Item(name=name)
#         db.add(item)
#         db.commit()
#         return {"id": item.id, "name": item.name}
#     finally:
#         db.close()