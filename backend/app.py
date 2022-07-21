import os
from datetime import timedelta
from distutils.log import debug

import matplotlib.pyplot as plt
from flask import Flask, Response, render_template, session
from flask_cors import CORS
from flask_session import Session
from flask_socketio import SocketIO
from scipy.fftpack import fft
from scipy.io import wavfile

from music.api import music
from user.api import user


def create_app():
    app = Flask(__name__, static_folder="static")
    CORS(app, supports_credentials=True)

    app.config["SECRET_KEY"] = os.urandom(24)
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=1)

    app.register_blueprint(music, url_prefix="/music")
    app.register_blueprint(user, url_prefix="/user")

    socketio = SocketIO(app, cors_allowed_origins="*")

    return socketio, app


socketio, app = create_app()


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


@socketio.on("join_chat", namespace="/chatroom")
def join_chat(data):
    username = data["username"]

    if username is None:
        socketio.emit(
            "error", "authentication failed\ntry login again", namespace="/chatroom"
        )
        return

    socketio.emit("join_success", {"username": username}, namespace="/chatroom")


@socketio.on("send_message", namespace="/chatroom")
def send_message(data):
    print("Data", data)

    username = data["username"]
    msg = data["msg"]

    if username is None:
        socketio.emit(
            "error", "authentication failed\ntry login again", namespace="/chatroom"
        )
        return

    socketio.emit("get_msg", data, namespace="/chatroom")


if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
    # app.run(host="0.0.0.0")
