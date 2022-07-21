import chunk
import math
import pickle
from gettext import bind_textdomain_codeset

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq, rfft, rfftfreq
from scipy.io import wavfile


def wav_to_bins(
    sample_rate,
    origin_data,
    file_path,
    bin_count=100,
    second_freq=20,
    max_hz=2000,
    chunk_size=2250,
):
    duration = origin_data.shape[0] // sample_rate
    bins = []

    flag = True

    for current_second in range(duration):
        for i in range(second_freq):

            if len(origin_data.shape) == 1:
                data = origin_data
            else:
                data = origin_data[:, 0] + origin_data[:, 1]

            partition_size = sample_rate // second_freq
            # crop_size = 10000

            data = data[
                sample_rate * current_second
                + partition_size * i : sample_rate * current_second
                + partition_size * i
                + chunk_size
            ]

            b = [(ele / 2**17.0) for ele in data]
            c = rfft(b)
            x = rfftfreq(len(b), 1 / sample_rate)

            x, c = zip(*sorted(zip(x, np.abs(c))))
            x, c = list(x), list(c)

            # print(len(x), len(c))
            # print(x[0], x[-1])

            for i, val in enumerate(x):
                if val > max_hz:
                    x = x[: i + 1]
                    c = c[: i + 1]
                    break

            # print(len(x))
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

            # if flag:
            #     plt.subplot(211)
            #     plt.plot(b, "b")
            #     plt.title("time line")
            #     plt.subplot(212)
            #     plt.plot(histogram, "r")
            #     plt.title("fft")
            #     plt.savefig("img2.jpg")
            #     flag = False

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

    with open(file_path, "wb") as f:
        pickle.dump(bins, f)


# sample_rate, data = wavfile.read("./static/beautiful_world.wav")
# wav_to_bins(sample_rate, data, "beautiful_world", 50, 20, )
