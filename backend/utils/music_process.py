from scipy.io import wavfile
from scipy.fft import fft, fftfreq, rfft, rfftfreq
import numpy as np

import pickle
import matplotlib.pyplot as plt


def wav_to_bins(sample_rate, origin_data, song_name, bin_count=50, second_freq=20):
    duration = origin_data.shape[0] // sample_rate
    bins = []

    flag = True

    for current_second in range(duration):
        print(current_second)
        for i in range(second_freq):

            data = origin_data[:, 0] + origin_data[:, 1]
            cur_sec = 80

            chunk_size = 10000

            data = data[
                sample_rate * cur_sec
                + ((sample_rate - chunk_size) // second_freq * i) : sample_rate
                * cur_sec
                + chunk_size
                + ((sample_rate - chunk_size) // second_freq * i)
            ]

            b = [(ele / 2**17.0) for ele in data]
            c = rfft(b)
            x = rfftfreq(len(b), 1 / sample_rate)
            chunk_size = len(x)

            x, c = zip(*sorted(zip(x, np.abs(c))))
            x, c = list(x), list(c)

            x = x[(chunk_size - 2000) // 2 : -(chunk_size - 2000) // 2]
            c = c[(chunk_size - 2000) // 2 : -(chunk_size - 2000) // 2]

            histogram = []

            for i in range(bin_count):
                bin = c[(len(x) // bin_count) * i : (len(x) // bin_count) * (i + 1)]
                bin = sum(bin) / len(bin)
                histogram.append(bin)

            bins.append(histogram)

            if flag:
                plt.subplot(211)
                plt.plot(b, "b")
                plt.title("time line")
                plt.subplot(212)
                plt.plot(histogram, "r")
                plt.title("fft")
                plt.savefig("img2.jpg")
                flag = False

    with open(f'{song_name}.pickle', 'wb') as f:
        pickle.dump(bins, f)


sample_rate, data = wavfile.read("./static/one_last_kiss.wav")
wav_to_bins(sample_rate, data, "one_last_kiss", 50, 20, )
