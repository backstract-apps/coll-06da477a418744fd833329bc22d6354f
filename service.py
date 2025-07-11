from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3
import jwt
import datetime
import requests
from pathlib import Path


async def get_todos(db: Session):

    query = db.query(models.Todos)

    todos_all = query.all()
    todos_all = (
        [new_data.to_dict() for new_data in todos_all] if todos_all else todos_all
    )
    res = {
        "todos_all": todos_all,
    }
    return res


async def get_todos_id(db: Session, id: int):

    query = db.query(models.Todos)
    query = query.filter(and_(models.Todos.id == id))

    todos_one = query.first()

    todos_one = (
        (todos_one.to_dict() if hasattr(todos_one, "to_dict") else vars(todos_one))
        if todos_one
        else todos_one
    )

    res = {
        "todos_one": todos_one,
    }
    return res


async def post_todos(db: Session, id: int, description: str, user_id: int):

    record_to_be_added = {"id": id, "user_id": user_id, "description": description}
    new_todos = models.Todos(**record_to_be_added)
    db.add(new_todos)
    db.commit()
    db.refresh(new_todos)
    todos_inserted_record = new_todos.to_dict()

    res = {
        "todos_inserted_record": todos_inserted_record,
    }
    return res


async def put_todos_id(db: Session, id: int, description: str, user_id: int):

    query = db.query(models.Todos)
    query = query.filter(and_(models.Todos.id == id))
    todos_edited_record = query.first()

    if todos_edited_record:
        for key, value in {
            "id": id,
            "user_id": user_id,
            "description": description,
        }.items():
            setattr(todos_edited_record, key, value)

        db.commit()
        db.refresh(todos_edited_record)

        todos_edited_record = (
            todos_edited_record.to_dict()
            if hasattr(todos_edited_record, "to_dict")
            else vars(todos_edited_record)
        )
    res = {
        "todos_edited_record": todos_edited_record,
    }
    return res


async def delete_todos_id(db: Session, id: int):

    query = db.query(models.Todos)
    query = query.filter(and_(models.Todos.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        todos_deleted = record_to_delete.to_dict()
    else:
        todos_deleted = record_to_delete
    res = {
        "todos_deleted": todos_deleted,
    }
    return res


async def get_users(db: Session):

    query = db.query(models.Users)

    users_all = query.all()
    users_all = (
        [new_data.to_dict() for new_data in users_all] if users_all else users_all
    )
    res = {
        "users_all": users_all,
    }
    return res


async def get_users_id(db: Session, id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))

    users_one = query.first()

    users_one = (
        (users_one.to_dict() if hasattr(users_one, "to_dict") else vars(users_one))
        if users_one
        else users_one
    )

    res = {
        "users_one": users_one,
    }
    return res


async def post_users(db: Session, id: int, username: str):

    record_to_be_added = {"id": id, "username": username}
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    users_inserted_record = new_users.to_dict()

    res = {
        "users_inserted_record": users_inserted_record,
    }
    return res


async def put_users_id(db: Session, id: int, username: str):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))
    users_edited_record = query.first()

    if users_edited_record:
        for key, value in {"id": id, "username": username}.items():
            setattr(users_edited_record, key, value)

        db.commit()
        db.refresh(users_edited_record)

        users_edited_record = (
            users_edited_record.to_dict()
            if hasattr(users_edited_record, "to_dict")
            else vars(users_edited_record)
        )
    res = {
        "users_edited_record": users_edited_record,
    }
    return res


async def delete_users_id(db: Session, id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        users_deleted = record_to_delete.to_dict()
    else:
        users_deleted = record_to_delete
    res = {
        "users_deleted": users_deleted,
    }
    return res


async def post_join(db: Session):

    todo_alias = aliased(models.Todos)
    query = db.query(models.Users, todo_alias)

    query = query.join(todo_alias, and_(models.Users.id == todo_alias.user_id))

    query = query.order_by(models.Users.id.asc())

    join_list = query.all()
    join_list = (
        [
            {
                "join_list_1": s1.to_dict() if hasattr(s1, "to_dict") else s1.__dict__,
                "join_list_2": s2.to_dict() if hasattr(s2, "to_dict") else s2.__dict__,
            }
            for s1, s2 in join_list
        ]
        if join_list
        else join_list
    )
    res = {
        "join_list": join_list,
    }
    return res
