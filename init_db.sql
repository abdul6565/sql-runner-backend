-- Create users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create recent_queries table for query history
CREATE TABLE IF NOT EXISTS recent_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL,
    query TEXT NOT NULL,
    result TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES users(username)
);

-- Sample data tables
CREATE TABLE IF NOT EXISTS Customers (
 customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
 first_name VARCHAR(100),
 last_name VARCHAR(100),
 age INTEGER,
 country VARCHAR(100)
);
INSERT OR IGNORE INTO Customers (first_name, last_name, age, country) VALUES
('John', 'Doe', 30, 'USA'),
('Robert', 'Luna', 22, 'USA'),
('David', 'Robinson', 25, 'UK'),
('John', 'Reinhardt', 22, 'UK'),
('Betty', 'Doe', 28, 'UAE');
CREATE TABLE IF NOT EXISTS Orders (
 order_id INTEGER PRIMARY KEY AUTOINCREMENT,
 item VARCHAR(100),
 amount INTEGER,
 customer_id INTEGER,
 FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);
INSERT OR IGNORE INTO Orders (item, amount, customer_id) VALUES
('Keyboard', 400, 4),
('Mouse', 300, 4),
('Monitor', 12000, 3),
('Keyboard', 400, 1),
('Mousepad', 250, 2);
CREATE TABLE IF NOT EXISTS Shippings (
 shipping_id INTEGER PRIMARY KEY AUTOINCREMENT,
 status VARCHAR(100),
 customer INTEGER
);
INSERT OR IGNORE INTO Shippings (status, customer) VALUES
('Pending', 2),
('Pending', 4),
('Delivered', 3),
('Pending', 5),
('Delivered', 1);
