import vlc
import os
# os.system("vcgencmd display_power 1")

current_video = None

instance = vlc.Instance()

player = instance.media_player_new()

# load two videos
video1 = vlc.Media("test1.mp4")
video2 = vlc.Media("test2.mp4")

def play_video(player, video):
    # need to call set_media() to (re)load a vid before playing
    player.set_media(video)
    player.play()

# start player
play_video(player, video1)
current_video = video1
next_video = video2


while True:
    if player.get_state() ==  vlc.State.Ended:
        play_video(player, next_video)
        current_video, next_video = next_video, current_video