from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, queries, tables
from config import settings
import sqlite3
import os
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup if it doesn't exist."""
    db_path = settings.database_url
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_login DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recent_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL,
            query TEXT NOT NULL,
            result TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Customers (
         customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
         first_name VARCHAR(100),
         last_name VARCHAR(100),
         age INTEGER,
         country VARCHAR(100)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
         order_id INTEGER PRIMARY KEY AUTOINCREMENT,
         item VARCHAR(100),
         amount INTEGER,
         customer_id INTEGER,
         FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Shippings (
         shipping_id INTEGER PRIMARY KEY AUTOINCREMENT,
         status VARCHAR(100),
         customer INTEGER
        );
        """)

        # Insert sample data
        cursor.executemany("INSERT INTO Customers (first_name, last_name, age, country) VALUES (?, ?, ?, ?)", [
            ('John', 'Doe', 30, 'USA'),
            ('Robert', 'Luna', 22, 'USA'),
            ('David', 'Robinson', 25, 'UK'),
            ('John', 'Reinhardt', 22, 'UK'),
            ('Betty', 'Doe', 28, 'UAE')
        ])

        cursor.executemany("INSERT INTO Orders (item, amount, customer_id) VALUES (?, ?, ?)", [
            ('Keyboard', 400, 4),
            ('Mouse', 300, 4),
            ('Monitor', 12000, 3),
            ('Keyboard', 400, 1),
            ('Mousepad', 250, 2)
        ])

        cursor.executemany("INSERT INTO Shippings (status, customer) VALUES (?, ?)", [
            ('Pending', 2),
            ('Pending', 4),
            ('Delivered', 3),
            ('Pending', 5),
            ('Delivered', 1)
        ])

        conn.commit()
        conn.close()
    yield

# Create FastAPI app
app = FastAPI(
    title="SQL Runner API",
    description="A secure SQL query execution API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001", "*"],  # Frontend URLs, allow all for Railway
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(queries.router, prefix="/api/v1", tags=["Queries"])
app.include_router(tables.router, prefix="/api/v1", tags=["Tables"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "SQL Runner Backend API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": "2024-01-01T00:00:00Z"  # Would use datetime.utcnow() in real app
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
