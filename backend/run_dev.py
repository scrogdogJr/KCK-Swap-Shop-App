"""
Development server runner with automatic database setup
Run with: python run_dev.py
"""
import subprocess
import sys
from pathlib import Path

def main():
    # Check if database needs seeding
    db_file = Path("app.db")
    
    if not db_file.exists():
        print("🔧 First run detected. Setting up database...")
        subprocess.run([sys.executable, "seed_database.py"])
        print()
    
    # Start uvicorn server
    print("🚀 Starting development server...")
    print("📖 API docs: http://localhost:8000/docs")
    print("🔍 Interactive docs: http://localhost:8000/redoc")
    print("Press Ctrl+C to stop\n")
    
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ])

if __name__ == "__main__":
    main()
