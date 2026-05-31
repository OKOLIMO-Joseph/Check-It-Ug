'use client';

import { useState } from 'react';
import { checkClaim } from '../lib/api';

interface ClaimInputProps {
  onResult: (result: any) => void;
}

export default function ClaimInput({ onResult }: ClaimInputProps) {
  const [text, setText] = useState('');
  const [lang, setLang] = useState('en');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!text.trim()) {
      setError('Please enter a claim to check');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const result = await checkClaim({ text, lang, source: 'web' });
      onResult(result);
    } catch (err) {
      setError('Failed to check claim. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <textarea
        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        rows={4}
        placeholder="Paste a WhatsApp message or claim to check..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      
      <div className="mt-4 flex gap-4">
        <select
          className="px-3 py-2 border border-gray-300 rounded-lg"
          value={lang}
          onChange={(e) => setLang(e.target.value)}
        >
          <option value="en">English</option>
          <option value="lg">Luganda</option>
          <option value="nyn">Runyankole</option>
        </select>
        
        <button
          className="flex-1 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
              </svg>
              Checking sources...
            </span>
          ) : (
            'Check it'
          )}
        </button>
      </div>
      
      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      )}
    </div>
  );
}