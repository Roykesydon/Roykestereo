import base64
from cgi import test
import hashlib
import os
from flask_cors import CORS
from flask import Blueprint, request, session

# from utils.config import get_config
from utils.validator import Validator
from utils.database import get_connection

user = Blueprint("user", __name__)
CORS(user, supports_credentials=True)


@user.route("/")
def index():
    return "Hello user"


@user.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data["username"]
    nickname = data["nickname"]
    password = data["password"]

    return_json = {"success": 0, "msg": "", "token": ""}

    validator = Validator()
    validator.required([username, nickname, password])
    validator.check_username(username)
    validator.check_nickname(nickname)
    validator.check_password(password)
    errors = validator.get_errors()

    if len(errors) != 0:
        return_json["msg"] = errors[0]
        return return_json

    """
    Get connection with mongodb
    """
    client = get_connection()
    db = client["roykestereo_db"]

    users_collection = db["users"]

    if users_collection.find_one({"username": username}) is not None:
        return_json["msg"] = "username already exists"
        return return_json

    """
    Insert user information into database
    """
    salt = os.urandom(16)
    salt = base64.b64encode(salt)

    password = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 100000
    ).hex()

    data = {
        "username": str(username),
        "nickname": str(nickname),
        "password": str(password),
        "salt": salt.decode("utf-8"),
    }
    users_collection.insert_one(data)

    session["username"] = username
    session.permanent = True

    return_json["success"] = 1
    return_json["data"] = {"username": username, "nickname": nickname}

    return return_json


@user.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = str(data["username"])
    password = str(data["password"])

    return_json = {"success": 0, "msg": "", "token": "", "isAdmin": 0}

    validator = Validator()
    validator.required([username, password])
    validator.check_username(username)
    validator.check_password(password)
    errors = validator.get_errors()

    if len(errors) != 0:
        return_json["msg"] = errors[0]
        return return_json

    """
    Get connection with mongodb
    """
    client = get_connection()
    db = client["roykestereo_db"]

    users_collection = db["users"]

    user_data = users_collection.find_one({"username": username})

    if user_data is None:
        return_json["msg"] = "username doesn't exist"
        return return_json

    """
    Insert user information into database
    """
    salt = user_data["salt"].encode("utf-8")
    user_password_in_db = user_data["password"]
    nickname = user_data["nickname"]

    hash_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 100000
    ).hex()

    if hash_password != user_password_in_db:
        return_json["msg"] = "wrong password"
        return return_json

    session["username"] = username
    session.permanent = True

    return_json["success"] = 1
    return_json["data"] = {
        "username": username,
        "nickname": nickname,
    }

    return return_json
