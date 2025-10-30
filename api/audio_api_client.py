#!/usr/bin/env python3
"""
Simple API Client for GET, POST, and DELETE requests
Easily configurable base URL and endpoints
"""

import requests
import json
from typing import Optional, Dict, Any


class APIClient:
    def __init__(self, base_url: str):
        """
        Initialize the API client with a base URL

        Args:
            base_url: Base IP address or URL (e.g., 'http://192.168.1.1:8000')
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Content-Type': 'application/json'
        }

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Send a GET request

        Args:
            endpoint: API endpoint (e.g., '/users' or '/api/data')
            params: Optional query parameters

        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        print(f"GET {url}")
        response = requests.get(url, params=params, headers=self.headers)
        return response

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Send a POST request

        Args:
            endpoint: API endpoint
            data: Data to send in request body

        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        print(f"POST {url}")
        response = requests.post(url, json=data, headers=self.headers)
        return response

    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Send a DELETE request

        Args:
            endpoint: API endpoint
            params: Optional query parameters

        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        print(f"DELETE {url}")
        response = requests.delete(url, params=params, headers=self.headers)
        return response

    def print_response(self, response: requests.Response):
        """
        Pretty print the response

        Args:
            response: Response object to print
        """
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        try:
            print(f"Response Body:\n{json.dumps(response.json(), indent=2)}")
        except json.JSONDecodeError:
            print(f"Response Body:\n{response.text}")
        print("-" * 50)


def main():
    # ============ CONFIGURATION - CHANGE THESE ============
    BASE_URL = "http://192.168.0.111"  # Misty Robot IP Address

    # Initialize client
    client = APIClient(BASE_URL)

    # ============ EXAMPLE REQUESTS - MODIFY AS NEEDED ============
    # Uncomment the requests you want to use

    # --- SYSTEM INFO ---
    # Get device information
    # print("\n=== Get Device Info ===")
    # response = client.get("/api/device")
    # client.print_response(response)

    # Get battery level
    # print("\n=== Get Battery Level ===")
    # response = client.get("/api/battery")
    # client.print_response(response)

    # --- LED CONTROL ---
    # Change LED color to red
    # print("\n=== Change LED to Red ===")
    # response = client.post("/api/led", data={"Red": 255, "Green": 0, "Blue": 0})
    # client.print_response(response)

    # LED transition (fade between colors)
    # print("\n=== LED Transition ===")
    # response = client.post("/api/led/transition", data={
    #     "Red": 255, "Green": 0, "Blue": 0,
    #     "Red2": 0, "Green2": 0, "Blue2": 255,
    #     "TransitionType": "Breathe",
    #     "TimeMs": 2000
    # })
    # client.print_response(response)

    # --- MOVEMENT ---
    # Drive forward
    # print("\n=== Drive Forward ===")
    # response = client.post("/api/drive", data={"LinearVelocity": 20, "AngularVelocity": 0})
    # client.print_response(response)

    # Stop driving
    # print("\n=== Stop Driving ===")
    # response = client.post("/api/drive/stop")
    # client.print_response(response)

    # Move head
    # print("\n=== Move Head ===")
    # response = client.post("/api/head", data={"Pitch": 10, "Roll": 0, "Yaw": 0, "Velocity": 10})
    # client.print_response(response)

    # Move arms
    # print("\n=== Move Right Arm ===")
    # response = client.post("/api/arms", data={"Arm": "right", "Position": 90, "Velocity": 50})
    # client.print_response(response)

    # --- AUDIO & SPEECH ---
    # Play audio
    # print("\n=== Play Audio ===")
    # response = client.post("/api/audio/play", data={"FileName": "s_Amazement.wav"})
    # client.print_response(response)

    # Text to speech
    #print("\n=== Text to Speech ===")
    #response = client.post("/api/tts/speak", data={"Text": "Hello, I am Misty! using A P I"})
    #client.print_response(response)

    # Speech to text (Capture Speech)
    """
    print("\n=== Capture Speech ===")
    response = client.post("/api/audio/speech/capture", data={
         "OverwriteExisting": True,
         "SilenceTimeout": 5000000000000,
         "MaxSpeechLength": 750000,
         "RequireKeyPhrase": False,
    })
    client.print_response(response)
    """

    # # Note: Listen for VoiceRecord WebSocket event to get transcription results

    # --- IMAGES & DISPLAY ---
    # List images
    # print("\n=== List Images ===")
    # response = client.get("/api/images/list")
    # client.print_response(response)

    # Display image
    # print("\n=== Display Image ===")
    # response = client.post("/api/images/display", data={"FileName": "e_DefaultContent.jpg"})
    # client.print_response(response)

    # Display text
    # print("\n=== Display Text ===")
    # response = client.post("/api/text/display", data={"Text": "Hello World!"})
    # client.print_response(response)

    # --- PERCEPTION ---
    # Take a photo
    # print("\n=== Take Photo ===")
    # response = client.post("/api/cameras/photo", data={"FileName": "my_photo.jpg"})
    # client.print_response(response)

    # Start face detection
    # print("\n=== Start Face Detection ===")
    # response = client.post("/api/faces/detection/start")
    # client.print_response(response)

    # Stop face detection
    # print("\n=== Stop Face Detection ===")
    # response = client.post("/api/faces/detection/stop")
    # client.print_response(response)

    # --- ASSET MANAGEMENT ---
    # List audio files
    print("\n=== List Audio Files ===")
    response = client.get("/api/audio/list")
    client.print_response(response)

    # Delete an image
    # print("\n=== Delete Image ===")
    # response = client.delete("/api/images", params={"FileName": "my_photo.jpg"})
    # client.print_response(response)

    print("\n=== Ready to use! Uncomment the examples above to test Misty's APIs ===")


if __name__ == "__main__":
    main()
