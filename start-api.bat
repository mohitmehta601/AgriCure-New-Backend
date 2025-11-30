@echo off
REM AgriCure FastAPI Server Startup Script (Windows Batch)

echo ======================================================================
echo  AgriCure API Server Startup
echo ======================================================================

REM Activate conda environment if available
if exist "%CONDA_PREFIX%" (
    echo Using conda environment
)

REM Install dependencies
echo Installing dependencies...
python -m pip install --quiet fastapi uvicorn pydantic pandas scikit-learn xgboost joblib numpy python-multipart

REM Check if model files exist
if not exist "Soil Type Prediction\soil_model_xgb.pkl" (
    echo WARNING: Soil model not found!
    echo Please train the model first by running:
    echo   cd "Soil Type Prediction"
    echo   python train_soil_model.py
    pause
    exit /b 1
)

echo Model files found
echo.
echo ======================================================================
echo  Starting FastAPI Server...
echo ======================================================================
echo.
echo Server URL: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ======================================================================
echo.

REM Start the server
python run_server.py
pause

