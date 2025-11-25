# 🎬 Video Splitter

A Python script to split video files into smaller segments of specified duration using ffmpeg.

## 📋 Features

- ✂️ Split videos into segments of any duration (in seconds)
- 🎯 Reliable encoding with VP8 codec for WebM files
- 📊 Real-time progress display
- 🗂️ Automatic output directory creation
- ✅ File size verification for each segment
- 🚀 Optimized for speed while maintaining quality

## 🔧 Prerequisites

### System Requirements

- **Python 3.6+** (usually pre-installed on most Linux distributions)
- **ffmpeg** with libvpx support

### Installing ffmpeg

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Fedora
```bash
sudo dnf install ffmpeg
```

#### macOS
```bash
brew install ffmpeg
```

#### Verify Installation
```bash
ffmpeg -version
ffprobe -version
```

Both commands should display version information without errors.

## 📥 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/video-splitter.git
cd video-splitter
```

### 2. (Optional) Create a Virtual Environment

While not strictly necessary (the script only uses standard library + ffmpeg), you can create a virtual environment for isolation:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Linux/macOS
# OR
venv\Scripts\activate     # On Windows
```

### 3. Make the Script Executable (Optional)
```bash
chmod +x split_video.py
```

## 🚀 Usage

### Basic Syntax
```bash
python3 split_video.py <video_filename> <segment_duration_seconds>
```

### Examples

#### Split a 5-minute video into 60-second segments
```bash
python3 split_video.py "my_video.webm" 60
```

#### Split a screencast into 45-second segments
```bash
python3 split_video.py "Screencast from 2025-11-21 01-33-35.webm" 45
```

#### Using relative or absolute paths
```bash
# Relative path
python3 split_video.py "./videos/recording.webm" 30

# Absolute path
python3 split_video.py "/home/user/Videos/presentation.webm" 120
```

## 📁 Output

### Output Directory
All segments are saved in a `result/` directory (created automatically if it doesn't exist).

### Naming Convention
Segments are named with a sequential number:
```
original_video_segment_01.webm
original_video_segment_02.webm
original_video_segment_03.webm
...
```

### Example Output
For a 5-minute video split into 60-second segments:
```
result/
├── my_video_segment_01.webm  (60 seconds)
├── my_video_segment_02.webm  (60 seconds)
├── my_video_segment_03.webm  (60 seconds)
├── my_video_segment_04.webm  (60 seconds)
├── my_video_segment_05.webm  (60 seconds)
└── my_video_segment_06.webm  (5.24 seconds - remainder)
```

## 🧪 Testing

### Test with a Sample Video

1. **Download or create a test video** (or use your own):
   ```bash
   # Example: Record a short screencast or use an existing video
   ```

2. **Run the script**:
   ```bash
   python3 split_video.py "test_video.webm" 10
   ```

3. **Verify the output**:
   ```bash
   ls -lh result/
   ```
   
   You should see multiple segment files with reasonable sizes (not 0 bytes).

4. **Play a segment** to verify it works:
   ```bash
   vlc result/test_video_segment_01.webm
   # OR
   mpv result/test_video_segment_01.webm
   # OR
   ffplay result/test_video_segment_01.webm
   ```

### Expected Behavior

When you run the script, you should see output like this:

```
🎬 Loading video: test_video.webm
⏱️  Video duration: 305.24 seconds (5.09 minutes)
✂️  Segment duration: 60 seconds
📦 Creating 6 segments...
⚠️  Note: Ré-encodage nécessaire pour webm (prendra quelques minutes)

⏳ Segment 1/6: 0.00s - 60.00s -> result/test_video_segment_01.webm
frame=  1500 fps= 25 q=10.0 size=   11264kB time=00:00:59.99 bitrate=1536.5kbits/s speed=1.0x
✅ Segment 1/6 terminé! (11.8 MB)

⏳ Segment 2/6: 60.00s - 120.00s -> result/test_video_segment_02.webm
...
```

## ⚙️ Technical Details

### Encoding Settings

The script uses the following ffmpeg parameters for optimal balance between speed and quality:

- **Video Codec**: `libvpx` (VP8) - faster than VP9, good quality
- **CRF**: `10` (Constant Rate Factor) - excellent quality (lower = better, range: 4-63)
- **Bitrate**: `2M` (2 Mbps) - good quality for most screencasts
- **CPU Used**: `4` - balanced speed/quality (range: 0-5, higher = faster but lower quality)

### Why Re-encoding?

WebM files don't have regular keyframes, making it impossible to split them accurately using simple copy mode (`-c copy`). Re-encoding ensures:
- ✅ All segments are valid and playable
- ✅ Precise timing at segment boundaries
- ✅ No corruption or empty files

### Performance

Approximate processing times (on a modern CPU):
- **1 minute of 1080p video**: ~1-2 minutes
- **5 minutes of 1080p video**: ~6-12 minutes
- **10 minutes of 1080p video**: ~12-25 minutes

Processing speed depends on:
- CPU performance
- Video resolution
- Video complexity (static vs. dynamic content)

## 🐛 Troubleshooting

### Error: "ffprobe not found"
**Solution**: Install ffmpeg (see Prerequisites section)

### Error: "Video file not found"
**Solution**: Check the file path. Use quotes around filenames with spaces:
```bash
python3 split_video.py "my video.webm" 60
```

### Segments are empty (0 bytes)
**Solution**: This script uses re-encoding to avoid this issue. If you still encounter it:
1. Verify your ffmpeg installation supports libvpx: `ffmpeg -codecs | grep vpx`
2. Check the original video plays correctly: `ffplay your_video.webm`

### Script is too slow
**Solutions**:
- Increase `-cpu-used` value (edit line 92 in the script, change `'4'` to `'5'`)
- Lower the quality: change `-crf` from `'10'` to `'20'` (line 90)
- Use a lower bitrate: change `'2M'` to `'1M'` (line 91)

### Out of disk space
**Solution**: The output files will be roughly the same total size as the input. Ensure you have enough free space:
```bash
df -h .
```

## 📝 Script Parameters Explained

### Command Line Arguments

1. **video_filename** (required)
   - The path to your video file
   - Can be relative or absolute
   - Use quotes if the filename contains spaces

2. **segment_duration_seconds** (required)
   - Duration of each segment in seconds
   - Must be a positive integer
   - Examples: `30`, `45`, `60`, `120`

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

Created for splitting screencast recordings and long videos into manageable segments.

## 🙏 Acknowledgments

- Built with [ffmpeg](https://ffmpeg.org/)
- Uses VP8 codec from the [WebM Project](https://www.webmproject.org/)

---

**Happy video splitting! 🎬✂️**
