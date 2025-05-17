// File: src/pages/Home.js
import React, { useState, useRef } from 'react';
import Navbar from '../components/Navbar';
import CodeEditor from '../components/CodeEditor';
import Terminal from '../components/Terminal';
import Sidebar from '../components/Sidebar';
import API_BASE_URL from '../config';

export default function Home() {
  // State variables
  const [code, setCode] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('Python');
  const [inputCommand, setInputCommand] = useState(''); // For user input
  const [output, setOutput] = useState('');
  const [user, setUser] = useState(null);
  const [snippets, setSnippets] = useState([]);

  // Mapping language names to IDs as per your backend
  const languageMapping = {
    Python: 1,
    C: 2,
    "C++": 3
  };

  const abortControllerRef = useRef(null);

  // Handler for executing code; passes the user input via the "user_input" parameter
  const handleRun = async () => {
    setOutput('');
    const payload = {
      code: code,
      language_id: languageMapping[selectedLanguage],
      save_snippet: false,
      snippet_title: 'New Code',
      user_input: inputCommand // <-- Your multi-line user input is passed here
    };

    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch(`${API_BASE_URL}/api/execute/execute/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: abortControllerRef.current.signal
      });
      const data = await response.json();
      if (data.status === 'success') {
        setOutput(data.stdout);
      } else {
        setOutput(`Error: ${data.friendly_error || data.stderr}`);
      }
    } catch (error) {
      if (error.name === 'AbortError') {
        setOutput('Execution stopped by user.');
      } else {
        setOutput('Error executing code.');
      }
    }
  };

  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
  };

  const handleClear = () => {
    setCode('');
  };

  const handleSave = async () => {
    if (!user) {
      alert('Please log in to save your snippet.');
      return;
    }
    const payload = {
      title: 'Saved Snippet',
      code: code,
      language: selectedLanguage,
      is_public: false
    };

    try {
      const response = await fetch(`${API_BASE_URL}/api/snippets/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (response.ok) {
        const newSnippet = await response.json();
        setSnippets(prev => [...prev, newSnippet]);
        alert('Snippet saved successfully!');
      } else {
        alert('Failed to save snippet.');
      }
    } catch (error) {
      console.error('Error saving snippet:', error);
    }
  };

  const handleLogin = async (username, password) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api-auth/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      if (response.ok) {
        const data = await response.json();
        setUser({ username: data.username });
      } else {
        alert('Invalid credentials');
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  const handleLogout = async () => {
    try {
      await fetch(`${API_BASE_URL}/api-auth/logout/`);
      setUser(null);
      setSnippets([]);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <div className="min-h-screen bg-yellow-50">
      <Navbar 
        user={user}
        onLoginClick={() => handleLogin('demoUser', 'demoPass')}
        onLogoutClick={handleLogout}
      />
      <div className="container mx-auto p-4 flex flex-col md:flex-row">
        <div className="flex-1">
          <CodeEditor
            code={code}
            setCode={setCode}
            selectedLanguage={selectedLanguage}
            setSelectedLanguage={setSelectedLanguage}
            onRun={handleRun}
            onStop={handleStop}
            onClear={handleClear}
            onSave={handleSave}
            isLoggedIn={!!user}
          />
          <div className="mt-4">
            {/* Updated Input Terminal: white background with black text and multi-line support */}
            <div className="border rounded bg-black text-white p-2 mb-4">
              <div className="flex justify-between items-center mb-2">
                <span className="font-bold">Input Terminal</span>
                <button 
                  onClick={() => setInputCommand('')}
                  className="bg-gray-700 hover:bg-gray-600 px-2 py-1 rounded"
                >
                  Clear
                </button>
              </div>
              <textarea
                value={inputCommand}
                onChange={(e) => setInputCommand(e.target.value)}
                className="w-full h-16 p-2 border rounded focus:outline-none resize-none overflow-y-auto text-black bg-white"
                placeholder="Enter input for your code..."
                rows={3}
              />
            </div>

            {/* Output Terminal remains unchanged */}
            <Terminal
              title="Output Terminal"
              content={output}
              isOutput={true}
              onClear={() => setOutput('')}
            />
          </div>
        </div>
        {user && (
          <div className="mt-4 md:mt-0 md:ml-4">
            <Sidebar 
              snippets={snippets}
              onSnippetSelect={(snippet) => {
                setCode(snippet.code);
                setSelectedLanguage(snippet.language_name);
              }}
            />
          </div>
        )}
      </div>
    </div>
  );
}
