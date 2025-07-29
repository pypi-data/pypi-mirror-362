# ncmpeg

**ncmpeg** is a terminal-based UI for [FFmpeg](https://ffmpeg.org/), built with Python and `ncurses`.  
It removes the need to memorize long command-line flags and gives you a fast, minimal way to handle common media tasks directly from your terminal.

## Features

### Video
- Convert formats
- Cut by start and end time
- Merge multiple video files
- Resize, crop, rotate or flip
- Burn hardcoded `.srt` subtitles
- Extract frames to PNG
- Generate GIFs
- Change playback speed (with audio)
- Overlay an image or watermark
- Strip metadata
- Display video info using ffprobe

### Audio
- Extract audio from video
- Adjust volume
- Normalize loudness
- Change audio playback speed
- Strip metadata
- Display audio info using ffprobe

## Installation

Install via pip:

```bash
pip install ncmpeg
```

Then run the app:

```bash
ncmpeg
```

To install from source:

```bash
git clone https://github.com/bearenbey/ncmpeg.git
cd ncmpeg
pip install .
ncmpeg
```

Dependencies:
- Python 3.8 or higher
- FFmpeg and ffprobe installed and available on your system

## Usage

- Use `↑ ↓` to navigate through operations or files
- Use `Tab` to switch between the operations panel and the file panel
- Press `Enter` to select or confirm
- Press `Esc` to cancel input
- Press `q` to quit the app

The file panel shows the current working directory. You can refer to it while filling in filenames or parameters on the left.

## License

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, either version 3 of the License, or  
(at your option) any later version.

This program is distributed in the hope that it will be useful,  
but WITHOUT ANY WARRANTY; without even the implied warranty of  
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the  
GNU General Public License for more details.

You should have received a copy of the GNU General Public License  
along with this program. If not, see <https://www.gnu.org/licenses/>.

© 2025 Eren Öğrül [termapp@pm.me](mailto:termapp@pm.me)