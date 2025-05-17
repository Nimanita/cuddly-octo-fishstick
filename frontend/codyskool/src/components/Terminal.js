import React from 'react';

export default function Terminal({ title, content, setContent, isOutput, onClear }) {
  return (
    <div className="border rounded bg-black text-white p-2 mb-4">
      <div className="flex justify-between items-center mb-2">
        <span className="font-bold">{title}</span>
        <button 
          onClick={onClear} 
          className="bg-gray-700 hover:bg-gray-600 px-2 py-1 rounded"
        >
          Clear
        </button>
      </div>
      {isOutput ? (
        <div className="bg-gray-900 p-2 rounded h-32 overflow-y-auto">
          <pre>{content}</pre>
        </div>
      ) : (
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="w-full h-16 p-2 border rounded focus:outline-none resize-none overflow-y-auto text-black bg-white"
          placeholder="Enter input for your code..."
          rows={3}  // This allows for multiple lines (Enter key will go to a new line).
        />
      )}
    </div>
  );
}


