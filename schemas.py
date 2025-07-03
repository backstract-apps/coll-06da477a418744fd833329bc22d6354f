from pydantic import BaseModel,Field,field_validator

import datetime

import uuid

from typing import Any, Dict, List,Optional,Tuple

import re

class Todos(BaseModel):
    id: int
    description: str
    user_id: int


class ReadTodos(BaseModel):
    id: int
    description: str
    user_id: int
    class Config:
        from_attributes = True


class Users(BaseModel):
    id: int
    username: str


class ReadUsers(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True


