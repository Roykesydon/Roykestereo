import base64
from cgi import test
import hashlib
import os
from flask_cors import CORS
from flask import Blueprint, request, session
from bson import ObjectId


# from utils.config import get_config
from utils.validator import Validator
from utils.database import get_connection

user = Blueprint("user", __name__)
CORS(user, supports_credentials=True)


@user.route("/sign_out", methods=["POST"])
def sign_out():
    return_json = {"success": 0, "msg": ""}
    session.pop("username", None)
    return_json["success"] = 1
    return return_json


@user.route("/nickname")
def get_nickname():
    return_json = {"success": 0, "msg": "", "data": []}
    username = request.args.get("username", default=None, type=str)

    if username is None:
        return_json["msg"] = "please fill username in args"

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

    return_json["success"] = True
    return_json["data"] = user_data["nickname"]

    return return_json


@user.route("/favorite_list")
def get_favorite_list():
    return_json = {"success": 0, "msg": "", "data": []}

    username = session.get("username")
    if username is None:
        return_json["msg"] = "authentication failed\ntry login again"
        return return_json

    """
    Get connection with mongodb
    """
    client = get_connection()
    db = client["roykestereo_db"]

    users_collection = db["users"]

    user_data = users_collection.find_one({"username": username})
    favorite_list = user_data.get("favorite_list")
    if favorite_list is None:
        favorite_list = []

    return_json["success"] = 1
    return_json["data"] = favorite_list

    return return_json


@user.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data["username"]
    nickname = data["nickname"]
    password = data["password"]

    return_json = {"success": 0, "msg": ""}

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

    return_json = {"success": 0, "msg": ""}

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


@user.route("/update_favorite_music", methods=["POST"])
def update_favorite_song():
    data = request.get_json()
    update_method = str(data["method"])  # remove, add
    music_id = str(data["music_id"])

    return_json = {"success": 0, "msg": ""}

    username = session.get("username")
    if username is None:
        return_json["msg"] = "authentication failed\ntry login again"
        return return_json

    """
    Get connection with mongodb
    """
    client = get_connection()
    db = client["roykestereo_db"]

    users_collection = db["users"]

    user_data = users_collection.find_one({"username": username})

    favorite_list = user_data.get("favorite_list")

    if favorite_list is None:
        favorite_list = []

    favorite_list = set(favorite_list)

    if update_method == "remove":
        favorite_list.discard(music_id)

    elif update_method == "add":
        favorite_list.add(music_id)

    else:
        return_json["msg"] = "wrong update method"
        return return_json

    users_collection.update_one(
        {"username": username}, {"$set": {"favorite_list": list(favorite_list)}}
    )

    return_json["success"] = 1

    return return_json
