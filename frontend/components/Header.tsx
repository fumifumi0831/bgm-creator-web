import React from 'react';
import Link from 'next/link';

export const Header: React.FC = () => {
  return (
    <header className="bg-blue-600 text-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold">
          BGM Creator
        </Link>
        
        <nav>
          <ul className="flex space-x-6">
            <li>
              <Link href="/" className="hover:underline">
                ホーム
              </Link>
            </li>
            <li>
              <Link href="/pricing" className="hover:underline">
                料金プラン
              </Link>
            </li>
            <li>
              <Link href="/faq" className="hover:underline">
                よくある質問
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};
