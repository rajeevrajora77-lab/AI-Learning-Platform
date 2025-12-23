# AI-Learning-Platform

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/rajeevrajora77-lab/AI-Learning-Platform)](https://github.com/rajeevrajora77-lab/AI-Learning-Platform)

An intelligent AI-powered learning platform that revolutionizes education by automatically generating comprehensive educational content and creating engaging experimental videos. Simply input a topic, and the platform intelligently gathers information, generates well-structured content, and produces creative videos to make learning easier and more interactive.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Features

### Core Features

✨ **Intelligent Content Generation**
- Automatic topic research and information gathering
- AI-powered content synthesis using advanced LLMs
- Structured text generation with proper formatting
- Multi-language support for global accessibility

🎬 **Creative Video Generation**
- Automated video creation from text content
- Text-to-speech voice narration integration
- Dynamic visual scene generation
- Experimental creative styles for engaging presentation

📚 **Learning Management**
- Topic-based course creation
- Progress tracking and analytics
- Content curation and organization
- Interactive learning modules

🔧 **Developer-Friendly**
- RESTful API for easy integration
- Comprehensive documentation
- Example scripts and notebooks
- Docker support for deployment

⚡ **Performance**
- Asynchronous processing for large content
- Caching mechanisms for faster retrieval
- Optimized video rendering pipeline
- Scalable architecture

## Architecture

```
┌─────────────────────────────────────────┐
│     Web Interface (Frontend)            │
│     HTML/CSS/JavaScript                 │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│     Flask/FastAPI Backend               │
│     REST API Server                     │
└──────────────────┬──────────────────────┘
        │          │          │
        ▼          ▼          ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Content      │ │ Video        │ │ Database     │
│ Generation   │ │ Generation   │ │ & Storage    │
│ Module       │ │ Module       │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
        │          │          │
        ▼          ▼          ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Google API   │ │ MoviePy      │ │ PostgreSQL/  │
│ OpenAI GPT   │ │ FFmpeg       │ │ MongoDB      │
│ Wikipedia    │ │ pyttsx3      │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- FFmpeg (for video processing)
- 2GB RAM minimum
- Internet connection for API calls

### Step 1: Clone the Repository

```bash
git clone https://github.com/rajeevrajora77-lab/AI-Learning-Platform.git
cd AI-Learning-Platform
```

### Step 2: Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your API keys
echo "OPENAI_API_KEY=your_key_here" >> .env
echo "GOOGLE_API_KEY=your_key_here" >> .env
```

### Step 5: Run the Application

```bash
python app.py
```

Application will be available at `http://localhost:5000`

## Usage

### Basic Usage - Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. Enter a topic in the input field (e.g., "Photosynthesis")
3. Click "Generate Content"
4. Wait for the content generation and video creation process
5. Review the generated content and video
6. Download the video or save to library

### Python API Usage

```python
from src.content_generator import ContentGenerator
from src.video_generator import VideoGenerator

# Initialize generators
content_gen = ContentGenerator(api_key='your_openai_key')
video_gen = VideoGenerator()

# Generate content
topic = "Machine Learning Basics"
content = content_gen.generate(topic)

print(content['title'])
print(content['description'])
print(content['sections'])

# Generate video
video_path = video_gen.create_video(
    content=content,
    output_format='mp4',
    style='experimental'
)

print(f"Video created: {video_path}")
```

### REST API Usage

```bash
# Generate content
curl -X POST http://localhost:5000/api/generate-content \
  -H "Content-Type: application/json" \
  -d '{"topic": "Quantum Physics"}'

# Response
{
  "id": "uuid",
  "topic": "Quantum Physics",
  "title": "Introduction to Quantum Physics",
  "content": {...},
  "status": "completed"
}

# Generate video
curl -X POST http://localhost:5000/api/generate-video \
  -H "Content-Type: application/json" \
  -d '{"content_id": "uuid", "style": "experimental"}'
```

## Project Structure

```
AI-Learning-Platform/
│
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── LICENSE                         # MIT License
│
├── src/                            # Source code
│   ├── __init__.py
│   ├── content_generator.py        # Content generation module
│   ├── video_generator.py          # Video creation module
│   ├── api_client.py               # External API integration
│   ├── database.py                 # Database operations
│   └── utils.py                    # Utility functions
│
├── templates/                      # HTML templates
│   ├── base.html                   # Base template
│   ├── index.html                  # Home page
│   ├── dashboard.html              # Dashboard
│   └── content.html                # Content viewer
│
├── static/                         # Static files
│   ├── css/
│   │   └── style.css               # Main stylesheet
│   ├── js/
│   │   └── script.js               # JavaScript functionality
│   └── assets/
│       └── images/
│
├── outputs/                        # Generated content
│   ├── videos/                     # Generated videos
│   └── content/                    # Text content files
│
├── docs/                           # Documentation
│   ├── API.md                      # API documentation
│   ├── INSTALLATION.md             # Installation guide
│   ├── CONFIGURATION.md            # Configuration guide
│   └── EXAMPLES.md                 # Usage examples
│
├── tests/                          # Test files
│   ├── test_content_generator.py
│   ├── test_video_generator.py
│   └── test_api.py
│
├── notebooks/                      # Jupyter notebooks
│   └── demo.ipynb                  # Demo notebook
│
└── docker/                         # Docker configuration
    └── Dockerfile                  # Docker build file
```

## Technologies Used

### Backend
- **Python 3.8+** - Core programming language
- **Flask** - Web framework for REST API
- **OpenAI GPT** - Content generation
- **Google APIs** - Information gathering
- **MoviePy** - Video processing
- **FFmpeg** - Multimedia framework
- **pyttsx3** - Text-to-speech conversion

### Frontend
- **HTML5** - Markup language
- **CSS3** - Styling
- **JavaScript** - Interactive functionality
- **Bootstrap** - Responsive design framework

### Database & Storage
- **SQLAlchemy** - ORM
- **PostgreSQL/SQLite** - Database
- **Firebase Storage** - Cloud storage (optional)

### DevOps
- **Docker** - Containerization
- **GitHub Actions** - CI/CD
- **Heroku/AWS** - Deployment

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key

# API Keys
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# Database
DATABASE_URL=sqlite:///app.db

# Video Settings
VIDEO_FORMAT=mp4
VIDEO_QUALITY=1080p
FRAME_RATE=30

# Output Paths
OUTPUT_DIR=./outputs
VIDEO_OUTPUT_DIR=./outputs/videos
CONTENT_OUTPUT_DIR=./outputs/content

# Logging
LOG_LEVEL=INFO
```

## API Documentation

### Endpoints

#### POST `/api/generate-content`
Generate educational content for a given topic.

**Request:**
```json
{
  "topic": "string",
  "language": "string (optional, default: en)",
  "depth": "string (basic|intermediate|advanced, default: intermediate)"
}
```

**Response:**
```json
{
  "id": "uuid",
  "topic": "string",
  "title": "string",
  "description": "string",
  "sections": ["array of content sections"],
  "created_at": "timestamp",
  "status": "completed"
}
```

#### POST `/api/generate-video`
Create a video from generated content.

**Request:**
```json
{
  "content_id": "uuid",
  "style": "string (experimental|professional|casual)",
  "duration": "integer (minutes)"
}
```

**Response:**
```json
{
  "video_id": "uuid",
  "content_id": "uuid",
  "video_url": "string",
  "duration": "integer",
  "file_size": "string",
  "status": "completed"
}
```

#### GET `/api/content/{id}`
Retrieve generated content by ID.

**Response:** Content object

#### GET `/api/video/{id}`
Retrieve generated video by ID.

**Response:** Video metadata

## Examples

### Example 1: Generate Content About Climate Change

```python
from src.content_generator import ContentGenerator

generator = ContentGenerator(api_key='your_key')
content = generator.generate("Climate Change", depth="intermediate")

for section in content['sections']:
    print(f"## {section['title']}")
    print(section['content'])
    print()
```

### Example 2: Create Educational Video

```python
from src.video_generator import VideoGenerator
from src.content_generator import ContentGenerator

content_gen = ContentGenerator()
video_gen = VideoGenerator()

topic = "Python Programming Basics"
content = content_gen.generate(topic)
video = video_gen.create_video(
    content=content,
    style='experimental',
    narrator_voice='en-US-Neural2-C'
)

print(f"Video saved at: {video['path']}")
print(f"Duration: {video['duration']} seconds")
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact & Support

- **Author**: Rajeev Rajora
- **Email**: rajeevrajora77@gmail.com
- **GitHub**: [@rajeevrajora77-lab](https://github.com/rajeevrajora77-lab)
- **Issues**: [GitHub Issues](https://github.com/rajeevrajora77-lab/AI-Learning-Platform/issues)

## Acknowledgments

- OpenAI for GPT models
- Google for search and translation APIs
- MoviePy community for video processing
- Bootstrap for UI framework

---

**Made with ❤️ by Rajeev Rajora**
