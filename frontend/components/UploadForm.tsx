import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const UploadForm: React.FC = () => {
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [duration, setDuration] = useState<number>(600); // 10 minutes default
  const [frequency, setFrequency] = useState<number | null>(null);
  const [fadeIn, setFadeIn] = useState<number>(2); // 2 seconds default
  const [fadeOut, setFadeOut] = useState<number>(2); // 2 seconds default
  const [addMotion, setAddMotion] = useState<boolean>(true); // Enable motion by default
  const [profiles, setProfiles] = useState<string[]>(['default', 'work', 'relax', 'focus']);
  const [selectedProfile, setSelectedProfile] = useState<string>('default');
  const [applyFrequencyOptimization, setApplyFrequencyOptimization] = useState<boolean>(true);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [progress, setProgress] = useState<number>(0);
  const [error, setError] = useState<string>('');
  const [downloadUrl, setDownloadUrl] = useState<string>('');
  const [jobId, setJobId] = useState<string>('');

  const handleAudioChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setAudioFile(e.target.files[0]);
    }
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setImageFile(e.target.files[0]);
    }
  };

  // ジョブ状態の定期的なチェック
  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;
    
    if (jobId && isUploading) {
      interval = setInterval(async () => {
        try {
          const statusResponse = await axios.get(`http://localhost:8000/api/status/${jobId}`);
          const { status, progress, file_id } = statusResponse.data;
          
          setProgress(progress);
          
          if (status === 'completed' && file_id) {
            setIsUploading(false);
            setDownloadUrl(`http://localhost:8000/api/download/${file_id}`);
            if (interval) clearInterval(interval);
          } else if (status === 'failed') {
            setIsUploading(false);
            setError('処理中にエラーが発生しました。もう一度お試しください。');
            if (interval) clearInterval(interval);
          }
        } catch (error) {
          console.error('Error checking job status:', error);
        }
      }, 2000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [jobId, isUploading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!audioFile) {
      setError('オーディオファイルを選択してください');
      return;
    }

    setIsUploading(true);
    setProgress(0);
    setError('');
    setDownloadUrl('');

    const formData = new FormData();
    formData.append('audio_file', audioFile);
    if (imageFile) {
      formData.append('image_file', imageFile);
    }
    formData.append('duration', duration.toString());
    if (frequency) {
      formData.append('frequency', frequency.toString());
    }
    formData.append('fade_in', fadeIn.toString());
    formData.append('fade_out', fadeOut.toString());
    formData.append('add_motion', addMotion.toString());
    formData.append('audio_profile', selectedProfile);
    formData.append('apply_frequency_optimization', applyFrequencyOptimization.toString());

    try {
      const response = await axios.post('http://localhost:8000/api/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setJobId(response.data.job_id);
    } catch (err) {
      setError('ファイルのアップロードに失敗しました。もう一度お試しください。');
      setIsUploading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-gray-700 mb-2 font-medium">オーディオファイル (MP3, WAV)</label>
        <input
          type="file"
          accept="audio/*"
          onChange={handleAudioChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
        />
      </div>

      <div>
        <label className="block text-gray-700 mb-2 font-medium">画像ファイル (オプション)</label>
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
        />
      </div>

      <div>
        <label className="block text-gray-700 mb-2 font-medium">動画の長さ (分)</label>
        <input
          type="range"
          min="1"
          max="30"
          value={duration / 60}
          onChange={(e) => setDuration(parseInt(e.target.value) * 60)}
          className="w-full"
        />
        <div className="text-center mt-1">{duration / 60} 分</div>
      </div>

      <div>
        <label className="block text-gray-700 mb-2 font-medium">サウンドプロファイル</label>
        <select
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
          value={selectedProfile}
          onChange={(e) => setSelectedProfile(e.target.value)}
        >
          {profiles.map(profile => (
            <option key={profile} value={profile}>
              {profile === 'default' ? 'デフォルト' : 
               profile === 'work' ? '作業用' : 
               profile === 'relax' ? 'リラックス用' : 
               profile === 'focus' ? '集中用' : profile}
            </option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-gray-700 mb-2 font-medium">フェードイン (秒)</label>
          <input
            type="number"
            min="0"
            max="10"
            value={fadeIn}
            onChange={(e) => setFadeIn(parseInt(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
          />
        </div>

        <div>
          <label className="block text-gray-700 mb-2 font-medium">フェードアウト (秒)</label>
          <input
            type="number"
            min="0"
            max="10"
            value={fadeOut}
            onChange={(e) => setFadeOut(parseInt(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
          />
        </div>
      </div>

      <div className="flex items-center">
        <input
          type="checkbox"
          id="add-motion"
          checked={addMotion}
          onChange={(e) => setAddMotion(e.target.checked)}
          className="h-4 w-4 text-blue-600"
        />
        <label htmlFor="add-motion" className="ml-2 text-gray-700">
          静止画に動きエフェクトを追加する
        </label>
      </div>

      <div className="flex items-center">
        <input
          type="checkbox"
          id="optimize-frequency"
          checked={applyFrequencyOptimization}
          onChange={(e) => setApplyFrequencyOptimization(e.target.checked)}
          className="h-4 w-4 text-blue-600"
        />
        <label htmlFor="optimize-frequency" className="ml-2 text-gray-700">
          音声を最適化する (聞き心地を良くする)
        </label>
      </div>

      {error && (
        <div className="text-red-500 text-center">{error}</div>
      )}

      {isUploading ? (
        <div className="space-y-3">
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
              className="bg-blue-600 h-2.5 rounded-full"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <div className="text-center text-sm text-gray-600">
            {progress < 10 ? 'アップロード中...' : 
             progress < 50 ? '音声処理中...' : 
             progress < 100 ? '動画作成中...' : '処理完了中...'}
          </div>
        </div>
      ) : downloadUrl ? (
        <div className="text-center">
          <a
            href={downloadUrl}
            className="bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 inline-block"
            download
          >
            BGM動画をダウンロード
          </a>
        </div>
      ) : (
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
        >
          BGM動画を作成
        </button>
      )}
    </form>
  );
};
