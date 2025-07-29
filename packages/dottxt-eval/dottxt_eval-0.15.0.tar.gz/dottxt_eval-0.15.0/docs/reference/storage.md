# Storage Backends

Storage backends in doteval handle the persistence of evaluation sessions, results, and metadata. They provide a consistent interface for saving and loading evaluation data while supporting different storage mechanisms.

## Overview

Storage backends implement the `Storage` abstract base class and provide session persistence. The storage system is extensible, allowing you to implement custom backends for your specific needs.

## Built-in Storage Backends

### JSON Storage (Default)

The JSON storage backend stores each session as a separate JSON file in a directory.

```python
from doteval.storage import JSONStorage

# Create JSON storage in default location
storage = JSONStorage("evals")

# Custom path
storage = JSONStorage("/path/to/my/evaluations")
```

**Directory Structure:**
```
evals/
├── gsm8k_baseline.json      # Session data
├── gsm8k_baseline.lock      # Lock file (if running)
├── sentiment_eval.json
└── math_reasoning.json
```

**Features:**
- Human-readable JSON format
- File-based locking
- Automatic directory creation
- Cross-platform compatibility

**Usage via URL:**
```bash
# Default JSON storage
doteval list --storage "json://evals"

# Custom path
doteval list --storage "json:///absolute/path/to/storage"

# Relative path
doteval list --storage "json://relative/path"
```

### SQLite Storage

The SQLite storage backend stores evaluation data in a relational database, enabling powerful querying capabilities.

```python
from doteval.storage import SQLiteStorage

# Create SQLite storage
storage = SQLiteStorage("evaluations.db")

# Custom path
storage = SQLiteStorage("/path/to/my/database.db")
```

**Features:**
- Efficient storage for large datasets
- Query capabilities for error analysis
- ACID transactions
- Built-in support for finding failed evaluations

**Additional Methods:**
```python
# Find all failed evaluations
failed_results = storage.get_failed_results("session_name")

# Find evaluations that encountered errors
error_results = storage.get_error_results("session_name")
```

**Usage via URL:**
```bash
# SQLite storage
doteval list --storage "sqlite://evaluations.db"

# Custom path
doteval list --storage "sqlite:///absolute/path/to/database.db"
```

## Custom Storage Backends

You can implement your own storage backend by inheriting from the `Storage` abstract base class and registering it.

### Available Functions

The `doteval.storage` module provides:

- `Storage` - Abstract base class for implementing backends
- `register(name, storage_class)` - Register a custom backend
- `list_backends()` - List all registered backend names
- `get_storage(path)` - Get a storage instance from a path

### Implementing a Custom Backend

```python
from doteval.storage import Storage, register
from typing import Optional

class RedisStorage(Storage):
    """Example Redis storage backend."""

    def __init__(self, connection_string: str):
        # Parse connection string and connect to Redis
        self.redis_client = connect_to_redis(connection_string)

    def save(self, session: Session):
        # Serialize and save session to Redis
        data = serialize_session(session)
        self.redis_client.set(f"session:{session.name}", data)

    def load(self, name: str) -> Optional[Session]:
        # Load and deserialize session from Redis
        data = self.redis_client.get(f"session:{name}")
        if data:
            return deserialize_session(data)
        return None

    def list_names(self) -> list[str]:
        # List all session names
        keys = self.redis_client.keys("session:*")
        return [key.decode().replace("session:", "") for key in keys]

    def rename(self, old_name: str, new_name: str):
        # Rename a session
        self.redis_client.rename(f"session:{old_name}", f"session:{new_name}")

    def delete(self, name: str):
        # Delete a session
        if not self.redis_client.delete(f"session:{name}"):
            raise ValueError(f"{name}: session not found.")

    def acquire_lock(self, name: str):
        # Acquire a lock for interrupted session detection
        if not self.redis_client.setnx(f"lock:{name}", "1"):
            raise RuntimeError(f"Session '{name}' is already locked.")

    def release_lock(self, name: str):
        # Release the lock
        self.redis_client.delete(f"lock:{name}")

    def is_locked(self, name: str) -> bool:
        # Check if session is locked
        return bool(self.redis_client.exists(f"lock:{name}"))

# Register the backend
register("redis", RedisStorage)
```

### Using Your Custom Backend

Once registered, you can use your backend just like the built-in ones:

```python
# In your code
from my_redis_storage import RedisStorage  # This triggers registration

# Use with SessionManager
from doteval.sessions import SessionManager

manager = SessionManager(storage_path="redis://localhost:6379/0")
```

```bash
# From command line
pytest eval_test.py --session my_eval --storage redis://localhost:6379/0
```

### Packaging Custom Backends

You can distribute your storage backend as a separate package:

```python
# my_storage_package/__init__.py
from doteval.storage import Storage, register

class MyCustomStorage(Storage):
    # Implementation...
    pass

# Auto-register on import
register("mybackend", MyCustomStorage)
```

Users can then install and use your backend:

```bash
pip install my-storage-package
pytest eval_test.py --storage mybackend://config
```

## Error Handling

The storage system provides helpful error messages for common configuration issues:

### Invalid Storage Paths

```bash
# Unknown backend
$ doteval list --storage "postgres://localhost"
Error: Unknown storage backend: postgres

# List available backends
$ python -c "from doteval.storage import list_backends; print(list_backends())"
['json', 'sqlite']
```

### Permission Issues

```bash
# No write permissions
$ doteval list --storage "json:///root/restricted"
Error: Permission denied: Cannot write to '/root/restricted'
```

### Storage Recovery

If storage files become corrupted or inaccessible:

```python
from doteval.storage import JSONStorage

storage = JSONStorage("evals")

# Check if session exists
if storage.exists("my_session"):
    try:
        session = storage.load("my_session")
    except Exception as e:
        print(f"Session corrupted: {e}")
        # Session file may need manual recovery
```
