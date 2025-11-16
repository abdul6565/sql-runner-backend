# This file is deprecated. The application has been refactored.
# Please use app.py as the main entry point.
# To run the application: python app.py

from app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
