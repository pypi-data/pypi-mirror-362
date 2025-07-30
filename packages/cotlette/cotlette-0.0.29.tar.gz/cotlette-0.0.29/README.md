![PyPI Version](https://img.shields.io/pypi/v/cotlette)
![Python Versions](https://img.shields.io/pypi/pyversions/cotlette)
![License](https://img.shields.io/pypi/l/cotlette)
![Downloads](https://img.shields.io/pypi/dm/cotlette)

# Cotlette 🚀

**Cotlette** is a modern, Django-inspired web framework built on top of **FastAPI**. It combines the best of both worlds: the speed and async power of FastAPI with the convenience of Django-like project structure, ORM, templates, and management commands.

---

## Key Features

- **FastAPI Under the Hood**: High-performance async web framework
- **Django-like Project Structure**: Familiar and easy to organize
- **SQLAlchemy-powered ORM**: Simple, Pythonic, and extensible with support for multiple databases
- **Alembic Migrations**: Powerful database migration system
- **Jinja2 Templates**: Powerful and flexible HTML rendering
- **Admin Panel**: Built-in, customizable (inspired by Django admin)
- **Management Commands**: CLI for project/app creation, server, shell, migrations, and more
- **Asynchronous Support**: Full async views and endpoints with automatic context detection
- **Multi-Database Support**: SQLite, PostgreSQL, MySQL, Oracle, and more
- **Extensible**: Add your own apps, middleware, commands, and more

---

## 🎯 URL-Based Async/Sync Mode Detection

Cotlette uses **URL-based mode detection** to determine whether to use synchronous or asynchronous database operations. This approach provides explicit control and predictable behavior across all frameworks.

### How It Works

The mode is determined by the presence of async drivers in your database URL:

```python
# Synchronous mode (default)
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'sqlite:///' + str(BASE_DIR / 'db.sqlite3'),  # Sync mode
    }
}

# Asynchronous mode  
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'sqlite+aiosqlite:///' + str(BASE_DIR / 'db.sqlite3'),  # Async mode
    }
}
```

### Supported Database Drivers

**Synchronous Drivers:**
- SQLite: `sqlite:///db.sqlite3`
- PostgreSQL: `postgresql://user:pass@localhost/dbname`
- MySQL: `mysql://user:pass@localhost/dbname`
- Oracle: `oracle://user:pass@localhost/dbname`

**Asynchronous Drivers:**
- SQLite: `sqlite+aiosqlite:///db.sqlite3`
- PostgreSQL: `postgresql+asyncpg://user:pass@localhost/dbname`
- MySQL: `mysql+aiomysql://user:pass@localhost/dbname`

### Benefits

- ✅ **Explicit Control**: You choose the mode explicitly in settings
- ✅ **Predictable Behavior**: No dependency on execution context
- ✅ **Framework Agnostic**: Works with FastAPI, Django, Flask, or any framework
- ✅ **Easy Switching**: Simply change the URL to switch modes
- ✅ **Clear Intent**: URL clearly shows sync or async database drivers

---

## Quick Start

### 1. Install Cotlette
```bash
pip install cotlette
```

### 2. Create a New Project
```bash
cotlette startproject myproject
cd myproject
```

### 3. Run the Development Server
```bash
cotlette runserver
```

Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000/)

---

## Example Projects

Cotlette comes with two complete example projects demonstrating both synchronous and asynchronous modes:

### Synchronous Example (`example/`)
```bash
cd example
cotlette runserver
```
- Uses `sqlite:///db.sqlite3` (synchronous mode)
- Direct iteration: `for user in users:`
- Direct template passing: `"users": users`

### Asynchronous Example (`example_async/`)
```bash
cd example_async
cotlette runserver
```
- Uses `sqlite+aiosqlite:///db.sqlite3` (asynchronous mode)
- Async iteration: `async for user in users:`
- Template execution: `"users": await users.execute()`

---

## Project Configuration

### Settings Structure
```python
# config/settings.py
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'sqlite:///' + str(BASE_DIR / 'db.sqlite3'),  # Sync mode
        # 'URL': 'sqlite+aiosqlite:///' + str(BASE_DIR / 'db.sqlite3'),  # Async mode
    }
}

INSTALLED_APPS = [
    'apps.home',
    'apps.admin',
    'apps.users',
    'apps.accounts',
    'apps.groups',
]

TEMPLATES = [
    {
        "BACKEND": "cotlette.template.backends.jinja2.Jinja2",
        "DIRS": ["templates"],
        "APP_DIRS": True
    },
]

SECRET_KEY = b'your-secret-key'
ALGORITHM = "HS256"
```

## Screenshots

**Home Page:**
![Home Page](.docs/img/first_page.jpg)

**Login Page:**
![Login Page](.docs/img/login_page.jpg)

**Admin Panel:**
![Admin Page](.docs/img/admin_page.jpg)

---

## Example: Defining a Model
```python
from cotlette.core.database import Model, CharField, IntegerField, AutoField
from cotlette.core.database.fields.related import ForeignKeyField

class UserModel(Model):
    table = "users_usermodel"
    
    id = AutoField()  # Primary key
    name = CharField(max_length=50)
    age = IntegerField()
    email = CharField(max_length=100)
    password_hash = CharField(max_length=255)
    group = ForeignKeyField(to="GroupModel", related_name="users")
    organization = CharField(max_length=100)
```

---

## Universal ORM Usage

Cotlette ORM automatically detects the mode based on your database URL configuration and works accordingly. No need for separate sync/async methods!

### Basic CRUD Operations
```python
# Create
article = Article.objects.create(title="Hello", content="World", author_id=1)

# Get single object
user = UserModel.objects.get(id=1)
user = UserModel.objects.get(email="john@example.com")

# Filter
users = UserModel.objects.filter(age__gte=25).execute()
users = UserModel.objects.filter(group_id=1).execute()

# Update
user.name = "Jane Doe"
user.save()

# Delete
user.delete()

# Count
count = UserModel.objects.count()
active_users = UserModel.objects.filter(age__gte=18).count()

# Exists
exists = UserModel.objects.filter(email="john@example.com").exists()
```

### In Async Mode
When using async database URLs, the same methods automatically work asynchronously:

```python
async def async_view():
    # Create
    article = await Article.objects.create(title="Hello", content="World", author_id=1)
    
    # Get
    user = await UserModel.objects.get(id=1)
    
    # Filter
    users = await UserModel.objects.filter(age__gte=25).execute()
    
    # Update
    user.name = "Jane Doe"
    await user.save()
    
    # Delete
    await user.delete()
    
    # Count
    count = await UserModel.objects.count()
    
    # Exists
    exists = await UserModel.objects.filter(email="john@example.com").exists()
```

---

## Example: Creating Views

### Synchronous View (with sync database URL)
```python
from fastapi import APIRouter, Request
from cotlette.shortcuts import render_template
from starlette.authentication import requires
from .models import UserModel

router = APIRouter()

@router.get("/users", response_model=None)
@requires("user_auth")
async def users_view(request: Request):
    users = UserModel.objects.all()  # Direct iteration works in sync mode
    
    return render_template(request=request, template_name="admin/users.html", context={
        "users": users,  # Can be passed directly to template
        "config": request.app.settings,
    })
```

### Asynchronous View (with async database URL)
```python
from fastapi import APIRouter, Request
from cotlette.shortcuts import render_template
from starlette.authentication import requires
from .models import UserModel

router = APIRouter()

@router.get("/users", response_model=None)
@requires("user_auth")
async def users_view(request: Request):
    users = UserModel.objects.all()
    
    # Option 1: Async iteration for lazy loading
    async for user in users:
        print("user", user)
    
    # Option 2: Execute for template context
    return render_template(request=request, template_name="admin/users.html", context={
        "users": await users.execute(),  # Must execute for template
        "config": request.app.settings,
    })
```

**Note**: The same ORM methods work in both contexts! Cotlette automatically detects the mode based on database URL configuration.

---

## Lazy Loading and Iteration

Cotlette supports lazy loading and iteration over QuerySet objects in both synchronous and asynchronous modes.

### Synchronous Mode

```python
# Method 1: Execute to get list
users = UserModel.objects.all().execute()
for user in users:
    print(user.name)

# Method 2: Direct iteration (lazy loading)
users = UserModel.objects.all()
for user in users:
    print(user.name)

# Method 3: Indexing
first_user = UserModel.objects.all().get_item(0)
first_two = UserModel.objects.all().get_item(slice(0, 2))
```

### Asynchronous Mode

```python
# Method 1: Execute to get list
users = await UserModel.objects.all().execute()
for user in users:
    print(user.name)

# Method 2: Async iteration (lazy loading)
users = UserModel.objects.all()
async for user in users:
    print(user.name)

# Method 3: Indexing
first_user = await UserModel.objects.all().get_item(0)
first_two = await UserModel.objects.all().get_item(slice(0, 2))
```

### Template Usage

**Synchronous Mode:**
```python
@router.get("/users")
async def users_view(request: Request):
    users = UserModel.objects.all()
    return render_template(request=request, template_name="users.html", context={
        "users": users,  # Can be passed directly
    })
```

**Asynchronous Mode:**
```python
@router.get("/users")
async def users_view(request: Request):
    users = UserModel.objects.all()
    return render_template(request=request, template_name="users.html", context={
        "users": await users.execute(),  # Must execute for template
    })
```

### Important Notes

- In **synchronous mode**: Use regular `for` loops for iteration
- In **asynchronous mode**: Use `async for` loops for iteration
- The `execute()` method always returns a list that can be iterated normally
- Direct iteration provides lazy loading - data is fetched only when needed
- Indexing and slicing work in both modes with appropriate await calls
- For Jinja2 templates in async mode, use `await queryset.execute()` to get a regular list

---

## Advanced ORM Features

### Query Chaining
```python
# Complex queries with chaining (sync mode)
articles = Article.objects.filter(author_id=1).order_by('-id').execute()

# In async mode
articles = await Article.objects.filter(author_id=1).order_by('-id').execute()
```

### Iteration and Lazy Loading
```python
# Iterate over QuerySet results (sync mode)
for article in Article.objects.all().iter():
    print(article.title)

# Get specific items by index or slice (sync mode)
first_article = Article.objects.all().get_item(0)
recent_articles = Article.objects.all().get_item(slice(0, 10))

# In async mode
async for article in Article.objects.all().iter():
    print(article.title)

first_article = await Article.objects.all().get_item(0)
recent_articles = await Article.objects.all().get_item(slice(0, 10))
```

### Bulk Operations
```python
# Create multiple objects (sync mode)
articles = [
    Article(title="Article 1", content="Content 1", author_id=1),
    Article(title="Article 2", content="Content 2", author_id=1),
]

for article in articles:
    article.save()

# In async mode
for article in articles:
    await article.save()
```

### Database Support
Cotlette supports multiple databases through SQLAlchemy with both sync and async drivers:

```python
# SQLite (sync and async)
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'sqlite:///db.sqlite3',  # Sync mode
        # 'URL': 'sqlite+aiosqlite:///db.sqlite3',  # Async mode
    }
}

# PostgreSQL (sync and async)
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'postgresql://user:pass@localhost/dbname',  # Sync mode
        # 'URL': 'postgresql+asyncpg://user:pass@localhost/dbname',  # Async mode
    }
}

# MySQL (sync and async)
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'mysql://user:pass@localhost/dbname',  # Sync mode
        # 'URL': 'mysql+aiomysql://user:pass@localhost/dbname',  # Async mode
    }
}
```

### Async/Sync Mode Configuration
Cotlette determines the database mode (sync/async) based on the URL configuration in settings:

```python
# Synchronous mode (default)
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'sqlite:///db.sqlite3',  # Sync mode
    }
}

# Asynchronous mode
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'sqlite+aiosqlite:///db.sqlite3',  # Async mode
    }
}

# PostgreSQL examples
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'postgresql://user:pass@localhost/dbname',  # Sync mode
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'postgresql+asyncpg://user:pass@localhost/dbname',  # Async mode
    }
}

# MySQL examples
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'mysql://user:pass@localhost/dbname',  # Sync mode
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'mysql+aiomysql://user:pass@localhost/dbname',  # Async mode
    }
}
```

**Note**: The mode is determined by the presence of async drivers in the URL. No automatic conversion - you explicitly choose sync or async mode in your settings!

### Benefits of URL-based Mode Detection

- **Explicit Control**: You choose the mode explicitly in settings, not based on execution context
- **Predictable Behavior**: No dependency on whether you're in an async function or not
- **Framework Agnostic**: Works consistently with FastAPI, Django, Flask, or any other framework
- **Easy Switching**: Simply change the URL to switch between sync and async modes
- **Clear Intent**: The URL clearly shows whether you're using sync or async database drivers

### Supported Async Drivers

- **SQLite**: `sqlite+aiosqlite://` (requires `aiosqlite` package)
- **PostgreSQL**: `postgresql+asyncpg://` (requires `asyncpg` package)  
- **MySQL**: `mysql+aiomysql://` (requires `aiomysql` package)
- **MySQL**: `mysql+asyncmy://` (requires `asyncmy` package)

---

## Management Commands

### Project Management
- `cotlette startproject <project_name>` — Create a new Cotlette project directory structure
- `cotlette startapp <app_name>` — Create a new Cotlette app directory structure

### Development Server
- `cotlette runserver [addrport]` — Start the development server
  - Optional arguments: `--ipv6`, `--reload`
  - Example: `cotlette runserver 0.0.0.0:8000`

### Interactive Shell
- `cotlette shell` — Interactive Python shell with auto-imports
  - Options: `--no-startup`, `--no-imports`, `--interface`, `--command`
  - Supports IPython, bpython, and standard Python

### Database Management
- `cotlette makemigrations [--message] [--empty]` — Create database migrations
  - Options: `--message`, `--empty`
  - Example: `cotlette makemigrations --message "Add user model"`
- `cotlette migrate [--revision] [--fake]` — Apply database migrations
  - Options: `--revision`, `--fake`
  - Example: `cotlette migrate --revision head`

### User Management
- `cotlette createsuperuser` — Create a superuser account
  - Options: `--username`, `--email`, `--noinput`
  - Interactive mode for secure password input

---

## Documentation

- [Technical Documentation](.docs/index.md)
- [ORM Reference](.docs/orm.md)
- [Template Reference](.docs/templates.md)
- [Command Reference](.docs/commands.md)
- [Middleware Reference](.docs/middleware.md)
- [Extending Cotlette](.docs/extending.md)
- [FAQ](.docs/faq.md)

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Contributing

Pull requests and issues are welcome! See [GitHub](https://github.com/ForceFledgling/cotlette).
