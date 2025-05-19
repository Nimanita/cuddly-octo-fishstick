import React from 'react';
import LanguageDropdown from './LanguageDropdown';
import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { cpp } from '@codemirror/lang-cpp';
import { EditorView } from '@codemirror/view';

// Define a custom light theme using EditorView.theme:
const lightTheme = EditorView.theme({
  "&": {
    color: "#000",            // Text color
    backgroundColor: "#fff",  // Editor background
  },
  ".cm-content": {
    caretColor: "#000",       // Caret color
  },
  ".cm-scroller": {
    backgroundColor: "#fff",  // Scroller (background) color.
  },
}, { dark: false });

export default function CodeEditor({
  code,
  setCode,
  selectedLanguage,
  setSelectedLanguage,
  onRun,
  onStop,
  onClear,
  onSave
}) {
  // Choose the proper language extension based on the selected language.
  const extensions = selectedLanguage === 'Python' ? [python()] : [cpp()];

  return (
    <div className="p-4 border rounded bg-gray-100">
      <div className="flex items-center space-x-2 mb-2">
        <LanguageDropdown
          selectedLanguage={selectedLanguage}
          onChange={(e) => setSelectedLanguage(e.target.value)}
        />
        <button
          onClick={onRun}
          className="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded"
        >
          Run
        </button>
        <button
          onClick={onStop}
          className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
        >
          Stop
        </button>
        <button
          onClick={onClear}
          className="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded"
        >
          Clear
        </button>
        
      </div>

      {/* CodeMirror Editor with a custom light theme */}
      <CodeMirror
        value={code}
        height="16rem"  // Roughly equates to Tailwind's h-64
        theme={lightTheme}
        extensions={extensions}
        onChange={(value) => setCode(value)}
      />
    </div>
  );
}


