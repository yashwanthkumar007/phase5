import requests
import RPi.GPIO as GPIO
import time

# Define GPIO pins for the sensor
SENSOR_PIN = 18

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# Replace this URL with the appropriate endpoint for sending alerts
ALERT_ENDPOINT = "https://your_alert_endpoint.com"

# Function to send alerts
def send_alert():
    try:
        alert_data = {
            'message': 'Flood warning: Water level is above threshold!'
        }
        response = requests.post(ALERT_ENDPOINT, json=alert_data)
        if response.status_code == 200:
            print("Alert sent successfully.")
        else:
            print(f"Failed to send alert. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Function for data logging
def log_data(sensor_value):
    with open("flood_log.txt", "a") as file:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - Water level: {sensor_value}\n"
        file.write(log_message)

# Main loop for monitoring water levels
try:
    while True:
        sensor_value = GPIO.input(SENSOR_PIN)
        if sensor_value:
            print("Water level is normal.")
            log_data("Normal")
        else:
            print("Alert: Water level is above threshold!")
            send_alert()
            log_data("Alert")
        time.sleep(5)  # Adjust the time interval based on the sensor reading frequency
except KeyboardInterrupt:
    print("Keyboard Interrupt. Cleaning up GPIO...")
    GPIO.cleanup()
