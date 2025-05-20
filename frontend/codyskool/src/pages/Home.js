import React, { useState, useRef } from 'react';
import Navbar from '../components/Navbar';
import CodeEditor from '../components/CodeEditor';
import Terminal from '../components/Terminal';
import API_BASE_URL from '../config';

export default function Home() {
  const [code, setCode] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('Python');
  const [interactiveInput, setInteractiveInput] = useState(''); // current text typed in the prompt
  const [output, setOutput] = useState('');
  const [prompt, setPrompt] = useState(null); // holds prompt message (e.g., "Enter first number:")
  const [user, setUser] = useState(null);
  const [snippets, setSnippets] = useState([]);
  
  const socketRef = useRef(null);

  const languageMapping = {
    Python: 1,
    C: 2,
    "C++": 3
  };

  // Start execution via WebSocket.
  const handleRun = () => {
    setOutput('');
    setPrompt(null);
    
    if (socketRef.current) {
      socketRef.current.close();
    }
    const wsUrl = process.env.REACT_APP_WS_URL || `wss://cuddly-octo-fishstick.onrender.com/ws/interactive/`;
    const socket = new WebSocket(wsUrl);
    socketRef.current = socket;

    socket.onopen = () => {
      const payload = {
        action: "start",
        language: selectedLanguage.toLowerCase(),
        code: code
      };
      socket.send(JSON.stringify(payload));
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.output) {
          setOutput(prev => prev + data.output);
        }
        if (data.prompt) {
          setPrompt(data.prompt);
        }
        if (data.error) {
          setOutput(prev => prev + "\nError: " + data.error);
        }
      } catch (err) {
        console.error("Error parsing message:", err);
      }
    };

    socket.onerror = (errorEvent) => {
      console.error("WebSocket error:", errorEvent);
      setOutput(prev => prev + "\nSocket error: " + JSON.stringify(errorEvent));
    };

    socket.onclose = () => {
      console.log("WebSocket connection closed.");
    };
  };

  // Stop execution by closing the WebSocket.
  const handleStop = () => {
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
    }
  };

  // Handles the sending of the prompt input.
  const handleSendInput = (inputText) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      // Echo only the input value, not the prompt text.
      setOutput(prev => prev  + inputText + "\n");
      setPrompt(null); // clear the prompt
      const payload = { action: "input", data: inputText };
      socketRef.current.send(JSON.stringify(payload));
    } else {
      console.warn("No open WebSocket connection to send input.");
    }
  };

  const handleClear = () => {
    setCode('');
  };

  // Handler for saving code snippets.
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

  return (
    <div className="min-h-screen bg-yellow-50">
      <Navbar />
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
            <Terminal
              title="Terminal"
              output={output}
              input={interactiveInput}
              setInput={setInteractiveInput}
              onSendInput={handleSendInput}
              onClear={() => { setOutput(''); setPrompt(null); }}
              prompt={prompt}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
