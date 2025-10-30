#!/usr/bin/env python3
"""
Simple Speech-to-Text converter for WAV files
Uses Pocketsphinx (offline, free)
"""

from pocketsphinx import AudioFile

def wav_to_text(wav_file_path):
    """
    Convert WAV file to text using speech recognition

    Args:
        wav_file_path: Path to the WAV file

    Returns:
        Transcribed text or error message
    """
    print(f"Loading audio file: {wav_file_path}")

    try:
        print("Transcribing speech to text (using offline recognition)...")

        # Process audio file with pocketsphinx
        audio = AudioFile(audio_file=wav_file_path)

        # Collect all transcribed text
        text_parts = []
        for phrase in audio:
            if phrase:
                text_parts.append(str(phrase))

        # Combine all parts
        text = " ".join(text_parts)

        if text:
            print("\n" + "="*60)
            print("TRANSCRIPTION:")
            print("="*60)
            print(text)
            print("="*60)
            return text
        else:
            print("\nError: Could not understand the audio or no speech detected")
            return None

    except FileNotFoundError:
        error_msg = f"File not found: {wav_file_path}"
        print(f"\nError: {error_msg}")
        return None

    except Exception as e:
        error_msg = f"An error occurred: {e}"
        print(f"\nError: {error_msg}")
        return None


def main():
    # Path to your WAV file
    wav_file = "./capture_Dialogue.wav"

    # Convert speech to text
    result = wav_to_text(wav_file)

    # Optionally save to a text file
    if result:
        output_file = "transcription.txt"
        with open(output_file, 'w') as f:
            f.write(result)
        print(f"\nTranscription saved to: {output_file}")


if __name__ == "__main__":
    main()
