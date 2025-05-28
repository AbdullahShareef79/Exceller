# 📄 Exceller

**Exceller** is a sophisticated document processing platform that converts Word documents into structured Excel files using advanced language models. Built with FastAPI and React, it's designed for professionals who need to efficiently analyze and transform document content.

## 🚀 Features

- ✨ **Modern UI** - Clean, responsive interface built with React and Tailwind CSS
- 🔐 **Secure Authentication** - JWT-based user authentication and authorization
- 📊 **Document Processing**
  - Upload and process Microsoft Word (.docx) files
  - Automatic conversion to structured Excel format
  - Background task processing with Celery
  - Real-time status updates
- 🔄 **Asynchronous Processing**
  - Redis-backed task queue
  - Scalable worker architecture
- 📈 **Monitoring**
  - Prometheus metrics integration
  - Sentry error tracking
  - Detailed logging system
- 🛡️ **Security Features**
  - Secure password hashing with bcrypt
  - Token-based API authentication
  - User-specific document isolation

## 🛠️ Technology Stack

- **Backend**
  - FastAPI (Modern, fast web framework)
  - SQLAlchemy (ORM)
  - Celery (Task Queue)
  - Redis (Message Broker)
  - Pydantic (Data Validation)

- **Frontend**
  - React (UI Components)
  - Tailwind CSS (Styling)
  - Fetch API (HTTP Client)

- **Infrastructure**
  - Prometheus (Metrics)
  - Sentry (Error Tracking)
  - SQLite (Database)

## 💻 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/abdullahshareef79/Exceller.git
   cd Exceller
   ```

2. **Set up Python environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install Redis:**
   - Windows: Download from [Redis for Windows](https://github.com/microsoftarchive/redis/releases)
   - Linux: `sudo apt-get install redis-server`
   - macOS: `brew install redis`

4. **Environment Setup:**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///./app.db
   REDIS_URL=redis://localhost:6379/0
   SENTRY_DSN=your-sentry-dsn  # Optional
   ```

## 🚀 Running the Application

1. **Start Redis:**
   ```bash
   # Redis should be running as a service
   redis-cli ping  # Should return PONG
   ```

2. **Start Celery Worker:**
   ```bash
   celery -A app.tasks.document_processing worker --loglevel=info
   ```

3. **Start FastAPI Application:**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the Application:**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 📚 API Documentation

The API documentation is available at `/docs` when running the application. Key endpoints include:

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/token` - Get authentication token
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents/` - List user's documents
- `GET /api/v1/documents/{id}/download` - Download processed file

## 🧪 Testing

Run the test suite:
```bash
pytest
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- FastAPI for the amazing framework
- Tailwind CSS for the styling utilities
- The open-source community for various tools and libraries

---

## 🚀 Features

- ✅ Upload Microsoft Word (`.docx`) files
- 🧠 Uses LLMs (Ollama, LMStudio, or TextGen) to extract & summarize text
- 📊 Generates structured `.xlsx` outputs
- 🛠️ Command-line and web interface (Flask)
- 🔄 Local file handling for full data privacy

---

## 💻 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/AbdullahShareef79/Exceller.git
cd Exceller
