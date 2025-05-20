CodySkool is an interactive online code execution environment similar to [online-python.com](https://www.online-python.com/), built with Django, React, WebSockets, and Docker. The application allows users to write, compile, and execute code in different programming languages within a web browser.

![CodySkool Architecture](https://i.ibb.co/YL6BpHM/codyskool-architecture.png)

## Table of Contents
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Local Setup Instructions](#local-setup-instructions)
- [Deployment](#deployment)
- [Workflow Explanation](#workflow-explanation)
- [Project Structure](#project-structure)
- [Advantages of this Setup](#advantages-of-this-setup)
- [Security Considerations](#security-considerations)
- [Future Enhancements](#future-enhancements)

## Features

- **Python execution support**: Focus on Python code execution (extensible architecture)
- **Real-time code execution** via WebSockets
- **Interactive input/output**: Handle program input prompts and responses
- **Secure execution environment**: Code runs in isolated Docker containers
- **Responsive UI**: Modern React-based interface with syntax highlighting
- **Resource limitations**: Memory and CPU restrictions for executed code
- **Compilation support**: For languages like C/C++
- **Error handling**: Proper display of compilation and runtime errors

## System Architecture

The system follows a client-server architecture with the following components:

1. **Frontend**: React-based UI with Tailwind CSS for code editing and displaying execution results
2. **Backend**: Django application with Channels (WebSockets) for real-time communication
3. **Execution Environment**: Docker containers for secure Python code execution
4. **WebSocket Communication**: Bidirectional messaging between frontend and backend

```
┌──────────────────┐                    ┌────────────────────────┐
│                  │    WebSockets      │                        │
│  React Frontend  │◄──────────────────►│  Django + Channels     │
│  (Code Editor UI)│                    │  (WebSocket Consumer)  │
│                  │                    │                        │
└──────────────────┘                    └───────────┬────────────┘
                                                    │
                                                    │ Execute Code
                                                    ▼
                                        ┌────────────────────────┐
                                        │  Docker Container      │
                                        │  (Python Execution)    │
                                        │                        │
                                        └────────────────────────┘
```

## Technology Stack

- **Frontend**:
  - React
  - Tailwind CSS
  - Code editor component (e.g., Monaco or CodeMirror)
  - WebSocket client

- **Backend**:
  - Django (Python web framework)
  - Django Channels (WebSocket support)
  - Daphne (ASGI server)

- **Execution Environment**:
  - Docker
  - Python interpreter

## Local Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/codyskool.git
   cd codyskool
   ```

2. **Set up Python virtual environment**
   ```bash
   cd backend/code_editor_backened
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Build the code executor Docker image**
   ```bash
   sudo docker build -t code_executor_image -f Dockerfile.executor .
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

### Frontend Setup

1. **Navigate to the frontend directory**
   ```bash
   cd ../../frontend/codyskool
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Build the frontend (for production)**
   ```bash
   npm run build
   ```

   Alternatively, for development:
   ```bash
   npm start
   ```

### Running the Application Locally

1. **Start the Django development server with Daphne (from the backend directory)**
   ```bash
   cd ../../backend/code_editor_backened
   daphne -b 0.0.0.0 -p 8000 code_editor_backened.asgi:application
   ```

2. **Access the application**
   Open your browser and navigate to: `http://localhost:8000`

## Deployment

For production deployment, the application is configured to run on Render or similar platforms:

1. **Free Tier Deployment**:
   - The production version uses the native Python interpreter instead of Docker due to free tier limitations of Render
   - The Dockerfile is adjusted to focus on serving the Django application with frontend assets

2. **Full Deployment (with Docker)**:
   - The complete setup with Docker-based code execution can be deployed on platforms that support Docker
   - Environment variables can be configured to adjust paths and settings

## Workflow Explanation

### Code Execution Flow

1. **User Input**:
   - User enters Python code in the editor
   - Clicks "Run" button

2. **WebSocket Communication**:
   - Frontend establishes WebSocket connection to backend
   - Code is sent to the Django server

3. **Backend Processing**:
   - Django Channels consumer receives the request
   - Code saved to temporary file in `code_exec_files` directory
   - Docker container launched with Python interpreter

4. **Execution & Stream Handling**:
   - Code executed in isolated Docker environment
   - Output streamed back to frontend via WebSocket
   - Special handling for interactive input (prompts detected and relayed)

5. **User Interaction**:
   - If program requires input, prompt shown to user
   - User input sent back via WebSocket
   - Process continues until completion or error

6. **Cleanup**:
   - Temporary files managed (retained for debugging purposes)
   - Docker container terminated
   - Resources released

### Interactive Input Handling

The system includes special handling for interactive programs:
- For Python, a wrapper script overrides the `input()` function to detect prompts
- When a prompt is detected, it's marked with "PROMPT:" and sent to frontend
- Frontend displays prompt and waits for user input
- User input is sent back to the running container

## Project Structure

```
codyskool/
├── backened/
│   └── code_editor_backened/
│       ├── code_editor_backened/
│       │   ├── asgi.py             # ASGI config with Channels
│       │   ├── __init__.py
│       │   ├── routing.py          # WebSocket routing
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── wsgi.py
│       ├── code_exec_files/        # Temporary code file storage
│       ├── code_executor_image     # Docker image for code execution 
│       ├── dockerfile              # Main application Dockerfile
│       ├── Dockerfile.executor     # Docker image for code execution
│       ├── editor/
│       │   ├── admin.py
│       │   ├── apps.py
│       │   ├── consumers.py        # WebSocket consumer
│       │   ├── __init__.py
│       │   ├── management/
│       │   ├── migrations/
│       │   ├── models.py
│       │   ├── serializers.py
│       │   ├── services/           # Code execution services
│       │   ├── tests.py
│       │   ├── urls.py
│       │   └── views.py
│       ├── manage.py
│       └── requirements.txt
│
└── frontend/
    └── codyskool/
        ├── package.json
        ├── package-lock.json
        ├── postcss.config.js
        ├── public/
        │   ├── favicon.ico
        │   ├── index.html
        │   ├── logo192.png
        │   ├── logo512.png
        │   ├── manifest.json
        │   └── robots.txt
        ├── src/
        │   ├── App.css
        │   ├── App.js
        │   ├── App.test.js
        │   ├── components/         # UI components
        │   ├── config.js
        │   ├── index.css
        │   ├── index.js
        │   ├── logo.svg
        │   ├── pages/              # Application pages
        │   ├── reportWebVitals.js
        │   └── setupTests.js
        └── tailwind.config.js
```

## Advantages of this Setup

1. **Security**:
   - Code execution happens in isolated Docker containers
   - Resource limitations prevent excessive CPU/memory usage
   - Sandboxed environment protects host system

2. **Real-time Interaction**:
   - WebSockets enable low-latency communication
   - Input/output streams work similar to a local terminal
   - Support for interactive programs requiring user input

3. **Scalability**:
   - Containerized execution enables horizontal scaling
   - Stateless architecture allows load balancing
   - Separate concerns (UI, backend, execution) for better maintainability

4. **Flexibility**:
   - Easy to add support for new programming languages
   - Frontend and backend can be developed independently
   - Docker-based execution is platform-independent

5. **Developer Experience**:
   - Live code execution without installing compilers/interpreters
   - Familiar IDE-like interface
   - Instant feedback on code changes

6. **Deployment Options**:
   - Can be deployed with or without Docker in production
   - Adaptive configuration based on hosting environment

## Security Considerations

1. **Resource Limitations**:
   - Docker containers have memory and CPU restrictions
   - Execution timeouts prevent infinite loops
   - File system access is containerized

2. **Code Isolation**:
   - Each execution runs in a separate container
   - No shared state between executions
   - Prevents interference between user sessions

3. **Input Validation**:
   - Sanitize user inputs to prevent malicious code
   - Restrict access to system resources from executed code

## Future Enhancements

1. **Additional Language Support**:
   - Adding C, C++, JavaScript, Java, Ruby, etc.
   - Support for different versions of Python and other interpreters/compilers

2. **Enhanced Editor Features**:
   - Code completion
   - Syntax error highlighting
   - Multiple files support

3. **Collaboration Features**:
   - Code sharing with unique URLs
   - Real-time collaborative editing
   - Comments and annotations

4. **Learning Resources**:
   - Integration with tutorials
   - Code examples and templates
   - Exercise suggestions

5. **GUI Output Support**:
   - Graphical output for Python programs (matplotlib, Tkinter)
   - Visual representation of program execution
   - Support for interactive GUI elements
