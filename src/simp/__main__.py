# ~/My_Projects/Python/SiMP/src/simp/__main__.py
import vlc
from pathlib import Path

def main() -> None:

    instance = vlc.Instance()
    player = instance.media_player_new()

    path : str
    
    while True:
        print("Press 'p' to toggle pause, 'e' to exit, 'c' to choose new song, 'l' to loop all songs:")
        cmd = input(">>> ")

        if cmd == "p":
            if not player.is_playing():
                player.play()
            else:
                player.pause()

        elif cmd == "e":
            player.stop()
            break

        elif cmd == "c":
            print("Searching...")
            search_here = Path("/Users/imsasankvindamuri/Music")
            all_songs = list(search_here.rglob("*.mp3")) + list(search_here.rglob("*.wav"))
            songlist = {i: song for i, song in enumerate(all_songs)}

            for i in songlist.keys():
                print(f"{i + 1} : {songlist[i].relative_to(search_here).as_posix()}")
            index = input("Choose a song via its index given in the left: ")

            songchoice = len(songlist)
            
            try:
                songchoice = int(index) - 1
            except ValueError:
                print("Error processing input")

            
            if not (songchoice < len(songlist) and songchoice >= 0):
                print("Input out of bounds...")

            else:
                path = rf"{songlist[songchoice].as_posix()}"

                if player.is_playing():
                    player.stop()

                media = instance.media_new(path)
                player.set_media(media)
                player.play()

                print(f"Now Playing... {path}")

        elif cmd == 'l':
            ...
            
        else:
            print("Invalid command.")
