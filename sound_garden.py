from services.sound_service import SoundService

# Test the SoundService class
if __name__ == "__main__":
    import time

    # Initialize the sound service
    sound_service = SoundService()



    print("Playing end sound...")
    sound_service.play_end_sound()
    time.sleep(13)  # Let the end sound play

    print("All sounds played successfully.")