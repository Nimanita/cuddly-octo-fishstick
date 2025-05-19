import React from 'react';

export default function LanguageDropdown({ selectedLanguage, onChange }) {
  return (
    <select
      value={selectedLanguage}
      onChange={onChange}
      className="border border-gray-300 rounded px-3 py-1"
    >
      <option value="Python">Python</option>

    </select>
  );
}
