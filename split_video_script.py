#!/usr/bin/env python3
"""
Video Splitter - Split video files into segments using ffmpeg with multi-threading support.
"""
import sys
import os
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# ANSI color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Thread-safe print lock
print_lock = threading.Lock()

def print_error(message):
    """Print error message in red."""
    with print_lock:
        print(f"{Colors.RED}{message}{Colors.RESET}")

def print_success(message):
    """Print success message in green."""
    with print_lock:
        print(f"{Colors.GREEN}{message}{Colors.RESET}")

def print_info(message):
    """Print info message in yellow."""
    with print_lock:
        print(f"{Colors.YELLOW}{message}{Colors.RESET}")

def print_normal(message):
    """Print normal message."""
    with print_lock:
        print(message)

def get_video_duration(video_path):
    """Get video duration using ffprobe."""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except subprocess.CalledProcessError:
        print_error("Error: Could not get video duration. Is ffprobe installed?")
        sys.exit(1)
    except FileNotFoundError:
        print_error("Error: ffprobe not found. Please install ffmpeg.")
        sys.exit(1)

def process_segment(segment_info):
    """
    Process a single video segment.
    
    Args:
        segment_info: Tuple containing (segment_number, total_segments, start_time, 
                      end_time, duration, video_path, output_filename)
    
    Returns:
        Tuple of (success: bool, segment_number: int, file_size: int, error_message: str)
    """
    seg_num, total_segs, start_time, end_time, duration, video_path, output_filename = segment_info
    
    print_info(f"[Segment {seg_num}/{total_segs}] Processing: {start_time:.2f}s - {end_time:.2f}s -> {output_filename.name}")
    
    cmd = [
        'ffmpeg',
        '-ss', str(start_time),
        '-i', video_path,
        '-t', str(duration),
        '-c:v', 'libvpx',
        '-crf', '10',
        '-b:v', '2M',
        '-cpu-used', '4',
        '-y',
        '-loglevel', 'error',
        '-stats',
        str(output_filename)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        
        if output_filename.exists() and output_filename.stat().st_size > 1000:
            file_size = output_filename.stat().st_size
            return (True, seg_num, file_size, None)
        else:
            return (False, seg_num, 0, "Output file is too small or empty")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else str(e)
        return (False, seg_num, 0, error_msg)
    except Exception as e:
        return (False, seg_num, 0, str(e))

def split_video_script(video_path, segment_duration, max_workers=None):
    """
    Split video into segments using multi-threading.
    
    Args:
        video_path: Path to the input video file
        segment_duration: Duration of each segment in seconds
        max_workers: Maximum number of concurrent workers (default: CPU count)
    """
    if not os.path.exists(video_path):
        print_error(f"Error: Video file '{video_path}' not found.")
        sys.exit(1)
    
    result_dir = Path("result")
    result_dir.mkdir(exist_ok=True)
    
    video_name = Path(video_path).stem
    video_ext = Path(video_path).suffix
    
    print_normal(f"\nLoading video: {Colors.BOLD}{video_path}{Colors.RESET}")
    total_duration = get_video_duration(video_path)
    
    print_info(f"Video duration: {total_duration:.2f} seconds ({total_duration/60:.2f} minutes)")
    print_info(f"Segment duration: {segment_duration} seconds")
    
    num_segments = int(total_duration // segment_duration) + (1 if total_duration % segment_duration > 0 else 0)
    print_info(f"Creating {num_segments} segments using multi-threading...\n")
    
    # Prepare segment information
    segments = []
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = min((i + 1) * segment_duration, total_duration)
        duration = end_time - start_time
        output_filename = result_dir / f"{video_name}_segment_{i+1:02d}{video_ext}"
        
        segments.append((i+1, num_segments, start_time, end_time, duration, video_path, output_filename))
    
    # Process segments concurrently
    successful = 0
    failed = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_segment, seg): seg for seg in segments}
        
        for future in as_completed(futures):
            success, seg_num, file_size, error_msg = future.result()
            
            if success:
                print_success(f"[Segment {seg_num}/{num_segments}] Completed successfully ({file_size / 1024 / 1024:.1f} MB)")
                successful += 1
            else:
                print_error(f"[Segment {seg_num}/{num_segments}] Failed: {error_msg}")
                failed += 1
    
    # Summary
    print_normal(f"\n{Colors.BOLD}Summary:{Colors.RESET}")
    print_success(f"Successful: {successful}/{num_segments}")
    if failed > 0:
        print_error(f"Failed: {failed}/{num_segments}")
    print_info(f"Output directory: {result_dir.absolute()}\n")
    
    if failed > 0:
        sys.exit(1)

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print_normal(f"{Colors.BOLD}Usage:{Colors.RESET} python split_video_script.py <video_filename> <segment_duration_seconds> [max_workers]")
        print_normal(f"\n{Colors.BOLD}Arguments:{Colors.RESET}")
        print_normal("  video_filename          Path to the video file")
        print_normal("  segment_duration        Duration of each segment in seconds")
        print_normal("  max_workers (optional)  Maximum number of concurrent workers (default: CPU count)")
        print_normal(f"\n{Colors.BOLD}Example:{Colors.RESET}")
        print_normal('  python split_video_script.py "video.webm" 60')
        print_normal('  python split_video_script.py "video.webm" 60 4\n')
        sys.exit(1)
    
    video_filename = sys.argv[1]
    
    try:
        segment_duration = int(sys.argv[2])
        if segment_duration <= 0:
            raise ValueError("Segment duration must be positive")
    except ValueError:
        print_error("Error: Invalid segment duration. Please provide a positive integer.")
        sys.exit(1)
    
    max_workers = None
    if len(sys.argv) == 4:
        try:
            max_workers = int(sys.argv[3])
            if max_workers <= 0:
                raise ValueError("Max workers must be positive")
        except ValueError:
            print_error("Error: Invalid max_workers value. Please provide a positive integer.")
            sys.exit(1)
    
    split_video_script(video_filename, segment_duration, max_workers)

if __name__ == "__main__":
    main()
