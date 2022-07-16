import base64
import hashlib
import os

import pickle
from flask_cors import CORS
from scipy.io import wavfile
from flask import Blueprint, request
from utils.music_process import wav_to_bins

music = Blueprint("music", __name__)
CORS(music, supports_credentials=True)


@music.route("/")
def index():
    return "Hello music"


# @music.route("/play", methods=["GET"])
# def play():
#     sample_rate, data = wavfile.read("./static/one_last_kiss.wav")
#     bins = wav_to_bins(
#         sample_rate,
#         data,
#         "one_last_kiss",
#         50,
#         20,
#     )

#     return bins


@music.route("/audio_wave/", methods=["GET"])
def audio_wave():
    with open("one_last_kiss.pickle", "rb") as file:
        return {"wave": pickle.load(file)}
    # with open("one_last_kiss.pickle", "rb") as file:
    #     return {"wave": pickle.load(file)}
