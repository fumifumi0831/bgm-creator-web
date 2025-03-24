import os
import subprocess
import uuid
import math
from typing import Optional, Tuple

class AudioProcessor:
    @staticmethod
    def get_audio_duration(input_file: str) -> float:
        """
        Get the duration of an audio file in seconds
        
        Args:
            input_file: Path to input audio file
            
        Returns:
            Duration in seconds
        """
        cmd = [
            'ffprobe', 
            '-v', 'error', 
            '-show_entries', 'format=duration', 
            '-of', 'default=noprint_wrappers=1:nokey=1', 
            input_file
        ]
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        duration = float(result.stdout)
        return duration
    
    @staticmethod
    def loop_audio(input_file: str, output_file: str, target_duration: int) -> str:
        """
        Loop audio file to reach the target duration
        
        Args:
            input_file: Path to input audio file
            output_file: Path to output audio file
            target_duration: Target duration in seconds
            
        Returns:
            Path to the processed audio file
        """
        # Get original audio duration
        original_duration = AudioProcessor.get_audio_duration(input_file)
        
        # Calculate number of loops needed
        loops_needed = math.ceil(target_duration / original_duration)
        
        # Create filter complex command for concatenation
        filter_complex = f"[0:a]afifo,aloop={loops_needed}:size=2e+09[a];"
        filter_complex += f"[a]atrim=0:{target_duration}[out]"
        
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-filter_complex', filter_complex,
            '-map', '[out]',
            '-y',  # Overwrite output file if it exists
            output_file
        ]
        
        subprocess.run(cmd, check=True)
        return output_file
    
    @staticmethod
    def adjust_frequency(input_file: str, output_file: str, frequency_factor: float) -> str:
        """
        Adjust audio frequency (pitch and speed)
        
        Args:
            input_file: Path to input audio file
            output_file: Path to output audio file
            frequency_factor: Factor to adjust frequency (e.g., 0.5 for half speed/pitch)
            
        Returns:
            Path to the processed audio file
        """
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-filter:a', f'asetrate=44100*{frequency_factor},aresample=44100',
            '-y',
            output_file
        ]
        
        subprocess.run(cmd, check=True)
        return output_file
    
    @staticmethod
    def add_fade_effects(input_file: str, output_file: str, fade_in: int = 0, fade_out: int = 0) -> str:
        """
        Add fade-in and fade-out effects to audio
        
        Args:
            input_file: Path to input audio file
            output_file: Path to output audio file
            fade_in: Fade-in duration in seconds
            fade_out: Fade-out duration in seconds
            
        Returns:
            Path to the processed audio file
        """
        # Get the duration to calculate fade out start time
        duration = AudioProcessor.get_audio_duration(input_file)
        fade_out_start = duration - fade_out
        
        # Build the filter
        filter_parts = []
        
        if fade_in > 0:
            filter_parts.append(f"afade=t=in:st=0:d={fade_in}")
        
        if fade_out > 0:
            filter_parts.append(f"afade=t=out:st={fade_out_start}:d={fade_out}")
        
        if filter_parts:
            filter_str = ','.join(filter_parts)
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-af', filter_str,
                '-y',
                output_file
            ]
            
            subprocess.run(cmd, check=True)
            return output_file
        else:
            # No fade effects, just copy the file
            shutil.copyfile(input_file, output_file)
            return output_file
    
    @staticmethod
    def process_audio(input_file: str, output_dir: str, duration: int, frequency_factor: Optional[float] = None, fade_in: int = 0, fade_out: int = 0) -> str:
        """
        Process audio with all required operations
        
        Args:
            input_file: Path to input audio file
            output_dir: Directory to save output files
            duration: Target duration in seconds
            frequency_factor: Optional factor to adjust frequency
            fade_in: Fade-in duration in seconds
            fade_out: Fade-out duration in seconds
            
        Returns:
            Path to the final processed audio file
        """
        # Create temporary filenames
        temp_filename = str(uuid.uuid4())
        temp_file1 = os.path.join(output_dir, f"{temp_filename}_1.mp3")
        temp_file2 = os.path.join(output_dir, f"{temp_filename}_2.mp3")
        final_audio = os.path.join(output_dir, f"{temp_filename}_final.mp3")
        
        # Step 1: Adjust frequency if needed
        current_file = input_file
        if frequency_factor is not None and frequency_factor != 1.0:
            current_file = AudioProcessor.adjust_frequency(current_file, temp_file1, frequency_factor)
        else:
            # Just copy to temp_file1 to maintain the workflow
            shutil.copyfile(input_file, temp_file1)
            current_file = temp_file1
        
        # Step 2: Loop audio to target duration
        current_file = AudioProcessor.loop_audio(current_file, temp_file2, duration)
        
        # Step 3: Add fade effects
        final_file = AudioProcessor.add_fade_effects(current_file, final_audio, fade_in, fade_out)
        
        # Clean up temporary files
        for file in [temp_file1, temp_file2]:
            if os.path.exists(file):
                os.remove(file)
        
        return final_file
