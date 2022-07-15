from flask import Flask, Response, render_template
from scipy.io import wavfile
from scipy.fftpack import fft

import matplotlib.pyplot as plt

app = Flask(__name__, static_folder='static')


@app.route("/wav")
def streamwav():
    def generate():
        with open("one_last_kiss.mp3", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/x-wav")


@app.route("/ogg")
def streamogg():
    def generate():
        with open("signals/song.ogg", "rb") as fogg:
            data = fogg.read(1024)
            while data:
                yield data
                data = fogg.read(1024)
    return Response(generate(), mimetype="audio/ogg")

@app.route("/audio_visualize")
def audio_visualize():
    fs, data = wavfile.read('./static/one_last_kiss.wav') # load the data
    b = [(ele/2**16.) for ele in data] 
    c = fft(b)
    print(type(data))
    print(data.dtype)
    print(data.shape)
    plt.subplot(211)
    plt.plot(b,'b')
    plt.title('time line')
    plt.subplot(212)
    plt.plot(abs(c),'r')
    plt.title('fft') 
    plt.savefig("test.jpg")

    return str(data.shape)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')