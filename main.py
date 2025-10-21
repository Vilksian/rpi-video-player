import vlc
import os
import platform
import random
import glob
import time
from gpiozero import Button  # assuming you’re using a GPIO pin as input

# --- setup ---
if platform.system() == "Linux":
    os.system("vcgencmd display_power 1")

# pin setup (adjust pin number)
trigger_pin = 17
trigger_button = Button(trigger_pin, pull_up=False)  # active HIGH input

# collect videos
loop_video_path = "loop.mp4"
trigger_videos = glob.glob("*trigger*.mp4")

# VLC setup
instance = vlc.Instance()
player = instance.media_player_new()

def play_video(video_path):
    """Load and play a specific video."""
    media = vlc.Media(video_path)
    player.set_media(media)
    player.play()

# start with looping video
current_video = "loop"
play_video(loop_video_path)

while True:
    # check if trigger signal is active
    if trigger_button.is_pressed and current_video == "loop":
        # pick a random trigger video
        if trigger_videos:
            chosen_video = random.choice(trigger_videos)
            print(f"Trigger detected! Playing: {chosen_video}")
            current_video = "trigger"
            play_video(chosen_video)
        else:
            print("No trigger videos found!")

    # check if video ended
    state = player.get_state()
    if state == vlc.State.Ended:
        if current_video == "trigger":
            print("Returning to loop.")
            current_video = "loop"
            play_video(loop_video_path)
        elif current_video == "loop":
            # restart loop
            play_video(loop_video_path)

    time.sleep(0.1)
