import vlc
import time

VIDEO_PATH = "test2.mp4"

# Create VLC instance; keep it lean
# --no-video-title-show : hides filename overlay
# --quiet               : suppresses console spam
instance = vlc.Instance("--no-video-title-show --quiet")

player = instance.media_player_new()
media  = instance.media_new(VIDEO_PATH)
player.set_media(media)
player.play()

# Wait for playback to actually start
while player.get_state() not in (vlc.State.Playing, vlc.State.Paused):
    time.sleep(0.05)

# Manual seamless-loop logic
while True:
    length = player.get_length()
    pos = player.get_time()

    if length > 0 and (length - pos) < 150:   # restart ~0.15 s before end
        # restart media *without* tearing down the decoder
        player.set_media(media)
        player.play()
        time.sleep(0.15)  # small delay to avoid double-trigger
    time.sleep(0.02)
