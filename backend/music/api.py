import base64
import hashlib
import os
import subprocess
import pickle
from flask_cors import CORS
from scipy.io import wavfile
from flask import Blueprint, request, session, send_from_directory, jsonify
from utils.music_process import wav_to_bins
from utils.database import get_connection
from bson import ObjectId
from time import time

music = Blueprint("music", __name__)
CORS(music, supports_credentials=True)


@music.route("/all_id_list")
def get_all_music_list():
    """
    Get connection with mongodb
    """
    client = get_connection()
    db = client["roykestereo_db"]
    music_collection = db["music"]
    cursor = music_collection.find({"available": True})
    all_music_list = list(cursor)
    all_music_list = [str(music["_id"]) for music in all_music_list]

    return jsonify(all_music_list)


@music.route("/info/<id>")
def search_by_id(id):
    """
    Get connection with mongodb
    """
    client = get_connection()
    db = client["roykestereo_db"]
    music_collection = db["music"]
    music_info = music_collection.find_one({"_id": ObjectId(id)})
    del music_info["_id"]

    return music_info


@music.route("/wave/<id>")
def wave_by_id(id):
    with open(f"./upload_files/wave/{str(id)}.pickle", "rb") as file:
        return {"wave": pickle.load(file)}


@music.route("/audio/<id>")
def audio_by_id(id):
    return send_from_directory(f"./upload_files/music/", f"{str(id)}.wav")


@music.route("/cover/<id>")
def cover_by_id(id):
    return send_from_directory(f"./upload_files/cover/", f"{str(id)}")


@music.route("/upload_music", methods=["POST"])
def upload_music():
    data = request.get_json()
    return_json = {"success": 0, "msg": ""}

    music_name = data["music_name"]
    cover = data["cover"]
    music = data["music"]

    cover_extension = cover.split(";")[0].split("/")[-1]
    music_extension = music.split(";")[0].split("/")[-1]

    username = session.get("username")
    if username is None:
        return_json["msg"] = "authentication failed\ntry login again"
        return return_json

    """
    Get connection with mongodb
    """
    client = get_connection()
    db = client["roykestereo_db"]

    """
    get user info
    """
    users_collection = db["users"]
    user_data = users_collection.find_one({"username": username})
    nickname = user_data["nickname"]

    """
    get new music id
    """
    music_collection = db["music"]
    new_music_id = ""

    timestamp = str(int(time() * 1000))
    """
    Save info to mongodb
    """
    try:
        data = {
            "music_name": music_name,
            "username": str(username),
            "nickname": str(nickname),
            "timestamp": timestamp,
            "available": False,
        }
        music_collection.insert_one(data)
    except:
        return_json["msg"] = "insert db fail"
        return return_json

    music_data = music_collection.find_one(data)

    new_music_id = str(music_data["_id"])

    """
    Save upload music
    """
    try:
        music_bytes = music.split(",")[-1]
        file_path = "./upload_files/music/" + str(new_music_id)
        with open(
            file_path + "." + music_extension,
            "wb",
        ) as file:
            file.write(base64.b64decode(music_bytes))
    except:
        return_json["msg"] = "Save music fail"
        return return_json

    if music_extension != "wav":
        try:
            subprocess.call(
                [
                    "C:\\Users\\Roykesydone\\ffmpeg-5.0.1-essentials_build\\ffmpeg-5.0.1-essentials_build\\bin\\ffmpeg.exe",
                    "-y",
                    "-i",
                    f"{file_path}.{music_extension}",
                    f"{file_path}.wav",
                ]
            )
        except:
            return_json["msg"] = "Save music fail"
            return return_json

        os.remove(f"{file_path}.{music_extension}")

    """
    Save music wave
    """
    try:
        sample_rate, data = wavfile.read(f"{file_path}.wav")
        file_path = "./upload_files/wave/" + str(new_music_id) + ".pickle"
        wav_to_bins(sample_rate, data, file_path)
    except:
        return_json["msg"] = "Save wave fail"
        return return_json

    """
    Save upload image
    """
    try:
        image_bytes = cover.split(",")[-1]
        file_path = "./upload_files/cover/" + str(new_music_id)
        with open(
            file_path,
            "wb",
        ) as file:
            file.write(base64.b64decode(image_bytes))
    except:
        return_json["msg"] = "Save image fail"
        return return_json

    """
    Save info to mongodb
    """
    try:
        music_collection.update_one(
            {"_id": ObjectId(new_music_id)}, {"$set": {"available": True}}
        )
    except:
        return_json["msg"] = "insert db fail"
        return return_json

    return_json["success"] = 1

    return return_json


@music.route("/audio_wave/", methods=["GET"])
def audio_wave():
    with open("one_last_kiss.pickle", "rb") as file:
        return {"wave": pickle.load(file)}
    # with open("one_last_kiss.pickle", "rb") as file:
    #     return {"wave": pickle.load(file)}
