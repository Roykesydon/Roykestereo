from gettext import bind_textdomain_codeset
from scipy.io import wavfile
from scipy.fft import fft, fftfreq, rfft, rfftfreq
import numpy as np
import math

import pickle
import matplotlib.pyplot as plt


def wav_to_bins(sample_rate, origin_data, song_name, bin_count=70, second_freq=100):
    duration = origin_data.shape[0] // sample_rate
    bins = []

    flag = True

    for current_second in range(duration):
        print(current_second)
        for i in range(second_freq):

            if len(origin_data.shape) == 1:
                data = origin_data
            else:
                data = origin_data[:, 0] + origin_data[:, 1]

            chunk_size = 20000
            # crop_size = 10000

            data = data[
                sample_rate * current_second
                + ((sample_rate - chunk_size) // second_freq * i) : sample_rate
                * current_second
                + chunk_size
                + ((sample_rate - chunk_size) // second_freq * i)
            ]

            b = [(ele / 2**17.0) for ele in data]
            c = rfft(b)
            x = rfftfreq(len(b), 1 / sample_rate)
            chunk_size = len(x)

            x, c = zip(*sorted(zip(x, np.abs(c))))
            x, c = list(x), list(c)

            for i, val in enumerate(x):
                if val > 2000:
                    x = x[: i + 1]
                    c = c[: i + 1]
                    break

            # print(len(x), x[-1])

            # print(x[0], x[-1])
            # x = x[(chunk_size - crop_size) // 2 : -(chunk_size - crop_size) // 2]
            # c = c[(chunk_size - crop_size) // 2 : -(chunk_size - crop_size) // 2]

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


    bins = [[math.log2(bin + 1) for bin in hist] for hist in bins]

    # mean = np.average(bins)
    # std = np.std(bins)
    # bins = [[(bin - mean) / std for bin in hist] for hist in bins]

    min_bin = min([min(hist) for hist in bins])
    bins = [[bin + min_bin for bin in hist] for hist in bins]

    max_bin = max([max(hist) for hist in bins])
    bins = [[bin / max_bin for bin in hist] for hist in bins]

    min_bins = [min(hist) for hist in bins]
    bins = [[bin - min_bin for bin in hist] for min_bin, hist in zip(min_bins, bins)]

    with open(f"{song_name}.pickle", "wb") as f:
        pickle.dump(bins, f)


# sample_rate, data = wavfile.read("./static/beautiful_world.wav")
# wav_to_bins(sample_rate, data, "beautiful_world", 50, 20, )
