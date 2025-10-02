import pytest
import os
import tempfile
from unittest.mock import patch
from app import app, db, User

@pytest.fixture
def client():
    # Create a temporary database
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Mock Redis for testing
    with patch('app.redis_client') as mock_redis:
        mock_redis.ping.return_value = True
        mock_redis.get.return_value = None
        mock_redis.set.return_value = True
        
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                yield client
                db.drop_all()
    
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

@pytest.fixture
def sample_user():
    return {
        'username': 'testuser',
        'email': 'test@example.com'
    }
