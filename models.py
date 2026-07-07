from pony.orm import Database, Required, Optional, PrimaryKey, Set
from datetime import datetime

db = Database()


class User(db.Entity):
    _table_ = 'tbl_user'
    id = PrimaryKey(int, auto=True)
    nama = Required(str, 100)
    email = Required(str, 150, unique=True)
    password = Required(str, 255)
    phone = Optional(str, 20, default='')
    location = Optional(str, 100, default='')
    bio = Optional(str, 500, default='')
    is_verified = Required(bool, default=False)
    verification_token = Optional(str, 100, default='')
    reset_token = Optional(str, 100, default='')
    reset_token_expiry = Optional(datetime)
    notif_email = Required(bool, default=True)
    dark_mode = Required(bool, default=False)
    save_history = Required(bool, default=True)
    created_at = Required(datetime, default=datetime.now)
    # Relations
    activities = Set('ActivityLog')
    chats = Set('ChatHistory')
    files = Set('UploadedFile')


class ActivityLog(db.Entity):
    _table_ = 'tbl_activity_log'
    id = PrimaryKey(int, auto=True)
    user = Required(User)
    action = Required(str, 255)
    detail = Optional(str, 500, default='')
    created_at = Required(datetime, default=datetime.now)


class ChatHistory(db.Entity):
    _table_ = 'tbl_chat_history'
    id = PrimaryKey(int, auto=True)
    user = Required(User)
    model_name = Required(str, 50)
    prompt = Required(str, 5000)
    response = Required(str, 10000)
    created_at = Required(datetime, default=datetime.now)


class UploadedFile(db.Entity):
    _table_ = 'tbl_uploaded_file'
    id = PrimaryKey(int, auto=True)
    user = Required(User)
    filename = Required(str, 255)
    original_name = Required(str, 255)
    file_type = Required(str, 10)
    file_size = Required(int)
    created_at = Required(datetime, default=datetime.now)
