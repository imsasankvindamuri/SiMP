# SiMP/src/simp/__main__.py

from simp.vlc_backend import Player, PlayerError, PlaylistNotLoadedError
from pathlib import Path



def main() -> None:
    player = Player()

    music_dir = Path().home() / "Music"

    print("Welcome to SiMP - The Simple Music Player")
    print(f"Default music directory: {music_dir.as_posix()}")
    print("Type 'help' to see available commands.")
    def show_now_playing():
        """Helper to display current song info"""
        if song := player.get_current_song():
            idx = player.get_current_index()
            print(f"\nNow playing [{idx+1}]: {Path(song).name}")
        else:
            print("\nNo song currently playing")

    while True:
        cmd = input(">>> ").strip().lower()

        match cmd:
            case "play":
                try:
                    index = int(input("Enter song index (default 0): ") or "0")
                    player.play(index)
                except ValueError:
                    print("Invalid index.")
                except PlaylistNotLoadedError as e:
                    print(e)

            case "pause":
                try:
                    player.toggle_pause()
                except PlaylistNotLoadedError as e:
                    print(e)

            case "stop":
                player.stop()

            case "exit":
                player.stop()
                print("Goodbye.")
                break

            case "load":
                print("Enter path to playlist folder (flat directory of music files):")
                p = input(">>> ").strip()
                try:
                    path = Path(p).expanduser().resolve()
                    player.set_playlist(path)
                    print(f"Loaded playlist: {path.as_posix()}")
                except PlayerError as e:
                    print(e)

            case "mode":
                print("Available modes: NORMAL, LOOP, REPEAT")
                mode = input("Enter mode: ").strip().upper()
                try:
                    player.set_mode(mode)
                    print(f"Mode set to {mode}")
                except PlayerError as e:
                    print(e)

            case "next":
                try:
                    player.next()
                except PlaylistNotLoadedError as e:
                    print(e)

            case "prev":
                try:
                    player.prev()
                except PlaylistNotLoadedError as e:
                    print(e)

            case "now":
                show_now_playing()

            case "help":
                print("""
Available commands:
  load   - Load a playlist directory
  play   - Play track at index
  pause  - Toggle pause
  stop   - Stop playback
  mode   - Change playback mode
  next   - Play next track
  prev   - Play previous track
  exit   - Exit the player
  now    - Show current song
  help   - Show this message
                """)

            case _:
                print("Unknown command. Type 'help' for a list of commands.")
