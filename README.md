# SQL Runner Backend

FastAPI backend for SQL Runner application with JWT authentication and SQLite database.

## Features

- JWT Authentication
- SQL Query Execution
- User Management
- Recent Queries Tracking
- Table Schema Information

## Deployment

### Railway

1. Connect this repository to Railway
2. Railway will automatically detect Python and install dependencies
3. The app will start using the command in `railway.json`

### Local Development

```bash
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /` - Health check
- `POST /register` - Register user
- `POST /token` - Login
- `POST /query` - Execute SQL query
- `GET /tables` - Get table list
- `POST /table_info` - Get table schema
- `GET /recent_queries` - Get user's recent queries
- `GET /profile` - Get user profile
- `POST /forgot_password` - Reset password

## Environment Variables

- `PORT` - Server port (default: 8000)

## Database

SQLite database with sample data (Customers, Orders, Shippings tables) is automatically initialized on first run.