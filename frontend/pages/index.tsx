import React from 'react';
import Head from 'next/head';
import { UploadForm } from '../components/UploadForm';
import { Header } from '../components/Header';
import { Footer } from '../components/Footer';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <Head>
        <title>BGM Creator Web</title>
        <meta name="description" content="YouTubeのBGM動画を簡単に作成" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />

      <main className="flex-1 container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center mb-8">
          YouTubeのBGM動画を簡単に作成
        </h1>
        
        <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md">
          <UploadForm />
        </div>
        
        <div className="mt-12 max-w-4xl mx-auto">
          <h2 className="text-2xl font-semibold mb-4">使い方</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white p-4 rounded-lg shadow-md">
              <div className="text-xl font-bold mb-2">1. アップロード</div>
              <p>オーディオファイルと、必要に応じて画像またはGIFをアップロードします。</p>
            </div>
            
            <div className="bg-white p-4 rounded-lg shadow-md">
              <div className="text-xl font-bold mb-2">2. カスタマイズ</div>
              <p>動画の長さ、周波数調整、フェード効果などを設定します。</p>
            </div>
            
            <div className="bg-white p-4 rounded-lg shadow-md">
              <div className="text-xl font-bold mb-2">3. ダウンロード</div>
              <p>処理が完了したら、作成されたBGM動画をダウンロードします。</p>
            </div>
          </div>
        </div>

        <div className="mt-12 max-w-4xl mx-auto bg-blue-50 p-6 rounded-lg">
          <h2 className="text-2xl font-semibold mb-4">BGM Creator Webの特徴</h2>
          
          <ul className="space-y-2">
            <li className="flex items-start">
              <svg className="h-6 w-6 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
              <span>簡単操作 - 専門的な知識は必要ありません</span>
            </li>
            <li className="flex items-start">
              <svg className="h-6 w-6 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
              <span>サウンドプロファイル - 目的に合わせた音質調整</span>
            </li>
            <li className="flex items-start">
              <svg className="h-6 w-6 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
              <span>動きエフェクト - 静止画に動きを追加</span>
            </li>
            <li className="flex items-start">
              <svg className="h-6 w-6 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
              <span>カスタム長 - 最大30分の動画を作成可能</span>
            </li>
          </ul>
        </div>
      </main>

      <Footer />
    </div>
  );
}
