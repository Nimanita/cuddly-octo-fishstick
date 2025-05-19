import React, { useEffect, useRef } from 'react';

export default function Terminal({ title, output, input, setInput, onSendInput, onClear, prompt }) {
  const outputRef = useRef(null);

  // Auto-scroll whenever the output or prompt is updated
  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [output, prompt]);

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
      <div ref={outputRef} className="bg-gray-900 p-2 rounded h-64 overflow-y-auto font-mono">
        <pre>{output}</pre>
        {prompt && (
          <div className="flex items-center">
            <span></span>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  onSendInput(input);
                  setInput('');
                }
              }}
              className="bg-transparent text-white outline-none ml-1 flex-1"
              autoFocus
              style={{ caretColor: 'white' }}
            />
            {/* Blinking cursor element */}
            <span className="blinking-cursor ml-1">|</span>
          </div>
        )}
      </div>
      <style jsx>{`
        .blinking-cursor {
          animation: blink 1s step-start infinite;
        }
        @keyframes blink {
          50% {
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
}





