# SiMP/src/simp/vlc_backend.py

import vlc
from pathlib import Path
from mutagen._file import File
from urllib.parse import urlparse, unquote

# Written in Helix btw.

class Player:
    def __init__(self) -> None:

        # Private attributes
        self._player = vlc.Instance()
        self._constants = Constants()
        self._playlist : vlc.MediaList = self._player.media_list_new()

        # Only 1 public-facing attribute
        self.queue = self._player.media_list_player_new()
        self.queue.set_playback_mode(self._constants.NORMAL)
        

    # The Player should handle:
    # 1) Loading the Playlist (A dir with no subdirs)
    # 2) Playing songs (Play, pause, stop, etc)
    # 3) Changing modes/playlists
    # 4) Exiting gracefully

    # Setting methods (playlists, etc.)

    def set_playlist(self, playlist_path : Path, index : int = 0) -> None:
        """
        Set given path to playlist if it is a valid playlist.
        """
        self._is_valid_playlist(playlist=playlist_path)

        playlist : vlc.MediaList = self._player.media_list_new()
        songlist = [
            path.as_posix() for path in playlist_path.iterdir()
            if path.suffix.lower() in self._constants.SUPPORTED_MEDIA_FILETYPES
        ]

        
        for song in songlist:
            playlist.add_media(song)
        
        if self.queue.is_playing():
            self.queue.stop()

        self.queue.set_media_list(playlist)
        if 0 <= index < playlist.count():
            self.queue.play_item_at_index(index)
            self._playlist = playlist
        else:
            raise PlayerError(f"Error: Invalid index {index}; length of playlist: {playlist.count()}")

    def set_mode(self, mode : str = "NORMAL") -> None:
        """
        Set mode based on string input.
        """
        match mode:
            case "NORMAL":
                self.queue.set_playback_mode(self._constants.NORMAL)
            case "LOOP":
                self.queue.set_playback_mode(self._constants.LOOP)
            case "REPEAT":
                self.queue.set_playback_mode(self._constants.REPEAT)
            case _:
                raise PlayerError(f"Error: Invalid Command: {mode}")


    # Metadata funcs. Unlike the others, these have return values.

    def get_current_song(self) -> Path | None:

        if self._playlist is None:
            return None

        media_player = self.queue.get_media_player()
        if not media_player:
            return None

        current_song = media_player.get_media()
        if not current_song:
            return None

        mrl = current_song.get_mrl()
        parsed = urlparse(mrl)

        if parsed.scheme != "file":
            return None
        
        path_str = unquote(parsed.path)
        return Path(path_str)

    def get_current_index(self) -> int:
        
        if self._playlist.count() == 0:
            return -1
        media_player = self.queue.get_media_player()
        index = self._playlist.index_of_item(media_player.get_media()) - 1 # Use 0 indexing

        return index if media_player else -1


    def read_metadata(self) -> dict[str, str]:
        song_path = self.get_current_song()
        if not song_path:
            return {
                "Error" : "No song currently playing."
            }

        # Replace leading `file://` if it exists

        song_path = Path(song_path).as_posix()
        
        if song_path.startswith("file://"):
            song_path = song_path.replace("file://","",1)

        audio = File(song_path,easy=True)

        if audio is None:
            return {
                "Error" : "Corrupted or unsupported filetype."
            }

        default = ["Unknown"]

        try:

            info = {
                "Title" : audio.get("title", [Path(song_path).stem])[0],
                "Artist" : audio.get("artist", default)[0],
                "Album" : audio.get("album", default)[0],
                "File" : Path(song_path).name
            }

            return info

        except Exception:

            return {
                "Title" : Path(song_path).stem,
                "Artist" : "Unknown",
                "Album" : "Unknown",
                "File" : Path(song_path).name
            }


    # Playback features. No comments here: they are mostly self-documenting.

    def play(self, index : int = 0) -> None:
        self._check_playlist_loaded()
        if 0 <= index < self._playlist.count():
            self.queue.play_item_at_index(index)
        else:
            raise PlayerError(f"Error: Invalid index for given playlist; index must be greater than or equal to 0 and less than {self._playlist.count()} for this playlist")


    def toggle_pause(self) -> None:
        self._check_playlist_loaded()
        self.queue.pause()
        
    def next(self) -> None:
        self._check_playlist_loaded()
        self.queue.next()

    def prev(self) -> None:
        self._check_playlist_loaded()
        self.queue.previous()

    def stop(self) -> None:
        self.queue.stop()

    # Private helper functions

    def _check_playlist_loaded(self) -> None:
        """
        Raises PlaylistNotLoadedError if current playlist has no supported files,
        causing self._playlist.count() to return 0.
        """
        if self._playlist.count() == 0:
            raise PlaylistNotLoadedError(f"Error: No playlist is loaded, or loaded playlist is empty. Please load a playlist with the following valid filetypes\n{
                                             [filetype for filetype in self._constants.SUPPORTED_MEDIA_FILETYPES]
                                         }")

    def _is_valid_playlist(self, playlist : Path) -> None:
        """
        Raises InvalidPlaylistError if playlist is not a flat directory.
        Use when updating existing playlist.
        """
        if not playlist.is_dir() or any([path.is_dir() for path in playlist.iterdir()]):
            raise InvalidPlaylistError(f"Error: A playlist must be a flat directory with the following file formats \n{
                             [filetype for filetype in self._constants.SUPPORTED_MEDIA_FILETYPES]
                         }.")

class Constants:
    def __init__(self) -> None:
        # Define constants; No magic numbers here, sir!
        self.NORMAL = vlc.PlaybackMode(0)
        self.LOOP = vlc.PlaybackMode(1)
        self.REPEAT = vlc.PlaybackMode(2)
        self.SUPPORTED_MEDIA_FILETYPES = frozenset({
            ".mp3",
            ".wav",
        })

        # Might add other filetypes later. Gotta ship MVP first.


# ++++++++++ EXCEPTIONS ++++++++++ #

class PlayerError(Exception):
    """Base exception for player-related errors."""
    pass

class PlaylistNotLoadedError(PlayerError):
    """Raised when an operation requires a playlist but none is loaded."""
    pass

class InvalidPlaylistError(PlayerError):
    """Raised when the playlist directory is invalid."""
    pass
