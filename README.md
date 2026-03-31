# Craft Listen 🎧

A simple Python-based graphical audio player specifically tailored for Japanese Language Proficiency Test (JLPT) listening practice tracks. It features a fun, Minecraft-style pixelated UI to make studying a bit more enjoyable.

## Features

- **Minecraft-style Pixelated UI**: Enjoy a cool, retro blocky interface while you practice.
- **Sequential playback**: Plays through your `.mp3` tracks one by one.
- **Interactive UI**: Simple graphical buttons to Play, Pause, Stop, skip to Next or go back to Previous track.
- **Batch Renamer Utility**: Includes a script (`rename_files.py`) for quickly renaming files (e.g., removing long specific prefixes like `shinkanzen_chokai_n4_` from bulk downloaded tracks).

## Prerequisites

- Python 3.7+
- `pygame` library (handles audio playback without cluttering your screen)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/CraftListen.git
   cd CraftListen
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Add your audio files**: Place your `.mp3` listening practice tracks inside the `music/` folder.
2. **Launch the player**:
   ```bash
   python main.py
   ```
3. Follow the on-screen terminal commands to navigate through your tracklist.

## Using the File Renamer

If you have bulk-downloaded files with long prefixes (e.g., `shinkanzen_chokai_n4_CD-A_010.mp3`), you can easily clean up their names using the included utility script:

```bash
python rename_files.py
```

*Note: You may want to edit `rename_files.py` to match the specific prefix you need removed from your own files.*

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

## License

This project is licensed under the MIT License.
