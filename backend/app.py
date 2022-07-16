from flask import Flask, Response, render_template
from flask_cors import CORS
from scipy.io import wavfile
from scipy.fftpack import fft

import os
from datetime import timedelta

from music.api import music
from user.api import user

import matplotlib.pyplot as plt

app = Flask(__name__, static_folder="static")
CORS(app, supports_credentials=True)

app.config["SECRET_KEY"] = os.urandom(24)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=31)

app.register_blueprint(music, url_prefix="/music")
app.register_blueprint(user, url_prefix="/user")


@app.route("/audio_visualize")
def audio_visualize():
    fs, data = wavfile.read("./static/one_last_kiss.wav")  # load the data
    b = [(ele / 2**16.0) for ele in data]
    c = fft(b)
    print(type(data))
    print(data.dtype)
    print(data.shape)
    plt.subplot(211)
    plt.plot(b, "b")
    plt.title("time line")
    plt.subplot(212)
    plt.plot(abs(c), "r")
    plt.title("fft")
    plt.savefig("test.jpg")

    return str(data.shape)


@app.route("/")
def index():
    """Video streaming home page."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
