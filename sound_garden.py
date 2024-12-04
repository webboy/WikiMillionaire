from services.sound_service import SoundService

# Test the SoundService class
if __name__ == "__main__":
    import time

    # Initialize the sound service
    sound_service = SoundService()

    # print("Playing opening sound...")
    # sound_service.play_opening_sound()
    # time.sleep(3)  # Allow the opening sound to play

    print("Playing background music...")
    sound_service.play_background_music()
    time.sleep(5)

    sound_service.disable_sound()

     # Let the background music play

    print("Playing answer sound...")
    sound_service.play_answer_sound()
    time.sleep(2)  # Let the answer sound play

    print("Stopping background music...")
    sound_service.stop_background_music()

    print("Playing end sound...")
    sound_service.play_end_sound()
    time.sleep(3)  # Let the end sound play

    print("All sounds played successfully.")