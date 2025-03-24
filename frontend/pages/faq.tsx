import React from 'react';
import Head from 'next/head';
import { Header } from '../components/Header';
import { Footer } from '../components/Footer';

export default function FAQ() {
  const faqItems = [
    {
      question: 'What file formats are supported?',
      answer: 'For audio files, we support MP3, WAV, and OGG formats. For images, we support JPG, PNG, and GIF (including animated GIFs).'
    },
    {
      question: 'How long does it take to process a video?',
      answer: 'Processing time depends on the length of your video and current server load. Most videos are processed within 2-5 minutes.'
    },
    {
      question: 'Can I use copyrighted music?',
      answer: 'We recommend using only audio that you have the rights to use. You are responsible for ensuring you have the appropriate licenses for any copyrighted content.'
    },
    {
      question: 'What is frequency adjustment?',
      answer: 'Frequency adjustment allows you to change the pitch and speed of your audio. Lower values make the audio slower and deeper, while higher values make it faster and higher-pitched.'
    },
    {
      question: 'How long can my videos be?',
      answer: 'Free users can create videos up to 10 minutes. Pro and Enterprise users can create videos up to 30 minutes.'
    },
    {
      question: 'Can I add my own watermark or logo?',
      answer: 'Yes, Enterprise users can add custom branding elements to their videos. You can upload your logo as the image and it will be displayed throughout the video.'
    },
    {
      question: 'How many videos can I create?',
      answer: 'Free users can create up to 5 videos per day. Pro and Enterprise users have unlimited video creation.'
    },
    {
      question: 'What is fade in/fade out?',
      answer: 'Fade in gradually increases the volume from silence at the beginning of your audio. Fade out gradually decreases the volume to silence at the end of your audio. This creates a smoother listening experience.'
    },
    {
      question: 'Do I need to install any software?',
      answer: 'No, BGM Creator Web is a fully web-based application. You only need a modern web browser to use it.'
    },
    {
      question: 'Can I cancel my subscription at any time?',
      answer: 'Yes, you can cancel your subscription at any time. Your access will continue until the end of your current billing period.'
    }
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <Head>
        <title>FAQ | BGM Creator Web</title>
        <meta name="description" content="Frequently asked questions about BGM Creator Web" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />

      <main className="flex-1 container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center mb-8">
          Frequently Asked Questions
        </h1>
        
        <div className="max-w-3xl mx-auto">
          <div className="space-y-6">
            {faqItems.map((item, index) => (
              <div key={index} className="bg-white p-6 rounded-lg shadow-md">
                <h2 className="text-xl font-bold mb-2">{item.question}</h2>
                <p className="text-gray-600">{item.answer}</p>
              </div>
            ))}
          </div>
          
          <div className="mt-12 text-center">
            <h2 className="text-2xl font-semibold mb-4">Still have questions?</h2>
            <p className="text-gray-600 mb-6">We're here to help. Contact our support team.</p>
            <button className="bg-blue-600 text-white py-2 px-6 rounded-md hover:bg-blue-700">
              Contact Support
            </button>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
