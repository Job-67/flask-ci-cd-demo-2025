import pytest
import json
from app import app, db, User

class TestBasicRoutes:
    """Test basic application routes"""
    
    def test_home_route(self, client):
        """Test the home route returns correct response"""
        response = client.get('/')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['message'] == 'Flask CI/CD Demo API'
        assert data['version'] == '1.0.0'
        assert data['status'] == 'healthy'
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'status' in data
        assert 'database' in data
        assert 'redis' in data

class TestUserRoutes:
    """Test user-related routes"""
    
    def test_get_users_empty(self, client):
        """Test getting users when database is empty"""
        response = client.get('/users')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_create_user_success(self, client, sample_user):
        """Test successful user creation"""
        response = client.post('/users', 
                             data=json.dumps(sample_user),
                             content_type='application/json')
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['username'] == sample_user['username']
        assert data['email'] == sample_user['email']
        assert 'id' in data
    
    def test_create_user_missing_data(self, client):
        """Test user creation with missing data"""
        response = client.post('/users', 
                             data=json.dumps({'username': 'testuser'}),
                             content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_user_duplicate_username(self, client, sample_user):
        """Test user creation with duplicate username"""
        # Create first user
        client.post('/users', 
                   data=json.dumps(sample_user),
                   content_type='application/json')
        
        # Try to create user with same username
        duplicate_user = {
            'username': sample_user['username'],
            'email': 'different@example.com'
        }
        response = client.post('/users', 
                             data=json.dumps(duplicate_user),
                             content_type='application/json')
        assert response.status_code == 409
    
    def test_create_user_duplicate_email(self, client, sample_user):
        """Test user creation with duplicate email"""
        # Create first user
        client.post('/users', 
                   data=json.dumps(sample_user),
                   content_type='application/json')
        
        # Try to create user with same email
        duplicate_user = {
            'username': 'differentuser',
            'email': sample_user['email']
        }
        response = client.post('/users', 
                             data=json.dumps(duplicate_user),
                             content_type='application/json')
        assert response.status_code == 409
    
    def test_get_user_by_id(self, client, sample_user):
        """Test getting user by ID"""
        # Create user first
        create_response = client.post('/users', 
                                    data=json.dumps(sample_user),
                                    content_type='application/json')
        created_user = json.loads(create_response.data)
        
        # Get user by ID
        response = client.get(f'/users/{created_user["id"]}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['id'] == created_user['id']
        assert data['username'] == sample_user['username']
        assert data['email'] == sample_user['email']
    
    def test_get_user_not_found(self, client):
        """Test getting non-existent user"""
        response = client.get('/users/999')
        assert response.status_code == 404
    
    def test_get_users_with_data(self, client, sample_user):
        """Test getting users when database has data"""
        # Create a user first
        client.post('/users', 
                   data=json.dumps(sample_user),
                   content_type='application/json')
        
        response = client.get('/users')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]['username'] == sample_user['username']

class TestCacheRoutes:
    """Test cache-related routes"""
    
    def test_get_cache_not_found(self, client):
        """Test getting non-existent cache key"""
        response = client.get('/cache/nonexistent')
        # This might return 404 or handle gracefully depending on Redis availability
        assert response.status_code in [404, 200]
    
    def test_set_cache_missing_value(self, client):
        """Test setting cache without value"""
        response = client.post('/cache/testkey', 
                             data=json.dumps({}),
                             content_type='application/json')
        assert response.status_code == 400

class TestErrorHandlers:
    """Test error handling"""
    
    def test_404_handler(self, client):
        """Test 404 error handler"""
        response = client.get('/nonexistent-route')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
