import os
import sys
import json
import numpy as np
from scipy import signal
import soundfile as sf
from typing import Dict, List, Tuple, Optional

class FrequencyOptimizer:
    """
    音声ファイルの周波数特性を最適化するクラス
    """
    
    @staticmethod
    def load_config() -> Dict:
        """
        設定ファイルを読み込む
        """
        # デフォルト設定
        default_config = {
            "profiles": {
                "default": {
                    "low_freq_range": [50, 200],
                    "low_boost": 3.0,
                    "cry_freq_range": [2500, 5000],
                    "cry_reduction": -3.0
                },
                "work": {
                    "low_freq_range": [40, 180],
                    "low_boost": 4.0,
                    "cry_freq_range": [2800, 5500],
                    "cry_reduction": -4.0
                },
                "relax": {
                    "low_freq_range": [60, 250],
                    "low_boost": 5.0,
                    "cry_freq_range": [2200, 4500],
                    "cry_reduction": -2.0
                },
                "focus": {
                    "low_freq_range": [30, 150],
                    "low_boost": 2.5,
                    "cry_freq_range": [3000, 6000],
                    "cry_reduction": -5.0
                }
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
    def optimize_audio(input_file: str, output_file: str, profile: str = "default") -> bool:
        """
        音声ファイルの周波数を最適化する
        
        Args:
            input_file: 入力音声ファイルのパス
            output_file: 出力音声ファイルのパス
            profile: 最適化プロファイル名
            
        Returns:
            bool: 処理が成功したかどうか
        """
        try:
            # 設定を読み込む
            all_configs = FrequencyOptimizer.load_config()
            
            # プロファイル設定を取得（指定がなければデフォルト）
            if profile not in all_configs['profiles']:
                print(f"警告: プロファイル '{profile}' が見つかりません。デフォルト設定を使用します。")
                profile = "default"
                
            config = all_configs['profiles'][profile]
            print(f"プロファイル '{profile}' の設定を適用します")
            
            # 音声ファイルを読み込む
            print("音声ファイルを読み込んでいます...")
            data, samplerate = sf.read(input_file)
            print(f"サンプリングレート: {samplerate}Hz")
            print(f"データ長: {len(data)} サンプル")
            
            # ステレオの場合、モノラルに変換
            if len(data.shape) > 1:
                print("ステレオをモノラルに変換しています...")
                data_mono = np.mean(data, axis=1)
                print(f"変換後のデータ長: {len(data_mono)} サンプル")
                
                # モノラルデータをステレオに戻す準備（処理はモノラルで行い、結果をステレオに複製）
                channels = data.shape[1]
                stereo_result = True
            else:
                data_mono = data
                stereo_result = False
            
            # FFTを実行
            print("FFTを実行しています...")
            fft_data = np.fft.fft(data_mono)
            freqs = np.fft.fftfreq(len(data_mono), 1/samplerate)
            
            # 周波数帯域ごとのゲインを計算
            print("周波数帯域の最適化を適用しています...")
            gain = np.ones_like(freqs)
            
            # 低周波帯域の強調
            low_freq_mask = (np.abs(freqs) >= config['low_freq_range'][0]) & (np.abs(freqs) <= config['low_freq_range'][1])
            gain[low_freq_mask] *= 10 ** (config['low_boost'] / 20)
            
            # 泣き声周波数帯域の抑制
            cry_freq_mask = (np.abs(freqs) >= config['cry_freq_range'][0]) & (np.abs(freqs) <= config['cry_freq_range'][1])
            gain[cry_freq_mask] *= 10 ** (config['cry_reduction'] / 20)
            
            # ゲインを適用
            fft_data *= gain
            
            # 逆FFTを実行
            print("逆FFTを実行しています...")
            optimized_data = np.real(np.fft.ifft(fft_data))
            
            # 正規化
            print("音量を正規化しています...")
            max_amplitude = np.max(np.abs(optimized_data))
            optimized_data = optimized_data / max_amplitude * 0.95  # ヘッドルーム確保
            
            # ステレオの場合は結果をステレオに戻す
            if stereo_result:
                optimized_stereo = np.zeros((len(optimized_data), channels))
                for i in range(channels):
                    optimized_stereo[:, i] = optimized_data
                optimized_data = optimized_stereo
            
            # 出力ファイルを保存
            print("最適化された音声を保存しています...")
            sf.write(output_file, optimized_data, samplerate)
            
            print("周波数最適化が完了しました")
            return True
            
        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return False
