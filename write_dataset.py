import serial
import csv

# Set the serial port and baud rate to match your Arduino
ser = serial.Serial('COM5', 9600)  # Replace 'COM4' with your Arduino's serial port

# Open a CSV file for writing
with open('modulated_noise.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write the header row if needed
    csv_writer.writerow(['Time', 'LUX'])

    try:
        while True:
            # Read a line of data from the Arduino
            data = ser.readline().decode().strip()
            if data:
                time_elapsed, lux = data.split(",")
                csv_writer.writerow([time_elapsed, lux])
    except KeyboardInterrupt:
        # Close the serial port
        ser.close()

