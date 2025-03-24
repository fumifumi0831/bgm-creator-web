import os
import json
import uuid
import math
import subprocess
from typing import List, Dict, Optional, Tuple
import shutil

class AudioLooper:
    """
    音声ファイルをループ再生し、クロスフェードを適用するクラス
    """
    
    @staticmethod
    def load_config() -> Dict:
        """
        設定ファイルを読み込む
        """
        # デフォルト設定
        default_config = {
            "audio": {
                "crossfade_duration": 3.0,
                "sample_rate": 44100,
                "quality": 2
            }
        }
        
        # 設定ファイルのパスを確認
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        
        # 設定ファイルが存在する場合は読み込み、なければデフォルト設定を使用
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                return config
            except Exception as e:
                print(f"設定ファイルの読み込みに失敗しました: {str(e)}")
                return default_config
        else:
            # 設定ファイルが存在しない場合はデフォルト設定を保存
            try:
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                with open(config_path, 'w') as f:
                    json.dump(default_config, f, indent=4)
            except Exception as e:
                print(f"デフォルト設定の保存に失敗しました: {str(e)}")
            
            return default_config
    
    @staticmethod
    def get_audio_duration(file_path: str) -> float:
        """
        音声ファイルの再生時間を取得する
        
        Args:
            file_path: 音声ファイルのパス
            
        Returns:
            float: 再生時間（秒）
        """
        cmd = [
            'ffprobe', 
            '-v', 'error', 
            '-show_entries', 'format=duration', 
            '-of', 'default=noprint_wrappers=1:nokey=1', 
            file_path
        ]
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return float(result.stdout)
    
    @staticmethod
    def apply_fade_effects(input_file: str, output_file: str, fade_in: float, fade_out: float, duration: float) -> str:
        """
        フェードイン・フェードアウト効果を適用する
        
        Args:
            input_file: 入力音声ファイルのパス
            output_file: 出力音声ファイルのパス
            fade_in: フェードインの時間（秒）
            fade_out: フェードアウトの時間（秒）
            duration: ファイルの再生時間
            
        Returns:
            str: 処理後のファイルパス
        """
        # フェードアウトの開始位置を計算
        fade_out_start = duration - fade_out
        
        # フィルタ文字列を構築
        filter_parts = []
        
        if fade_in > 0:
            filter_parts.append(f"afade=t=in:st=0:d={fade_in}")
        
        if fade_out > 0 and fade_out_start > 0:
            filter_parts.append(f"afade=t=out:st={fade_out_start}:d={fade_out}")
        
        if filter_parts:
            # フィルタを適用
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
            # フェード効果なしの場合はファイルをコピー
            shutil.copyfile(input_file, output_file)
            return output_file
    
    @staticmethod
    def combine_audio_with_loops(input_file: str, output_file: str, target_duration: int, 
                             crossfade_duration: float = 3.0, profile: str = "default") -> str:
        """
        音声ファイルをループ再生し、クロスフェードを適用して結合する
        
        Args:
            input_file: 入力音声ファイルのパス
            output_file: 出力音声ファイルのパス
            target_duration: 目標の再生時間（秒）
            crossfade_duration: クロスフェードの時間（秒）
            profile: オーディオプロファイル名
            
        Returns:
            str: 処理後のファイルパス
        """
        # 設定を読み込む
        config = AudioLooper.load_config()
        audio_config = config.get('audio', {})
        sample_rate = audio_config.get('sample_rate', 44100)
        audio_quality = audio_config.get('quality', 2)
        
        if crossfade_duration <= 0:
            crossfade_duration = audio_config.get('crossfade_duration', 3.0)
        
        # 一時ディレクトリを作成
        temp_dir = os.path.join(os.path.dirname(output_file), "temp_" + str(uuid.uuid4()))
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # 入力ファイルの長さを取得
            duration = AudioLooper.get_audio_duration(input_file)
            print(f"入力ファイルの再生時間: {duration}秒")
            
            # 必要なループ回数を計算（確実な切り上げ）
            loop_count = math.ceil(target_duration / duration)
            print(f"必要なループ回数: {loop_count}")
            
            # 各ループに対してフェード効果を適用
            temp_files = []
            file_list_path = os.path.join(temp_dir, "file_list.txt")
            
            with open(file_list_path, 'w') as file_list:
                for i in range(loop_count):
                    temp_file = os.path.join(temp_dir, f"loop_{i}.mp3")
                    
                    # フェード効果を適用
                    print(f"ループ {i+1}/{loop_count} にフェード効果を適用しています...")
                    ffmpeg_cmd = [
                        'ffmpeg', '-y', 
                        '-i', input_file,
                        '-filter_complex', f"[0:a]aformat=sample_fmts=fltp:sample_rates={sample_rate}:channel_layouts=stereo,"
                                         f"volume=1,afade=t=in:st=0:d={crossfade_duration},"
                                         f"afade=t=out:st={duration-crossfade_duration}:d={crossfade_duration}[a]",
                        '-map', '[a]', 
                        '-acodec', 'libmp3lame', 
                        '-q:a', str(audio_quality),
                        temp_file
                    ]
                    
                    subprocess.run(ffmpeg_cmd, check=True)
                    temp_files.append(temp_file)
                    
                    # ファイルリストに追加
                    file_list.write(f"file '{temp_file}'\n")
            
            # ループした音声ファイルを結合
            temp_combined = os.path.join(temp_dir, "combined.mp3")
            print("処理済みの音声ファイルを結合しています...")
            combine_cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', file_list_path,
                '-c', 'copy',
                temp_combined
            ]
            
            subprocess.run(combine_cmd, check=True)
            
            # 指定された時間で切り詰める
            print(f"目標再生時間 {target_duration}秒 で切り詰めています...")
            trim_cmd = [
                'ffmpeg', '-y',
                '-i', temp_combined,
                '-t', str(target_duration),
                '-c', 'copy',
                output_file
            ]
            
            subprocess.run(trim_cmd, check=True)
            
            print(f"ループ処理が完了しました: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")
            import traceback
            print(traceback.format_exc())
            raise e
            
        finally:
            # 一時ファイルの削除
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                print(f"一時ファイルの削除に失敗しました: {str(e)}")
    
    @staticmethod
    def normalize_audio_volume(input_file: str, output_file: str) -> str:
        """
        音量を正規化する
        
        Args:
            input_file: 入力音声ファイルのパス
            output_file: 出力音声ファイルのパス
            
        Returns:
            str: 処理後のファイルパス
        """
        # 設定を読み込む
        config = AudioLooper.load_config()
        audio_config = config.get('audio', {})
        sample_rate = audio_config.get('sample_rate', 44100)
        
        # loudnormフィルタを用いて正規化
        print("音量を正規化しています...")
        cmd = [
            'ffmpeg', '-y',
            '-i', input_file,
            '-filter:a', 'loudnorm=I=-16:LRA=11:TP=-1.5',
            '-ar', str(sample_rate),
            '-ac', '2',
            output_file
        ]
        
        subprocess.run(cmd, check=True)
        return output_file
