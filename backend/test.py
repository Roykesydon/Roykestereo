from scipy.io import wavfile

from utils.music_process import wav_to_bins

sample_rate, data = wavfile.read("./static/one_last_kiss.wav")
# sample_rate, data = wavfile.read("./static/beautiful_world.wav")
# sample_rate, data = wavfile.read("./static/the_edge.wav")
# sample_rate, data = wavfile.read("./static/the_edge.wav")
print(sample_rate, data.dtype)
# wav_to_bins(sample_rate, data, "the_edge")
wav_to_bins(sample_rate, data, "one_last_kiss")
