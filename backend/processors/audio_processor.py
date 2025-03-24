import os
import subprocess
import uuid
import math
import shutil
from typing import Optional, Tuple

# 新しく追加したクラスをインポート
from processors.frequency_optimizer import FrequencyOptimizer
from processors.audio_looper import AudioLooper

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
        # 新しいAudioLooperクラスを使用
        return AudioLooper.combine_audio_with_loops(input_file, output_file, target_duration)
    
    @staticmethod
    def adjust_frequency(input_file: str, output_file: str, frequency_factor: float) -> str:
        """
        Adjust audio frequency
        
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
        # AudioLooperのメソッドを使用
        duration = AudioProcessor.get_audio_duration(input_file)
        return AudioLooper.apply_fade_effects(input_file, output_file, fade_in, fade_out, duration)
    
    @staticmethod
    def process_audio(input_file: str, output_dir: str, duration: int, 
                     frequency_factor: Optional[float] = None, 
                     fade_in: int = 0, fade_out: int = 0, 
                     profile: str = "default", 
                     apply_frequency_optimization: bool = True) -> str:
        """
        Process audio with all required operations
        
        Args:
            input_file: Path to input audio file
            output_dir: Directory to save output files
            duration: Target duration in seconds
            frequency_factor: Optional factor to adjust frequency
            fade_in: Fade-in duration in seconds
            fade_out: Fade-out duration in seconds
            profile: Audio profile for optimization
            apply_frequency_optimization: Whether to apply frequency optimization
            
        Returns:
            Path to the final processed audio file
        """
        # Create temporary filenames
        temp_filename = str(uuid.uuid4())
        temp_file1 = os.path.join(output_dir, f"{temp_filename}_1.mp3")
        temp_file2 = os.path.join(output_dir, f"{temp_filename}_2.mp3")
        temp_file3 = os.path.join(output_dir, f"{temp_filename}_3.mp3")
        final_audio = os.path.join(output_dir, f"{temp_filename}_final.mp3")
        
        try:
            print("音声処理を開始します...")
            
            # Step 1: Adjust frequency if needed
            current_file = input_file
            if frequency_factor is not None and frequency_factor != 1.0:
                print(f"周波数を調整しています（係数: {frequency_factor}）...")
                current_file = AudioProcessor.adjust_frequency(current_file, temp_file1, frequency_factor)
            else:
                # Just copy to temp_file1 to maintain the workflow
                shutil.copyfile(input_file, temp_file1)
                current_file = temp_file1
            
            # Step 2: Loop audio to target duration
            print(f"音声をループして{duration}秒に拡張しています...")
            current_file = AudioProcessor.loop_audio(current_file, temp_file2, duration)
            
            # Step 3: Apply frequency optimization if requested
            if apply_frequency_optimization:
                print(f"周波数最適化を適用しています（プロファイル: {profile}）...")
                FrequencyOptimizer.optimize_audio(current_file, temp_file3, profile)
                current_file = temp_file3
            
            # Step 4: Normalize audio volume
            print("音量を正規化しています...")
            current_file = AudioLooper.normalize_audio_volume(current_file, final_audio)
            
            # Clean up temporary files
            for file in [temp_file1, temp_file2, temp_file3]:
                if os.path.exists(file):
                    os.remove(file)
            
            print("音声処理が完了しました")
            return final_audio
            
        except Exception as e:
            print(f"音声処理中にエラーが発生しました: {str(e)}")
            # Clean up on error
            for file in [temp_file1, temp_file2, temp_file3, final_audio]:
                if os.path.exists(file):
                    os.remove(file)
            raise e