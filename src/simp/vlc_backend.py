# SiMP/src/simp/vlc_backend.py

import vlc
from pathlib import Path

# Written in Helix btw.

class Player:
    def __init__(self) -> None:
        
        self._player = vlc.Instance()
        self._constants = Constants()
        self.queue = self._player.media_list_player_new()
        self._playlist : vlc.MediaList = self._player.media_list_new()
        self.queue.set_playback_mode(self._constants.NORMAL)
        

    # The Player should handle:
    # 1) Loading the Playlist (A dir with no subdirs)
    # 2) Playing songs (Play, pause, stop, etc)
    # 3) Changing modes/playlists
    # 4) Exiting gracefully

    def _is_valid_playlist(self, playlist : Path) -> None:
        if not playlist.is_dir() or any([path.is_dir() for path in playlist.iterdir()]):
            raise InvalidPlaylistError(f"Error: A playlist must be a flat directory with only the following file formats \n{
                             [filetype for filetype in self._constants.SUPPORTED_MEDIA_FILETYPES]
                         }.")

    def set_playlist(self, playlist_path : Path, index : int = 0) -> None:
        self._is_valid_playlist(playlist=playlist_path)

        playlist : vlc.MediaList = self._player.media_list_new()
        songlist = [
            path.as_posix() for path in playlist_path.iterdir()
            if path.suffix.lower() in self._constants.SUPPORTED_MEDIA_FILETYPES
        ]

        # Why path.as_posix() and not a cross platform soln.?
        # Because I really don't know how I can make this
        # truly cross platform
        #
        # Also fuck MSFT.

        for song in songlist:
            playlist.add_media(song)
        
        if self.queue.is_playing():
            self.queue.stop()

        self.queue.set_media_list(playlist)
        if 0 <= index <= playlist.count():
            self.queue.play_item_at_index(index)
            self._playlist = playlist
        else:
            raise PlayerError(f"Error: Invalid index {index}; length of playlist: {playlist.count()}")

    def get_current_song(self) -> str:
        """Returns the currently playing song's path or empty string if none"""
        if self._playlist.count() == 0:
            return ""
    
        media_player = self.queue.get_media_player()
        if not media_player:
            return ""
    
        current_media = media_player.get_media()
        return current_media.get_mrl() if current_media else ""

    def get_current_index(self) -> int:
        """Returns current song index or -1 if none"""
        if self._playlist.count() == 0:
            return -1
        media_player = self.queue.get_media_player()
        return self._playlist.index_of_item(media_player.get_media()) if media_player else -1


    def set_mode(self, mode : str = "NORMAL") -> None:
        match mode:
            case "NORMAL":
                self.queue.set_playback_mode(self._constants.NORMAL)
            case "LOOP":
                self.queue.set_playback_mode(self._constants.LOOP)
            case "REPEAT":
                self.queue.set_playback_mode(self._constants.REPEAT)
            case _:
                raise PlayerError(f"Error: Invalid Command: {mode}")

    def play(self, index : int = 0) -> None:
        if self._playlist.count() == 0:
            raise PlaylistNotLoadedError(f"Error: No playlist is loaded, or loaded playlist is empty. Please load a playlist with the following valid filetypes\n{
                                             [filetype for filetype in self._constants.SUPPORTED_MEDIA_FILETYPES]
                                         }")
        self.queue.play_item_at_index(index)

    def toggle_pause(self) -> None:
        if self._playlist.count() == 0:
            raise PlaylistNotLoadedError(f"Error: No playlist is loaded, or loaded playlist is empty. Please load a playlist with the following valid filetypes\n{
                                             [filetype for filetype in self._constants.SUPPORTED_MEDIA_FILETYPES]
                                         }")
        self.queue.pause()
        
    def next(self) -> None:
        if self._playlist.count() == 0:
            raise PlaylistNotLoadedError(f"Error: No playlist is loaded, or loaded playlist is empty. Please load a playlist with the following valid filetypes\n{
                                             [filetype for filetype in self._constants.SUPPORTED_MEDIA_FILETYPES]
                                         }")
        self.queue.next()

    def prev(self) -> None:
        if self._playlist.count() == 0:
            raise PlaylistNotLoadedError(f"Error: No playlist is loaded, or loaded playlist is empty. Please load a playlist with the following valid filetypes\n{
                                             [filetype for filetype in self._constants.SUPPORTED_MEDIA_FILETYPES]
                                         }")
        self.queue.previous()

    def stop(self) -> None:
        self.queue.stop()


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

class NoActiveTrackError(PlayerError):
    """Raised when trying to pause/stop without a playing track."""
    pass

class InvalidPlaylistError(PlayerError):
    """Raised when the playlist directory is invalid."""
    pass
