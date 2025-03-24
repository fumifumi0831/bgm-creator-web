import React, { useState } from 'react';
import axios from 'axios';

export const UploadForm: React.FC = () => {
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [duration, setDuration] = useState<number>(600); // 10 minutes default
  const [frequency, setFrequency] = useState<number | null>(null);
  const [fadeIn, setFadeIn] = useState<number>(2); // 2 seconds default
  const [fadeOut, setFadeOut] = useState<number>(2); // 2 seconds default
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [progress, setProgress] = useState<number>(0);
  const [error, setError] = useState<string>('');
  const [downloadUrl, setDownloadUrl] = useState<string>('');

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!audioFile) {
      setError('Please select an audio file');
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

    try {
      // TODO: Replace with your actual API endpoint
      const response = await axios.post('http://localhost:8000/api/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percentage = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setProgress(percentage);
          }
        }
      });

      // Mock the processing and status check
      // In a real implementation, you would poll the /api/status endpoint
      setTimeout(() => {
        setDownloadUrl(`http://localhost:8000/api/download/${response.data.job_id}`);
        setIsUploading(false);
      }, 3000);
    } catch (err) {
      setError('Error processing your request. Please try again.');
      setIsUploading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-gray-700 mb-2 font-medium">Audio File (MP3, WAV)</label>
        <input
          type="file"
          accept="audio/*"
          onChange={handleAudioChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
        />
      </div>

      <div>
        <label className="block text-gray-700 mb-2 font-medium">Image File (Optional)</label>
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
        />
      </div>

      <div>
        <label className="block text-gray-700 mb-2 font-medium">Video Duration (minutes)</label>
        <input
          type="range"
          min="1"
          max="30"
          value={duration / 60}
          onChange={(e) => setDuration(parseInt(e.target.value) * 60)}
          className="w-full"
        />
        <div className="text-center mt-1">{duration / 60} minutes</div>
      </div>

      <div>
        <label className="block text-gray-700 mb-2 font-medium">Frequency Adjustment (Optional)</label>
        <select
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
          value={frequency || ''}
          onChange={(e) => {
            const value = e.target.value;
            setFrequency(value ? parseFloat(value) : null);
          }}
        >
          <option value="">No adjustment</option>
          <option value="0.75">Slower (0.75x)</option>
          <option value="0.9">Slightly slower (0.9x)</option>
          <option value="1.1">Slightly faster (1.1x)</option>
          <option value="1.25">Faster (1.25x)</option>
        </select>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-gray-700 mb-2 font-medium">Fade In (seconds)</label>
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
          <label className="block text-gray-700 mb-2 font-medium">Fade Out (seconds)</label>
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
            {progress < 100 ? 'Uploading...' : 'Processing your video...'}
          </div>
        </div>
      ) : downloadUrl ? (
        <div className="text-center">
          <a
            href={downloadUrl}
            className="bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 inline-block"
            download
          >
            Download Your BGM Video
          </a>
        </div>
      ) : (
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
        >
          Create BGM Video
        </button>
      )}
    </form>
  );
};
