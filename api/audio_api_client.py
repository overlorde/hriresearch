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

    def list_audio_recordings(self) -> Optional[list]:
        """
        List all audio recordings available on the device

        Returns:
            List of audio file names, or None if request fails
        """
        print("\n=== Listing All Audio Recordings ===")
        response = self.get("/api/audio/list")
        self.print_response(response)

        if response.status_code == 200:
            try:
                data = response.json()
                # The API typically returns a list under 'result' key
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'result' in data:
                    return data['result']
                else:
                    return data
            except json.JSONDecodeError:
                print("Error: Could not parse response as JSON")
                return None
        else:
            print(f"Error: Failed to list recordings (Status: {response.status_code})")
            return None

    def download_audio_recording(self, filename: str, save_path: Optional[str] = None) -> bool:
        """
        Download a specific audio recording from the device

        Args:
            filename: Name of the audio file to download
            save_path: Local path to save the file (defaults to current directory with same filename)

        Returns:
            True if download successful, False otherwise
        """
        if save_path is None:
            save_path = filename

        url = f"{self.base_url}/api/audio"
        print(f"\n=== Downloading Audio Recording: {filename} ===")
        print(f"GET {url}?FileName={filename}")

        try:
            # Download the audio file (binary data)
            response = requests.get(url, params={"FileName": filename})

            if response.status_code == 200:
                # Save the audio file
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"Successfully downloaded: {filename} -> {save_path}")
                print(f"File size: {len(response.content)} bytes")
                return True
            else:
                print(f"Error: Failed to download (Status: {response.status_code})")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"Error downloading file: {str(e)}")
            return False

    def download_all_recordings(self, output_dir: str = "./recordings") -> int:
        """
        Download all audio recordings from the device

        Args:
            output_dir: Directory to save all recordings (created if doesn't exist)

        Returns:
            Number of files successfully downloaded
        """
        import os

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Get list of all recordings
        recordings = self.list_audio_recordings()

        if not recordings:
            print("No recordings found or failed to list recordings")
            return 0

        print(f"\n=== Downloading {len(recordings)} recordings to {output_dir} ===")

        success_count = 0
        for i, recording in enumerate(recordings, 1):
            # Handle both string filenames and dict objects
            filename = recording if isinstance(recording, str) else recording.get('name', recording.get('fileName', ''))

            if filename:
                save_path = os.path.join(output_dir, filename)
                print(f"\n[{i}/{len(recordings)}] Downloading {filename}...")
                if self.download_audio_recording(filename, save_path):
                    success_count += 1

        print(f"\n=== Download Complete: {success_count}/{len(recordings)} files downloaded ===")
        return success_count

    def start_recording(self, filename: str = "capture_speech.wav",
                       max_speech_length_ms: int = 10000,
                       silence_timeout_ms: int = 5000,
                       overwrite_existing: bool = True) -> requests.Response:
        """
        Start recording speech from Misty's microphone

        Args:
            filename: Name to save the recording as (default: "capture_speech.wav")
            max_speech_length_ms: Maximum recording length in milliseconds (default: 10000 = 10 seconds)
            silence_timeout_ms: Stop recording after this many ms of silence (default: 5000 = 5 seconds)
            overwrite_existing: Whether to overwrite existing file with same name (default: True)

        Returns:
            Response object from the API
        """
        print(f"\n=== Starting Speech Recording: {filename} ===")
        print(f"Max length: {max_speech_length_ms}ms, Silence timeout: {silence_timeout_ms}ms")

        response = self.post("/api/audio/speech/capture", data={
            "FileName": filename,
            "MaxSpeechLength": max_speech_length_ms,
            "SilenceTimeout": silence_timeout_ms,
            "OverwriteExisting": overwrite_existing,
            "RequireKeyPhrase": False
        })
        self.print_response(response)
        return response

    def stop_recording(self) -> requests.Response:
        """
        Stop the current audio recording

        Returns:
            Response object from the API
        """
        print("\n=== Stopping Speech Recording ===")
        response = self.post("/api/audio/recording/stop")
        self.print_response(response)
        return response


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
    # print("\n=== List Audio Files ===")
    # response = client.get("/api/audio/list")
    # client.print_response(response)

    # Delete an image
    # print("\n=== Delete Image ===")
    # response = client.delete("/api/images", params={"FileName": "my_photo.jpg"})
    # client.print_response(response)

    # --- RECORDING WORKFLOW ---
    # Record speech and download it
    import time

    # Step 1: Start recording (will automatically stop after silence or max length)
    print("\n" + "="*60)
    print("RECORDING WORKFLOW")
    print("="*60)
    client.start_recording(filename="capture_Dialogue.wav", max_speech_length_ms=10000, silence_timeout_ms=5000)

    # Step 2: Wait for recording to complete (it stops automatically)
    print("\n🎤 Speak now! Recording will stop after 5 seconds of silence or 10 seconds total...")
    time.sleep(15)  # Wait for recording to complete

    # Step 3: List all recordings to verify it was saved
    print("\n" + "="*60)
    print("LISTING ALL RECORDINGS")
    print("="*60)
    recordings = client.list_audio_recordings()

    # Step 4: Download the recorded file
    print("\n" + "="*60)
    print("DOWNLOADING RECORDING")
    print("="*60)
    client.download_audio_recording("capture_Dialogue.wav", "./capture_Dialogue.wav")

    print("\n" + "="*60)
    print("✓ COMPLETE! Your recording has been saved to: ./capture_Dialogue.wav")
    print("="*60)


if __name__ == "__main__":
    main()
