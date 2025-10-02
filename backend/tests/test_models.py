import pytest
from app import app, db, User

class TestUserModel:
    """Test User model functionality"""
    
    def test_user_creation(self, client):
        """Test creating a user model"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.username == 'testuser'
            assert user.email == 'test@example.com'
    
    def test_user_to_dict(self, client):
        """Test user to_dict method"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            db.session.add(user)
            db.session.commit()
            
            user_dict = user.to_dict()
            assert isinstance(user_dict, dict)
            assert user_dict['username'] == 'testuser'
            assert user_dict['email'] == 'test@example.com'
            assert 'id' in user_dict
    
    def test_user_unique_constraints(self, client):
        """Test user unique constraints"""
        with app.app_context():
            # Create first user
            user1 = User(username='testuser', email='test@example.com')
            db.session.add(user1)
            db.session.commit()
            
            # Try to create user with same username
            user2 = User(username='testuser', email='different@example.com')
            db.session.add(user2)
            
            with pytest.raises(Exception):  # Should raise integrity error
                db.session.commit()
            
            db.session.rollback()
            
            # Try to create user with same email
            user3 = User(username='differentuser', email='test@example.com')
            db.session.add(user3)
            
            with pytest.raises(Exception):  # Should raise integrity error
                db.session.commit()
    
    def test_user_query(self, client):
        """Test querying users"""
        with app.app_context():
            # Create test users
            user1 = User(username='user1', email='user1@example.com')
            user2 = User(username='user2', email='user2@example.com')
            
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
            
            # Query all users
            users = User.query.all()
            assert len(users) == 2
            
            # Query by username
            found_user = User.query.filter_by(username='user1').first()
            assert found_user is not None
            assert found_user.username == 'user1'
            
            # Query by email
            found_user = User.query.filter_by(email='user2@example.com').first()
            assert found_user is not None
            assert found_user.email == 'user2@example.com'
