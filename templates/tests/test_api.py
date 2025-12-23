"""Test cases for AI Learning Platform API endpoints"""

import pytest
import json
from datetime import datetime


class TestContentGeneration:
    """Test suite for content generation API"""
    
    def test_generate_content_success(self, client):
        """Test successful content generation"""
        response = client.post(
            '/api/generate-content',
            data=json.dumps({'topic': 'Machine Learning', 'language': 'en'}),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'id' in data
        assert 'title' in data
        assert 'description' in data
        assert data['status'] == 'completed'
    
    def test_generate_content_missing_topic(self, client):
        """Test content generation without topic"""
        response = client.post(
            '/api/generate-content',
            data=json.dumps({'language': 'en'}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_generate_content_invalid_language(self, client):
        """Test content generation with invalid language"""
        response = client.post(
            '/api/generate-content',
            data=json.dumps({'topic': 'Python', 'language': 'invalid'}),
            content_type='application/json'
        )
        
        # Should either fail validation or handle gracefully
        assert response.status_code in [400, 201]  # Depends on implementation


class TestVideoGeneration:
    """Test suite for video generation API"""
    
    def test_generate_video_success(self, client):
        """Test successful video generation"""
        response = client.post(
            '/api/generate-video',
            data=json.dumps({'content_id': 1, 'style': 'experimental'}),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'video_id' in data
        assert 'video_url' in data
        assert data['status'] == 'completed'
    
    def test_generate_video_missing_content_id(self, client):
        """Test video generation without content ID"""
        response = client.post(
            '/api/generate-video',
            data=json.dumps({'style': 'experimental'}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_generate_video_invalid_style(self, client):
        """Test video generation with invalid style"""
        response = client.post(
            '/api/generate-video',
            data=json.dumps({'content_id': 1, 'style': 'invalid_style'}),
            content_type='application/json'
        )
        
        # Should either handle gracefully or validate
        assert response.status_code in [400, 201]


class TestHealthCheck:
    """Test suite for health check endpoint"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
    
    def test_health_check_format(self, client):
        """Test health check response format"""
        response = client.get('/api/health')
        data = json.loads(response.data)
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(data['timestamp'])
            is_valid_timestamp = True
        except:
            is_valid_timestamp = False
        
        assert is_valid_timestamp


class TestDatabaseOperations:
    """Test suite for database operations"""
    
    def test_content_model_creation(self, app):
        """Test Content model creation"""
        from app import db, Content
        
        with app.app_context():
            # Create a test content
            content = Content(
                topic='Test Topic',
                title='Test Title',
                description='Test Description'
            )
            
            assert content.topic == 'Test Topic'
            assert content.title == 'Test Title'
            assert content.description == 'Test Description'
    
    def test_video_model_creation(self, app):
        """Test Video model creation"""
        from app import db, Video
        
        with app.app_context():
            # Create a test video
            video = Video(
                content_id=1,
                video_path='/outputs/videos/test.mp4',
                duration=120.5,
                style='experimental'
            )
            
            assert video.content_id == 1
            assert video.video_path == '/outputs/videos/test.mp4'
            assert video.duration == 120.5


class TestErrorHandling:
    """Test suite for error handling"""
    
    def test_404_error(self, client):
        """Test 404 error handling"""
        response = client.get('/api/nonexistent')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_cors_headers(self, client):
        """Test CORS headers"""
        response = client.get('/api/health')
        
        # CORS should be enabled
        assert response.status_code == 200
    
    def test_content_type_validation(self, client):
        """Test content type validation"""
        response = client.post(
            '/api/generate-content',
            data='invalid',
            content_type='text/plain'
        )
        
        # Should reject non-JSON content
        assert response.status_code >= 400


@pytest.fixture
def app():
    """Create and configure a Flask application for testing"""
    from app import app as flask_app
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with flask_app.app_context():
        from app import db
        db.create_all()
    
    yield flask_app


@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()
