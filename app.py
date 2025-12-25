"""Main Flask application for AI Learning Platform"""

import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ai_learning.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database Models
class Content(db.Model):
    """Model for storing generated content"""
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Video(db.Model):
    """Model for storing generated videos metadata"""
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    video_path = db.Column(db.String(255), nullable=False)
    video_url = db.Column(db.String(255))
    duration = db.Column(db.Float)
    file_size = db.Column(db.String(50))
    style = db.Column(db.String(50), default='experimental')
    status = db.Column(db.String(50), default='processing')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/', methods=['GET'])
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/api/generate-content', methods=['POST'])
def generate_content():
    """API endpoint to generate educational content"""
    try:
        data = request.get_json()
        topic = data.get('topic')
        language = data.get('language', 'en')
        depth = data.get('depth', 'intermediate')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        # TODO: Implement content generation logic
        # This will integrate with OpenAI GPT for content synthesis
        
        # Mock response for now
        response = {
            'id': 1,
            'topic': topic,
            'title': f'Introduction to {topic}',
            'description': f'Learn about {topic} with our AI-powered platform',
            'sections': [
                {
                    'title': 'Overview',
                    'content': f'This section provides an overview of {topic}...'
                }
            ],
            'created_at': datetime.utcnow().isoformat(),
            'status': 'completed'
        }
        
        return jsonify(response), 201
        
    except Exception as e:
        logger.error(f'Error generating content: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/generate-video', methods=['POST'])
def generate_video():
    """API endpoint to generate video from content"""
    try:
        data = request.get_json()
        content_id = data.get('content_id')
        style = data.get('style', 'experimental')
        
        if not content_id:
            return jsonify({'error': 'Content ID is required'}), 400
        
        # TODO: Implement video generation logic
        # This will use MoviePy and FFmpeg for video creation
        
        response = {
            'video_id': 1,
            'content_id': content_id,
            'video_url': '/outputs/videos/video_1.mp4',
            'duration': 120,
            'file_size': '45.2 MB',
            'style': style,
            'status': 'completed'
        }
        
        return jsonify(response), 201
        
    except Exception as e:
        logger.error(f'Error generating video: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/content/<int:content_id>', methods=['GET'])
def get_content(content_id):
    """Retrieve generated content by ID"""
    try:
        content = Content.query.get(content_id)
        if not content:
            return jsonify({'error': 'Content not found'}), 404
        
        return jsonify({
            'id': content.id,
            'topic': content.topic,
            'title': content.title,
            'description': content.description,
            'created_at': content.created_at.isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f'Error retrieving content: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f'Internal server error: {str(error)}')
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    host = os.getenv('APP_HOST', '0.0.0.0')
    port = int(os.getenv('APP_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f'Starting AI Learning Platform on {host}:{port}')
    app.run(host=host, port=port, debug=debug)
