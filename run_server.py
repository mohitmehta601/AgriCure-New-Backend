"""
Simple script to run the FastAPI server
"""
import os
import uvicorn

# Set NumExpr to use all available CPU cores
os.environ['NUMEXPR_MAX_THREADS'] = '16'

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("AgriCure API Server")
    print("=" * 70)
    print("Server URL: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("ReDoc: http://localhost:8000/redoc")
    print("=" * 70 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
