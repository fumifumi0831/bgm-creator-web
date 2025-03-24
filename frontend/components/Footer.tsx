import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-white py-6">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <div className="text-xl font-bold">BGM Creator Web</div>
            <div className="text-gray-400 text-sm mt-1">
              Create YouTube BGM videos easily
            </div>
          </div>
          
          <div className="flex space-x-6">
            <a href="#" className="hover:text-blue-400">
              Terms of Service
            </a>
            <a href="#" className="hover:text-blue-400">
              Privacy Policy
            </a>
            <a href="#" className="hover:text-blue-400">
              Contact
            </a>
          </div>
        </div>
        
        <div className="mt-6 text-center text-gray-400 text-sm">
          &copy; {new Date().getFullYear()} BGM Creator Web. All rights reserved.
        </div>
      </div>
    </footer>
  );
};
