import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, butter, lfilter

# Load lux data from the CSV file
data = np.genfromtxt('modulated_noise.csv', delimiter=',', skip_header=1)  # Skip the header

time_signal = data[1:400, 0]
lux_signal = data[1:400, 1]

# Generate time array based on the known sampling rate
sampling_rate = 10      # 10 Hz, one sample every 100 ms
signal_frequency = 0.1  # square wave time period of 2s, amplitude = 128

lux_frequencies, lux_psd = welch(lux_signal, fs=sampling_rate, nperseg=len(lux_signal))

def butter_lowpass_filter(data, cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = lfilter(b, a, data)
    return filtered_data

filtered_signal = butter_lowpass_filter(lux_signal, signal_frequency, sampling_rate)
noise = filtered_signal - lux_signal

# Calculate Signal Power (using the modulated signal)
signal_power = np.mean(lux_signal**2)

# Calculate Noise Power
noise_power = np.mean(noise**2)

# Calculate SNR (in dB)
snr_db = 10 * np.log10(signal_power / noise_power)

print("Signal Power:", signal_power)
print("Noise Power:", noise_power)
print("SNR (dB):", snr_db)


# Plot Raw Signal over Time
plt.figure(figsize=(10, 4))
plt.plot(time_signal, lux_signal, label='Raw LUX Signal')
plt.title('Dataset 2 - Raw LUX Signal over Time')
plt.xlabel('Time')
plt.ylabel('Signal Amplitude')
plt.grid(True)
plt.legend()
plt.show()

# Plot Raw Signal over Time
plt.figure(figsize=(10, 4))
plt.plot(time_signal, filtered_signal, label='Filtered LUX Signal')
plt.plot(time_signal, noise, label="Noise")
plt.title('Dataset 2 - Filtered LUX Signal over Time')
plt.xlabel('Time')
plt.ylabel('Signal Amplitude')
plt.grid(True)
plt.legend()
plt.show()

# # Plot PSD 
# plt.figure(figsize=(10, 5))
# plt.semilogx(lux_frequencies, lux_psd)
# plt.legend(["PSD"])
# plt.title('Power Spectral Density (PSD) of LUX Data')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('PSD (dB/Hz)')
# plt.grid()
# plt.show()
