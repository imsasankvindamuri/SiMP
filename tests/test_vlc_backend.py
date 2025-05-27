import pytest
from pathlib import Path
from simp.vlc_backend import Player, PlayerError, PlaylistNotLoadedError, InvalidPlaylistError

from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_player():
    with patch("simp.vlc_backend.vlc.Instance") as mock_instance:
        instance = mock_instance.return_value
        instance.media_list_player_new.return_value = MagicMock()
        instance.media_list_new.return_value = MagicMock()
        return Player()


def test_invalid_playlist_path_raises_error(mock_player):
    with pytest.raises(InvalidPlaylistError):
        mock_player.set_playlist(Path("/nonexistent/path"))


def test_valid_playlist_but_contains_subdirs(mock_player, tmp_path):
    # Create a subdirectory inside the playlist path
    (tmp_path / "subdir").mkdir()
    with pytest.raises(InvalidPlaylistError):
        mock_player.set_playlist(tmp_path)


def test_empty_playlist_folder_sets_no_media(mock_player, tmp_path):
    with patch.object(mock_player.queue, "set_media_list") as set_list:
        mock_player._playlist = MagicMock()
        mock_player._playlist.count.return_value = 0  # already done

        with patch.object(mock_player._player, "media_list_new") as mocked_media_list_new:
            mock_media_list = MagicMock()
            mock_media_list.count.return_value = 0
            mocked_media_list_new.return_value = mock_media_list

            with patch.object(mock_player.queue, "is_playing", return_value=False):
                mock_player.set_playlist(tmp_path)



def test_set_mode_valid(mock_player):
    for mode in ["NORMAL", "LOOP", "REPEAT"]:
        mock_player.set_mode(mode)  # should not raise


def test_set_mode_invalid(mock_player):
    with pytest.raises(PlayerError):
        mock_player.set_mode("SHUFFLE")


def test_get_current_song_returns_empty(mock_player):
    mock_player._playlist.count = MagicMock(return_value=0)
    assert mock_player.get_current_song() == ""


def test_get_current_index_returns_negative_one(mock_player):
    mock_player._playlist.count = MagicMock(return_value=0)
    assert mock_player.get_current_index() == -1


def test_play_without_playlist_raises(mock_player):
    mock_player._playlist.count = MagicMock(return_value=0)
    with pytest.raises(PlaylistNotLoadedError):
        mock_player.play()


def test_pause_without_playlist_raises(mock_player):
    mock_player._playlist.count = MagicMock(return_value=0)
    with pytest.raises(PlaylistNotLoadedError):
        mock_player.toggle_pause()


def test_next_without_playlist_raises(mock_player):
    mock_player._playlist.count = MagicMock(return_value=0)
    with pytest.raises(PlaylistNotLoadedError):
        mock_player.next()


def test_prev_without_playlist_raises(mock_player):
    mock_player._playlist.count = MagicMock(return_value=0)
    with pytest.raises(PlaylistNotLoadedError):
        mock_player.prev()


def test_stop_does_not_crash(mock_player):
    mock_player.stop()  # should not raise


def test_set_playlist_out_of_range_index(mock_player, tmp_path):
    with patch.object(mock_player._player, "media_list_new") as mocked_media_list_new:
        mock_media_list = MagicMock()
        mock_media_list.count.return_value = 1  # assume 1 valid song in dir
        mocked_media_list_new.return_value = mock_media_list

        with patch.object(mock_player.queue, "is_playing", return_value=False):
            with pytest.raises(PlayerError):
                mock_player.set_playlist(tmp_path, index=5)


def test_constants_supported_filetypes():
    from simp.vlc_backend import Constants
    c = Constants()
    assert ".mp3" in c.SUPPORTED_MEDIA_FILETYPES
    assert ".wav" in c.SUPPORTED_MEDIA_FILETYPES

