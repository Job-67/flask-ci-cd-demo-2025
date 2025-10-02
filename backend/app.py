import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Use SQLite for local development if PostgreSQL is not available
default_db_url = 'sqlite:///app.db'
if os.environ.get('FLASK_ENV') == 'testing':
    default_db_url = 'sqlite:///:memory:'
elif os.environ.get('DATABASE_URL'):
    default_db_url = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = default_db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# Redis connection
redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379')
try:
    redis_client = redis.from_url(redis_url, decode_responses=True)
    # Test connection
    redis_client.ping()
except Exception:
    # Use fake redis for testing/development when Redis is not available
    try:
        import fakeredis
        redis_client = fakeredis.FakeRedis(decode_responses=True)
    except ImportError:
        # Fallback to a mock object
        class MockRedis:
            def ping(self): return True
            def get(self, key): return None
            def set(self, key, value): return True
        redis_client = MockRedis()

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

# Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'Flask CI/CD Demo API',
        'version': '1.0.0',
        'status': 'healthy'
    })

@app.route('/health')
def health_check():
    try:
        # Check database connection
        db.session.execute(db.text('SELECT 1'))
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    try:
        # Check Redis connection
        redis_client.ping()
        redis_status = 'healthy'
    except Exception as e:
        redis_status = f'unhealthy: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'redis': redis_status
    })

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Username and email are required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409
    
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/cache/<key>', methods=['GET'])
def get_cache(key):
    value = redis_client.get(key)
    if value is None:
        return jsonify({'error': 'Key not found'}), 404
    return jsonify({'key': key, 'value': value})

@app.route('/cache/<key>', methods=['POST'])
def set_cache(key):
    data = request.get_json()
    if not data or 'value' not in data:
        return jsonify({'error': 'Value is required'}), 400
    
    redis_client.set(key, data['value'])
    return jsonify({'key': key, 'value': data['value']})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
