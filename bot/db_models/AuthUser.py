from orm import Model, String, Integer, DateTime, Float, Boolean
from objects.globals import db, metadata

from datetime import datetime as dt

class AuthUser(Model):

    __tablename__ = "wgb_authuser"
    __database__ = db
    __metadata__ = metadata

    id = Integer(primary_key=True)
    password = String(max_length=128)
    user_id = Integer()
    is_superuser = Boolean(default=False)
    username = String(max_length=150)
    last_name = String(max_length=150)
    email = String(max_length=255, default=None)
    is_staff = Boolean(default=False)
    is_active = Boolean(default=False)
    date_joined = DateTime(default=dt.now())
    first_name = String(max_length=150)
    balance = Float(default=0.0)