import React from 'react';

export default function Sidebar({ snippets, onSnippetSelect }) {
  return (
    <div className="w-full md:w-1/4 bg-green-100 p-4 border rounded">
      <h2 className="text-xl font-bold mb-2">Saved Snippets</h2>
      {snippets.length === 0 ? (
        <p>No snippets saved yet.</p>
      ) : (
        <ul>
          {snippets.map((snippet) => (
            <li
              key={snippet.id}
              onClick={() => onSnippetSelect(snippet)}
              className="mb-2 p-2 bg-white rounded shadow cursor-pointer hover:bg-gray-200"
            >
              {snippet.title}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
