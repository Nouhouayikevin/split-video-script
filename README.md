# Video Splitter

A Python script for splitting video files into segments of specified duration using ffmpeg with multi-threading support.

## Features

- Split videos into segments of any duration (in seconds)
- Multi-threaded processing for faster execution
- Reliable encoding with VP8 codec for WebM files
- Color-coded terminal output for better readability
- Real-time progress tracking
- Automatic output directory creation
- File size verification for each segment
- Optimized for speed while maintaining quality

## Prerequisites

### System Requirements

- **Python 3.6+** (standard library only, no external packages required)
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

#### Arch Linux
```bash
sudo pacman -S ffmpeg
```

### Verify Installation

Run the following commands to ensure ffmpeg is properly installed:

```bash
ffmpeg -version
ffprobe -version
```

Both commands should display version information without errors.

## Installation

### Clone the Repository
```bash
git clone git@github.com:Nouhouayikevin/split-video-script.git
cd video-splitter
```

### Make the Script Executable (Optional)
```bash
chmod +x split_video_script.py
```

No additional dependencies or virtual environment setup is required.

## Usage

### Basic Syntax
```bash
python3 split_video_script.py <video_filename> <segment_duration_seconds> [max_workers]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `video_filename` | Yes | Path to the video file (relative or absolute) |
| `segment_duration_seconds` | Yes | Duration of each segment in seconds (positive integer) |
| `max_workers` | No | Maximum number of concurrent workers (default: CPU count) |

### Examples

#### Split a video into 60-second segments
```bash
python3 split_video_script.py "recording.webm" 60
```

#### Split with custom thread count
```bash
python3 split_video_script.py "presentation.webm" 45 4
```

#### Using absolute paths
```bash
python3 split_video_script.py "/home/user/Videos/screencast.webm" 30
```

#### Using relative paths
```bash
python3 split_video_script.py "./videos/tutorial.webm" 120 2
```

## Output

### Directory Structure

All segments are saved in a `result/` directory, created automatically in the current working directory.

### Naming Convention

Segments are named sequentially with zero-padded numbers:

```
result/
├── video_name_segment_01.webm
├── video_name_segment_02.webm
├── video_name_segment_03.webm
└── ...
```

### Example Output

For a 5-minute video split into 60-second segments:

```
result/
├── my_video_segment_01.webm  (60.00 seconds, ~12 MB)
├── my_video_segment_02.webm  (60.00 seconds, ~12 MB)
├── my_video_segment_03.webm  (60.00 seconds, ~14 MB)
├── my_video_segment_04.webm  (60.00 seconds, ~14 MB)
├── my_video_segment_05.webm  (60.00 seconds, ~13 MB)
└── my_video_segment_06.webm  (5.24 seconds, ~1 MB)
```

## Terminal Output

The script provides color-coded output for better readability:

- **Yellow**: Informational messages (processing status, video info)
- **Green**: Success messages (completed segments)
- **Red**: Error messages (failures, missing files)
- **Bold**: Section headers and important information

### Sample Output

```
Loading video: my_video.webm
Video duration: 305.24 seconds (5.09 minutes)
Segment duration: 60 seconds
Creating 6 segments using multi-threading...

[Segment 1/6] Processing: 0.00s - 60.00s -> my_video_segment_01.webm
[Segment 2/6] Processing: 60.00s - 120.00s -> my_video_segment_02.webm
[Segment 1/6] Completed successfully (11.8 MB)
[Segment 3/6] Processing: 120.00s - 180.00s -> my_video_segment_03.webm
[Segment 2/6] Completed successfully (11.7 MB)
...

Summary:
Successful: 6/6
Output directory: /path/to/result
```

## Testing

### Quick Test

1. Prepare a test video file (or use an existing one)
2. Run the script with a short segment duration:
   ```bash
   python3 split_video_script.py "test_video.webm" 10
   ```
3. Verify the output:
   ```bash
   ls -lh result/
   ```
4. Play a segment to confirm it works:
   ```bash
   vlc result/test_video_segment_01.webm
   # or
   mpv result/test_video_segment_01.webm
   # or
   ffplay result/test_video_segment_01.webm
   ```

### Performance Testing

Test different worker counts to find optimal performance for your system:

```bash
# Single-threaded (slowest)
python3 split_video_script.py "video.webm" 60 1

# Dual-threaded
python3 split_video_script.py "video.webm" 60 2

# Quad-threaded
python3 split_video_script.py "video.webm" 60 4

