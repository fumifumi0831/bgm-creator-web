import os
import subprocess
import uuid
import shutil
from PIL import Image
from typing import Optional, Tuple, List
import math

class VideoProcessor:
    @staticmethod
    def create_video_from_image(audio_file: str, image_file: str, output_file: str, duration: Optional[int] = None) -> str:
        """
        Create a video using a static image and audio
        
        Args:
            audio_file: Path to audio file
            image_file: Path to image file
            output_file: Path to output video file
            duration: Optional duration in seconds (defaults to audio length)
            
        Returns:
            Path to the created video file
        """
        # Get audio duration if not provided
        if duration is None:
            cmd = [
                'ffprobe', 
                '-v', 'error', 
                '-show_entries', 'format=duration', 
                '-of', 'default=noprint_wrappers=1:nokey=1', 
                audio_file
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            duration = float(result.stdout)
        
        # Check if image is a GIF
        is_gif = False
        try:
            with Image.open(image_file) as img:
                is_gif = getattr(img, "is_animated", False)
        except Exception:
            pass
        
        # Command for static image or GIF
        if is_gif:
            cmd = [
                'ffmpeg',
                '-stream_loop', '-1',  # Loop GIF indefinitely
                '-i', image_file,      # Input GIF
                '-i', audio_file,      # Input audio
                '-shortest',           # End when the shorter input ends (audio in this case)
                '-c:v', 'libx264',     # Video codec
                '-pix_fmt', 'yuv420p', # Pixel format
                '-c:a', 'aac',         # Audio codec
                '-b:a', '192k',        # Audio bitrate
                '-y',                  # Overwrite output file if it exists
                output_file
            ]
        else:
            # For static image
            cmd = [
                'ffmpeg',
                '-loop', '1',          # Loop image
                '-i', image_file,      # Input image
                '-i', audio_file,      # Input audio
                '-c:v', 'libx264',     # Video codec
                '-tune', 'stillimage', # Optimize for still image
                '-c:a', 'aac',         # Audio codec
                '-b:a', '192k',        # Audio bitrate
                '-pix_fmt', 'yuv420p', # Pixel format
                '-shortest',           # End when the shorter input ends (audio)
                '-y',                  # Overwrite output file if it exists
                output_file
            ]
        
        subprocess.run(cmd, check=True)
        return output_file
    
    @staticmethod
    def add_motion_to_image(image_file: str, output_file: str, audio_file: str, duration: int, motion_type: str = "zoom") -> str:
        """
        Create a video with motion effect on a static image
        
        Args:
            image_file: Path to input image file
            output_file: Path to output video file
            audio_file: Path to audio file
            duration: Duration in seconds
            motion_type: Type of motion effect (zoom, pan, etc.)
            
        Returns:
            Path to the processed video file
        """
        # Define filter based on motion type
        if motion_type == "zoom":
            # Slow zoom in effect
            filter_complex = "zoompan=z='min(zoom+0.0005,1.3)':d={}:s=1280x720:fps=30".format(duration * 30)  # 30 fps
        elif motion_type == "pan":
            # Slow panning effect
            filter_complex = "zoompan=z=1.1:x='iw/2-(iw/zoom/2)+sin(time)*50':y='ih/2-(ih/zoom/2)+cos(time)*50':d={}:s=1280x720:fps=30".format(duration * 30)
        else:
            # Default: subtle zoom and pan
            filter_complex = "zoompan=z='min(zoom+0.0008,1.2)':x='iw/2-(iw/zoom/2)+sin(time)*10':y='ih/2-(ih/zoom/2)+cos(time)*10':d={}:s=1280x720:fps=30".format(duration * 30)
        
        cmd = [
            'ffmpeg',
            '-loop', '1',          # Loop image
            '-i', image_file,      # Input image
            '-i', audio_file,      # Input audio
            '-filter_complex', filter_complex,
            '-c:v', 'libx264',     # Video codec
            '-c:a', 'aac',         # Audio codec
            '-b:a', '192k',        # Audio bitrate
            '-pix_fmt', 'yuv420p', # Pixel format
            '-shortest',           # End when the shorter input ends (audio)
            '-y',                  # Overwrite output file if it exists
            output_file
        ]
        
        subprocess.run(cmd, check=True)
        return output_file
    
    @staticmethod
    def process_video(audio_file: str, image_file: str, output_dir: str, duration: int, add_motion: bool = False, motion_type: str = "zoom") -> str:
        """
        Process audio and image to create a video
        
        Args:
            audio_file: Path to processed audio file
            image_file: Path to image file
            output_dir: Directory to save output files
            duration: Target duration in seconds
            add_motion: Whether to add motion effect to static images
            motion_type: Type of motion effect
            
        Returns:
            Path to the final video file
        """
        # Create output filename
        output_filename = str(uuid.uuid4())
        output_file = os.path.join(output_dir, f"{output_filename}.mp4")
        
        # Check if image is a GIF
        is_gif = False
        try:
            with Image.open(image_file) as img:
                is_gif = getattr(img, "is_animated", False)
        except Exception:
            pass
        
        # Process based on image type and motion setting
        if is_gif or not add_motion:
            # GIFs already have motion or user doesn't want motion effect
            return VideoProcessor.create_video_from_image(audio_file, image_file, output_file, duration)
        else:
            # Add motion effect to static image
            return VideoProcessor.add_motion_to_image(image_file, output_file, audio_file, duration, motion_type)
