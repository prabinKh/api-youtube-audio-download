# video_downloader/utils.py
import os
import subprocess
import re
import logging
import tempfile
from django.conf import settings
from pathlib import Path

logger = logging.getLogger(__name__)

def download_audio(video_url, name):
    """
    Download audio from a video URL using yt-dlp via subprocess and return the path to the mp3 file.
    
    Args:
        video_url (str): URL of the video to download audio from.
        name (str): Name to use for the output file.
    
    Returns:
        str: Path to the downloaded mp3 file, or None if download fails.
    """
    logger.info(f"Starting download for video: {video_url} with name: {name}")
    
    if not video_url or not name:
        logger.error("Invalid input: video_url and name must be provided")
        return None
    
    try:
        output_dir = os.path.join(settings.MEDIA_ROOT, 'audio', 'temp')
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Using output directory: {output_dir}")
    except Exception as e:
        logger.error(f"Failed to create output directory {output_dir}: {str(e)}")
        return None

    sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    output_template = os.path.join(output_dir, f"{sanitized_name}.%(ext)s")
    absolute_audio_path = os.path.join(output_dir, f"{sanitized_name}.mp3")
    
    if os.path.exists(absolute_audio_path):
        try:
            os.remove(absolute_audio_path)
            logger.info(f"Removed existing file at {absolute_audio_path}")
        except Exception as e:
            logger.warning(f"Failed to remove existing file: {str(e)}")

    command = [
        'yt-dlp',
        '-x', 
        '--audio-format', 'mp3',
        '--audio-quality', '0',  
        '--output', output_template,
        video_url
    ]

    try:
        subprocess.run(['yt-dlp', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("yt-dlp is not installed or not in PATH")
        return None

    try:
        logger.info(f"Running command: {' '.join(command)}")
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=300  
        )
        logger.info(f"yt-dlp completed successfully")
        
        if result.stdout:
            logger.debug(f"yt-dlp stdout: {result.stdout[:500]}...")
        if result.stderr:
            logger.debug(f"yt-dlp stderr: {result.stderr[:500]}...")

        if os.path.exists(absolute_audio_path):
            file_size = os.path.getsize(absolute_audio_path)
            logger.info(f"Audio file created successfully at {absolute_audio_path} (size: {file_size} bytes)")
            
            if file_size == 0:
                logger.error("Downloaded audio file is empty")
                os.remove(absolute_audio_path)
                return None
                
            return absolute_audio_path
        else:
            logger.error(f"Audio file not found at {absolute_audio_path}")
            return None

    except subprocess.TimeoutExpired:
        logger.error("Download process timed out after 5 minutes")
        return None
    except subprocess.CalledProcessError as e:
        logger.error(f"yt-dlp failed with exit code {e.returncode}: {e.stderr}")
        return None
    except FileNotFoundError as e:
        logger.error(f"Required binary not found in system PATH: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error downloading audio: {str(e)}")
        return None