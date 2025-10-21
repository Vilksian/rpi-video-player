import vlc
import os
import platform
import time

# Turn display on (if using vcgencmd control)
if platform.system() == "Linux":
    os.system("vcgencmd display_power 1")

# Create a VLC instance with loop enabled
# --no-video-title-show hides the overlay text
# --input-repeat=-1 loops forever
instance = vlc.Instance("--no-video-title-show --input-repeat=-1 --quiet")

# Create player
player = instance.media_player_new()

# Load media
media = instance.media_new("test2.mp4")
player.set_media(media)

# Start playback
player.play()

# Keep script alive indefinitely
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    player.stop()
