# Flask API Extended Reference

## Flask-SQLAlchemy Query Reference

### Common Query Patterns

```python
from sqlalchemy.orm import joinedload

# Basic CRUD
User.query.all()
User.query.first()
User.query.get_or_404(user_id)
User.query.filter_by(username="john").first()
User.query.filter(User.age > 18).all()

# Complex queries
from sqlalchemy import and_, or_, desc

User.query.filter(
    and_(User.age >= 18, User.is_active == True)
).order_by(desc(User.created_at)).all()

# Eager loading (prevents N+1)
User.query.options(joinedload(User.posts)).all()

# Count
User.query.count()
User.query.filter(User.is_active == True).count()

# Exists
from sqlalchemy import exists
User.query.filter(exists().where(Post.user_id == User.id)).all()
```

---

## Flask-JWT-Extended Full Options

### Configuration Keys

| Key | Default | Description |
|-----|---------|-------------|
| `JWT_SECRET_KEY` | `None` | Required. Secret for signing tokens |
| `JWT_ACCESS_TOKEN_EXPIRES` | `timedelta(hours=1)` | Access token lifetime |
| `JWT_REFRESH_TOKEN_EXPIRES` | `timedelta(days=30)` | Refresh token lifetime |
| `JWT_TOKEN_LOCATION` | `["headers"]` | Where to look for tokens |
| `JWT_HEADER_NAME` | `Authorization` | Header name |
| `JWT_HEADER_TYPE` | `Bearer` | Header prefix |
| `JWT_BLACKLIST_ENABLED` | `False` | Enable token revocation |
| `JWT_BLACKLIST_TOKEN_CHECKS` | `["access", "refresh"]` | Token types to check |

### Decorators

```python
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, get_jwt,
    verify_jwt_in_request, create_access_token,
    create_refresh_token, unset_jwt_cookies
)

@jwt_required()                    # Requires valid access token
@jwt_required(refresh=True)        # Requires valid refresh token
@jwt_required(optional=True)       # Token optional; None if missing
@jwt_required(fresh=True)          # Requires fresh token (not refreshed)
@jwt_required(locations=["cookies"])  # Look in cookies
```

---

## Flask-Migrate Commands

```bash
flask db init              # Initialize migrations
flask db migrate -m "msg"  # Generate migration
flask db upgrade           # Apply migrations
flask db downgrade         # Rollback last migration
flask db history           # Show migration history
flask db current           # Show current revision
flask db stamp head        # Mark current DB as up-to-date
```

---

## SQLAlchemy Relationships

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posts = db.relationship("Post", backref="author", lazy="dynamic")

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
```

| Lazy Type | Behavior |
|-----------|----------|
| `select` | Default. Query on first access |
| `joined` | Eager load with JOIN |
| `subquery` | Eager load with subquery |
| `dynamic` | Returns Query object (chainable) |
| `raise` | Raises error if accessed without eager load |

---

## Gunicorn Configuration

```python
# gunicorn.conf.py
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
timeout = 30
keepalive = 2
errorlog = "-"
accesslog = "-"
capture_output = True
enable_stdio_inheritance = True
```

---

## Flask-Limiter Quick Setup

```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
limiter.init_app(app)

# In routes
@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    ...
```
