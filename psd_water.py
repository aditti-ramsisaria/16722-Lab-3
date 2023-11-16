import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# Load lux data from the CSV file
carrier_data = np.genfromtxt('air_reference.csv', delimiter=',', skip_header=1)  
modulated_data = np.genfromtxt('water_modulated.csv', delimiter=',', skip_header=1)  

time_signal = carrier_data[1:400, 0] 
carrier_signal = carrier_data[1:400, 1] 
modulated_signal = modulated_data[1:400, 1] 

def perform_psd(signal, reference, sampling_rate):
    # Perform PSD by multiplying the signal with the reference
    psd_result = signal * reference

    # Apply a low-pass filter to extract the DC component
    cutoff_frequency = 0.1  # Adjust the cutoff frequency as needed
    filtered_result = butter_lowpass_filter(psd_result, cutoff_frequency, sampling_rate)

    return filtered_result

def butter_lowpass_filter(data, cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = lfilter(b, a, data)
    return filtered_data

psd_signal = perform_psd(modulated_signal, carrier_signal, 10)

carrier_amplitude = np.mean(np.abs(carrier_signal))
modulated_amplitude = np.mean(np.abs(modulated_signal))
psd_amplitude = np.mean(np.abs(psd_signal))

print("Carrier Amplitude:", carrier_amplitude)
print("Modulated Signal Amplitude:", modulated_amplitude)

# Reconstruct Signal from PSD
reconstructed_signal = psd_signal / carrier_amplitude
reconstructed_amplitude = np.mean(np.abs(reconstructed_signal))
print("PSD Signal Amplitude:", reconstructed_amplitude)

noise = reconstructed_signal - modulated_signal

# Calculate Signal Power (using the modulated signal)
signal_power = np.mean(modulated_signal**2)

# Calculate Noise Power
noise_power = np.mean(noise**2)

# Calculate SNR (in dB)
snr_db = 10 * np.log10(signal_power / noise_power)

print("Signal Power:", signal_power)
print("Noise Power:", noise_power)
print("SNR (dB):", snr_db)

# Plot Raw Signal over Time 
plt.figure(figsize=(10, 4))
plt.plot(time_signal, carrier_signal, label='Carrier (Air) Signal')
plt.plot(time_signal, modulated_signal, label='Modulated (Water) Signal')
plt.legend()
plt.title('Reference and Modulated LUX Signal over Time')
plt.xlabel('Time')
plt.ylabel('Signal Amplitude')
plt.grid(True)
plt.legend()
plt.show()

# Plot Raw Signal over Time - Dataset 3
plt.figure(figsize=(10, 4))
plt.plot(time_signal, reconstructed_signal, label='PSD LUX Signal')
plt.legend()
plt.title('PSD LUX Signal over Time')
plt.xlabel('Time')
plt.ylabel('Signal Amplitude')
plt.grid(True)
plt.legend()
plt.show()
