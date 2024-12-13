# Claude Chat Application

A modern, secure web-based chat interface for the Claude AI assistant, built with Flask and JavaScript. This application provides a real-time chat experience with code highlighting, message history, and a clean user interface.

## 🌟 Features

- **Real-time Chat Interface**: Smooth, responsive chat experience with Claude AI
- **Code Highlighting**: Automatic syntax highlighting for code snippets
- **Message History**: Persistent conversation history using Flask sessions
- **Copy Code Functionality**: Easy code copying with a single click
- **Markdown Support**: Renders markdown-style messages properly
- **Security Features**: Implemented security headers and CSRF protection
- **Responsive Design**: Works on both desktop and mobile devices
- **Type Indicators**: Visual feedback while Claude is processing responses

## 🔧 Technical Stack

- **Backend**: Python/Flask
- **Frontend**: HTML5, JavaScript, TailwindCSS
- **AI Integration**: Claude-3 API (Anthropic)
- **Security**: Flask-Talisman, Session Management
- **Styling**: Tailwind CSS, Font Awesome
- **Code Highlighting**: highlight.js

## 📋 Prerequisites
- Python 3.8+
- Anthropic API Key
- Modern web browser
- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository**
  ```bash
  git clone https://github.com/yourusername/claude-chat-app.git
  cd claude-chat-app
  ```
2. **Create and activate virtual environment**
  ```bash
  python -m venv .venv
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
  ```
3. **Install dependencies**
  ```bash
  pip install -r requirements.txt
  ```
4. **Create environment file**
Create a `.env` file in the root directory:
  ```env
  ANTHROPIC_API_KEY=your_api_key_here
  SECRET_KEY=your_secret_key_here
  FLASK_ENV=development
  ```


## 🔧 Configuration

The application can be configured through the `config.py` file:

- `SESSION_TYPE`: Session storage type (default: filesystem)
- `SESSION_PERMANENT`: Session permanence flag
- `PERMANENT_SESSION_LIFETIME`: Session lifetime
- Security headers and CSP settings can be adjusted in `run.py`

## 🚀 Running the Application

1. **Start the Flask server**
```bash
python run.py
```

2. **Access the application**
Open your web browser and navigate to: `http://127.0.0.1:5000`


## 📁 Project Structure

```bash
claude-chat-app/
├── .gitignore
├── README.md
├── requirements.txt
├── config.py
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   │       └── chat.js
│   └── templates/
│       └── index.html
└── run.py
```

## 🔒 Security Features

- HTTPS enforcement (in production)
- Secure session management
- Content Security Policy (CSP)
- CSRF protection
- XSS prevention
- Secure headers

## 💻 Development

### Debug Mode
Run the application in debug mode for development: `FLASK_ENV=development python run.py`


### Logging
Logs are written to `app.log` and include:
- API requests and responses
- Error tracking
- Debug information (in development)

## 🔍 API Endpoints

- `GET /`: Main chat interface
- `POST /api/chat`: Send messages to Claude
- `GET /api/get-conversation`: Retrieve conversation history

## ⚙️ Environment Variables

- `ANTHROPIC_API_KEY`: Your Claude API key
- `SECRET_KEY`: Flask session secret key
- `FLASK_ENV`: Application environment
- `FLASK_HOST`: Host to bind (default: 127.0.0.1)
- `FLASK_PORT`: Port to use (default: 5000)

## 🚧 Production Deployment

For production deployment:

1. Use a production WSGI server (e.g., Gunicorn)
2. Enable HTTPS
3. Set appropriate security headers
4. Use environment variables for sensitive data
5. Configure proper logging

Example production server start: `gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"`


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Anthropic for the Claude AI API
- Flask team for the excellent web framework
- TailwindCSS for the styling framework
- highlight.js team for code highlighting

## 📞 Support

For support, please:
1. Check existing issues
2. Create a new issue with detailed information
3. Provide logs and steps to reproduce

## 🔄 Updates

Check the [CHANGELOG.md](CHANGELOG.md) for version history and updates.




