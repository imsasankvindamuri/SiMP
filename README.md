# SiMP - The Simple Music Player

A privacy-respecting, terminal-based music player that follows the UNIX philosophy: everything is a file.

## Philosophy

SiMP treats your music collection the way it should be treated - as files on your filesystem.
Playlists are simply directories containing music files. No databases, no vendor lock-in, no cloud
synchronization of your listening habits. Just you, your music, and a clean interface.

## Features

- **Directory-based playlists**: Your playlists are just folders with music files
- **Offline-first**: Designed for locally stored music files
- **Privacy-respecting**: No telemetry, no data collection, no internet required
- **Multiple playback modes**: Normal, Loop (repeat all), and Repeat (repeat one)
- **Metadata support**: Reads ID3 tags and other metadata from your files
- **Cross-platform**: Works on macOS, Linux, and Windows
- **Terminal-based**: Lightweight and keyboard-driven interface

## Current Status

**Version 0.0.3** - Core backend functionality complete, basic REPL interface available.

- ✅ Core playback engine
- ✅ Playlist management (directory-based)
- ✅ Playback modes (Normal/Loop/Repeat)
- ✅ Metadata reading
- ✅ Navigation (next/previous with mode preservation)
- 🚧 Terminal User Interface (coming in v0.1.0)
- 🚧 Bluetooth audio device handling (coming in v0.1.0)

## Installation

### System Requirements

1. **VLC Media Player** must be installed on your system:
   - **macOS (Homebrew)**: `brew install vlc`
   - **Ubuntu/Debian**: `sudo apt install vlc`
   - **Fedora**: `sudo dnf install vlc`
   - **Windows**: Download from [videolan.org](https://www.videolan.org/vlc/)

2. **Python 3.13+** (check with `python --version`)

3. **`pipx`** (Download with system package manager or with `pip` as shown with **VLC Media Player.**)

### Install SiMP

```bash
# Clone the repository
git clone https://github.com/yourusername/simp.git
cd SiMP

# Install with pipx (recommended)
pipx install .
```

## Usage

### Basic Commands (Current REPL Interface)

```bash
# Start SiMP
simp

# Available commands in the REPL:
- load   = Load a playlist directory
- play   = Play track at index
- pause  = Toggle pause
- stop   = Stop playback
- mode   = Change playback mode
- next   = Play next track
- prev   = Play previous track
- exit   = Exit the player
- now    = Show current song
- mdata  = Show metadata of current song
- help   = Show the help message
```

### Setting Up Your Music

SiMP uses a simple directory structure for playlists:

```
~/Music/
├── Chill Playlist/
│   ├── song1.mp3
│   ├── song2.wav
│   └── song3.mp3
├── Rock Collection/
│   ├── track1.mp3
│   └── track2.mp3
└── Study Music/
    ├── focus1.mp3
    └── focus2.mp3
```

Each directory becomes a playlist. Just point SiMP to any directory and it will treat all supported audio files
as a playlist.

## Supported File Formats

Currently supported (more formats planned for v0.1.0):
- MP3 (`.mp3`)
- WAV (`.wav`)

## Development

### Project Structure

```
SiMP/
├── src/simp/
│   ├── __init__.py
│   ├── __main__.py      # Entry point and REPL interface
│   └── vlc_backend.py   # Core Player class
├── pyproject.toml
└── README.md
```

### Architecture

SiMP is built around a clean separation of concerns:

- **`Player` class**: Core audio playback functionality using VLC backend
- **Context managers**: Safe temporary mode switching for navigation
- **Exception handling**: Comprehensive error handling for edge cases
- **UNIX philosophy**: Leverage filesystem as the database

## Roadmap

### v0.1.0 - Consumer Ready
- [ ] Full Terminal User Interface (TUI) using Textual
- [ ] Better audio device handling (Bluetooth disconnect detection)
- [ ] More file format support (FLAC, OGG, AAC, M4A)
- [ ] Playlist management commands
- [ ] Configuration file support

### v0.2.0 - Enhanced Features
- [ ] Shuffle mode
- [ ] Queue management
- [ ] Search functionality
- [ ] Keyboard shortcuts customization
- [ ] Volume control

### v1.0.0 - Stable Release
- [ ] Plugin system
- [ ] Theming support
- [ ] Advanced metadata handling
- [ ] Performance optimizations

## Contributing

SiMP is open source and welcomes contributions! Whether it's:

- Bug reports and feature requests
- Documentation improvements  
- Code contributions
- Testing on different platforms

Please feel free to open issues or submit pull requests.

## Philosophy & Design Principles

1. **Files are the API**: Your filesystem organization IS your music organization
2. **Privacy first**: No telemetry, no cloud, no tracking
3. **UNIX philosophy**: Do one thing well, compose with other tools
4. **Fail gracefully**: Comprehensive error handling and recovery
5. **Developer experience**: "Would I be able to debug this while sleep-deprived?"

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Built with [python-vlc](https://github.com/oaubert/python-vlc) for robust audio playback
- Metadata handling powered by [Mutagen](https://github.com/quodlibet/mutagen)
- Written in [Helix](https://helix-editor.com/) btw 😉

---

**Note**: SiMP is currently in active development. The REPL interface is functional but basic.
A full TUI is coming in v0.1.0. Feedback and testing are greatly appreciated!
