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

# the caching time in ms
cache_ms = 400

# pin setup (adjust pin number)
trigger_pin = 17
trigger_button = Button(trigger_pin, pull_up=False)  # active HIGH input

# collect videos
loop_video_path = "loop.mp4"
trigger_videos = glob.glob("*trigger*.mp4")
print(
    f"""
    Raspberry Pi Zero W Video Player
    System: {platform.system()}
    Cache Time: {cache_ms}
    Loop Video: {"Found" if trigger_pin else "Not Found"}
    Trigger Videos: {f"{len(trigger_videos)} Found"}
    Trigger Pin: {trigger_pin}
    """,
)

# VLC setup
instance = vlc.Instance(f"--no-video-title-show --quiet --file-caching={cache_ms}")
player = instance.media_player_new()

def play_video(video_path):
    """Load and play a specific video."""
    media = vlc.Media(video_path)
    player.set_media(media)
    player.play()

# start with looping video
current_video = "loop"
last_trigger_video = None  # keep track of previous trigger
play_video(loop_video_path)

while True:
    # check if trigger signal is active
    if trigger_button.is_pressed and current_video == "loop":
        # pick a random trigger video
        if trigger_videos:

            # make a list excluding the last played trigger
            available_videos = [v for v in trigger_videos if v != last_trigger_video]
            if not available_videos:  # all videos are the same as last, fallback
                available_videos = trigger_videos

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