# Auto (uses CPU count)
python3 split_video_script.py "video.webm" 60
```

## Technical Details

### Encoding Parameters

The script uses optimized ffmpeg parameters for WebM files:

| Parameter | Value | Description |
|-----------|-------|-------------|
| Video Codec | `libvpx` | VP8 codec (faster than VP9, good quality) |
| CRF | `10` | Constant Rate Factor (lower = better quality, range: 4-63) |
| Bitrate | `2M` | 2 Mbps target bitrate |
| CPU Used | `4` | Speed/quality balance (0=slowest/best, 5=fastest/worst) |

### Why Re-encoding?

WebM files lack regular keyframes, making accurate splitting with simple copy mode (`-c copy`) impossible. Re-encoding ensures:

- All segments are valid and playable
- Precise timing at segment boundaries
- No corruption or empty output files
- Consistent quality across all segments

### Multi-threading Benefits

Processing multiple segments concurrently significantly reduces total processing time:

| Segments | Sequential | 2 Workers | 4 Workers |
|----------|-----------|-----------|-----------|
| 6 segments | ~12 min | ~6-7 min | ~4-5 min |
| 10 segments | ~20 min | ~10-12 min | ~6-8 min |

**Note**: Actual performance depends on CPU capabilities and video complexity.

### Performance Metrics

Approximate processing times on a modern CPU (Intel i5/i7 or AMD Ryzen 5/7):

| Video Length | Resolution | Workers | Estimated Time |
|--------------|-----------|---------|----------------|
| 5 minutes | 1080p | 2 | 6-8 minutes |
| 5 minutes | 1080p | 4 | 4-6 minutes |
| 10 minutes | 1080p | 2 | 12-16 minutes |
| 10 minutes | 1080p | 4 | 8-12 minutes |

Processing speed varies based on:
- CPU performance and core count
- Video resolution and bitrate
- Content complexity (static vs. dynamic scenes)
- Available system resources

## Troubleshooting

### Common Issues

#### Error: "ffprobe not found"

**Cause**: ffmpeg is not installed or not in PATH.

**Solution**: Install ffmpeg using your package manager (see Prerequisites section).

#### Error: "Video file not found"

**Cause**: Incorrect file path or filename.

**Solution**: 
- Verify the file exists: `ls -l "video.webm"`
- Use quotes around filenames with spaces: `"my video.webm"`
- Use absolute paths if relative paths fail

#### Segments are empty (0 bytes)

**Cause**: This script uses re-encoding to prevent this issue, but it can occur if ffmpeg lacks codec support.

**Solution**:
1. Verify libvpx support: `ffmpeg -codecs | grep vpx`
2. Test the original video: `ffplay video.webm`
3. Check ffmpeg error output in the terminal

#### Script is too slow

**Solutions**:
1. Increase worker count: `python3 split_video_script.py video.webm 60 4`
2. Reduce quality (edit script):
   - Change `-crf` from `'10'` to `'20'` (line 90)
   - Change `-cpu-used` from `'4'` to `'5'` (line 92)
   - Reduce bitrate from `'2M'` to `'1M'` (line 91)

#### Out of disk space

**Cause**: Insufficient storage for output files.

**Solution**: 
- Check available space: `df -h .`
- Output files are roughly the same total size as input
- Free up space or use a different output location

#### Permission denied

**Cause**: No write permission in current directory.

**Solution**:
- Check permissions: `ls -ld .`
- Run from a directory where you have write access
- Or modify the script to use a different output directory

## Advanced Usage

### Custom Output Directory

Modify line 119 in the script to change the output directory:

```python
result_dir = Path("/custom/path/to/output")
```

### Adjust Quality Settings

Edit the ffmpeg command parameters (lines 88-92) to customize encoding:

```python
'-crf', '10',      # Quality: 4 (best) to 63 (worst)
'-b:v', '2M',      # Bitrate: adjust based on needs
'-cpu-used', '4',  # Speed: 0 (slow/best) to 5 (fast/worst)
```

### Process Multiple Videos

Create a simple bash script:

```bash
#!/bin/bash
for video in *.webm; do
    python3 split_video_script.py "$video" 60 4
done
```

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Author

Created for efficiently splitting screencast recordings and long videos into manageable segments.

## Acknowledgments

- Built with [ffmpeg](https://ffmpeg.org/)
- Uses VP8 codec from the [WebM Project](https://www.webmproject.org/)
- Multi-threading implemented with Python's `concurrent.futures`

---

**For issues, questions, or feature requests, please open an issue on GitHub.**
