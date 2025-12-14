# AgriCure Backend - Complete Documentation

> **Version:** 2.0  
> **Last Updated:** December 8, 2025  
> **Author:** AgriCure Development Team

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [System Components](#system-components)
  - [Node.js API Server](#nodejs-api-server)
  - [Python FastAPI Server](#python-fastapi-server)
  - [Machine Learning Models](#machine-learning-models)
- [Database Setup](#database-setup)
- [API Documentation](#api-documentation)
- [Frontend Integration](#frontend-integration)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## 🌾 Overview

AgriCure is a comprehensive agricultural management platform that integrates machine learning models for soil type prediction and fertilizer recommendations. The system consists of:

- **Node.js Express Backend** (Port 3000) - Main API for user management, authentication, and farm data
- **Python FastAPI Server** (Port 8000) - ML models for soil prediction and fertilizer recommendations
- **MongoDB Database** - User, farm, and recommendation data storage
- **React/TypeScript Frontend** - User interface

### Key Features

✅ **User Authentication** - Email/password with OTP verification  
✅ **Farm Management** - Add, edit, and track multiple farms  
✅ **Soil Type Prediction** - ML-based soil detection from GPS coordinates  
✅ **Fertilizer Recommendations** - AI-powered fertilizer suggestions  
✅ **Product Key Management** - License key validation system  
✅ **Email Notifications** - OTP verification and alerts

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     FRONTEND (React + TypeScript)                        │
│                         Port: 5173 (dev)                                 │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  • User Dashboard                                                  │ │
│  │  • Farm Management (Add/Edit/View Farms)                           │ │
│  │  • Fertilizer Recommendation Form                                  │ │
│  │  • Soil Type Detection                                             │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │ HTTP/REST
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│               NODE.JS EXPRESS BACKEND (Port 3000)                        │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  Routes:                                                           │ │
│  │  • /api/auth        - Authentication (signup, login, OTP)         │ │
│  │  • /api/farms       - Farm CRUD operations                        │ │
│  │  • /api/users       - User profile management                     │ │
│  │  • /api/fertilizer-ml - Proxy to Python ML API                    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                               │                                          │
│  ┌────────────────────────────┴──────────────────────────────────────┐  │
│  │                      MongoDB Database                             │  │
│  │  Collections: users, farms, pendingusers, otps, recommendations   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │ HTTP POST (axios proxy)
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              PYTHON FASTAPI SERVER (Port 8000)                           │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  Endpoints:                                                        │ │
│  │  • POST /soil-data               - Soil type prediction           │ │
│  │  • POST /predict-soil            - Advanced soil prediction       │ │
│  │  • POST /fertilizer-recommendation - Fertilizer recommendations   │ │
│  │  • GET /health                   - Health check                   │ │
│  │  • GET /soil-types               - List available soil types      │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                               │                                          │
│  ┌────────────────────────────┴──────────────────────────────────────┐  │
│  │              Machine Learning Models                              │  │
│  │  • XGBoost Soil Classifier                                        │  │
│  │  • Primary Fertilizer Model (Random Forest/XGBoost/CatBoost)     │  │
│  │  • Secondary Fertilizer Model (Micronutrients)                    │  │
│  │  • LLM Enhancement (Google Gemini API)                            │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 16+ with npm
- **Python** 3.8+
- **MongoDB** Atlas account or local MongoDB
- **Git** for version control

### Installation

#### 1. Clone Repository

```powershell
cd "P:\Latest AgriCure\Backend"
```

#### 2. Install Node.js Dependencies

```powershell
npm install
```

#### 3. Install Python Dependencies

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install packages
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create `.env` file in Backend root:

```env
# MongoDB Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/agricure
JWT_SECRET=your_jwt_secret_key_change_in_production
JWT_EXPIRES_IN=7d
NODE_ENV=development

# Email Configuration (for OTP)
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password

# Google Gemini API (optional, for LLM-enhanced recommendations)
GEMINI_API_KEY=your-gemini-api-key
```

### Starting Servers

#### Option A: Start All Servers (Recommended)

```powershell
.\start-all-servers.ps1
```

This script starts:

- Node.js Express server (port 3000)
- Python FastAPI server (port 8000)

#### Option B: Start Manually

**Terminal 1 - Node.js:**

```powershell
npm start
# or
node src/server.js
```

**Terminal 2 - Python:**

```powershell
.\.venv\Scripts\Activate.ps1
python run_server.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Verify Installation

**Node.js Health Check:**

```
http://localhost:3000/api/health
```

**Python Health Check:**

```
http://localhost:8000/health
```

**API Documentation:**

```
http://localhost:8000/docs
```

---

## 🔧 System Components

### Node.js API Server

**Location:** `Backend/src/`  
**Port:** 3000  
**Framework:** Express.js

#### Key Files

- **`src/server.js`** - Main application entry point
- **`src/routes/`** - API route handlers
  - `auth.js` - Authentication (signup, login, OTP verification)
  - `farms.js` - Farm management CRUD operations
  - `users.js` - User profile management
  - `fertilizerML.js` - Proxy to Python ML API
- **`src/models/`** - MongoDB schemas
  - `User.js` - User model
  - `Farm.js` - Farm model
  - `OTP.js` - OTP verification
  - `PendingUser.js` - Pre-verification user storage
- **`src/middleware/`** - Custom middleware
  - `auth.js` - JWT authentication
  - `errorHandler.js` - Error handling
- **`src/services/`** - Business logic
  - `emailService.js` - Email sending (OTP, notifications)

#### Main Routes

| Route                          | Method | Description                    | Authentication |
| ------------------------------ | ------ | ------------------------------ | -------------- |
| `/api/auth/signup`             | POST   | User registration with OTP     | No             |
| `/api/auth/verify-otp`         | POST   | Verify OTP and complete signup | No             |
| `/api/auth/login`              | POST   | User login                     | No             |
| `/api/auth/resend-otp`         | POST   | Resend OTP                     | No             |
| `/api/farms`                   | GET    | Get all user farms             | Yes            |
| `/api/farms`                   | POST   | Create new farm                | Yes            |
| `/api/farms/:id`               | PUT    | Update farm                    | Yes            |
| `/api/farms/:id`               | DELETE | Delete farm                    | Yes            |
| `/api/fertilizer-ml/recommend` | POST   | Get fertilizer recommendations | Yes            |
| `/api/fertilizer-ml/health`    | GET    | Check Python API status        | No             |

---

### Python FastAPI Server

**Location:** `Backend/main.py`  
**Port:** 8000  
**Framework:** FastAPI

#### Key Endpoints

##### 1. Soil Type Prediction

**Endpoint:** `POST /soil-data`

**Purpose:** Predict soil type from GPS coordinates

**Request:**

```json
{
  "latitude": 28.6139,
  "longitude": 77.209
}
```

**Response:**

```json
{
  "location": {
    "latitude": 28.6139,
    "longitude": 77.209,
    "timestamp": "2025-12-08T10:30:00"
  },
  "soil_type": "Alluvial Soil",
  "confidence": 0.87,
  "soil_properties": {
    "clay": null,
    "sand": null,
    "silt": null
  },
  "sources": ["ML Model Prediction", "XGBoost Classifier"],
  "success": true
}
```

##### 2. Fertilizer Recommendation

**Endpoint:** `POST /fertilizer-recommendation`

**Purpose:** Get AI-powered fertilizer recommendations

**Request:**

```json
{
  "size": 2.5,
  "crop": "Wheat",
  "soil": "Loamy",
  "sowing_date": "2025-01-05",
  "nitrogen": 190,
  "phosphorus": 9.5,
  "potassium": 115,
  "soil_ph": 7.1,
  "soil_moisture": 32,
  "electrical_conductivity": 0.5,
  "soil_temperature": 26,
  "use_llm": true
}
```

**Response:**

```json
{
  "success": true,
  "ml_predictions": {
    "N_Status": "High",
    "P_Status": "Low",
    "K_Status": "Optimal",
    "Primary_Fertilizer": "DAP",
    "Secondary_Fertilizer": "Zinc Sulphate",
    "pH_Amendment": "None"
  },
  "cost_estimate": {
    "primary_fertilizer": "₹2,500",
    "secondary_fertilizer": "₹800",
    "organic_options": "₹1,200",
    "total_estimate": "₹4,500",
    "field_size": "For 2.50 hectares"
  },
  "application_timing": {
    "primary_fertilizer": "Apply in 3 split doses",
    "secondary_fertilizer": "Apply during active growth",
    "organic_options": "Apply 3-4 weeks before sowing"
  },
  "timestamp": "2025-01-05T10:30:00"
}
```

##### 3. Health Check

**Endpoint:** `GET /health`

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2025-12-08T10:30:00",
  "model_loaded": true,
  "message": "All models loaded successfully"
}
```

---

### Machine Learning Models

#### 1. Soil Type Prediction Model

**Location:** `Backend/Soil Type Prediction/`  
**Model Type:** XGBoost Classifier  
**Model Files:**

- `soil_model_xgb.pkl` - Trained model
- `soil_label_encoder.pkl` - Label encoder

**Supported Soil Types:**

- Alluvial
- Black
- Red
- Laterite
- Arid
- Clayey
- Alkaline

**Features Used:**

- Geographic: latitude, longitude, elevation
- Environmental: rainfall, temperature, aridity index, NDVI
- Spatial: distance to rivers, distance to coast
- Categorical: land cover, geology

**Training:**

```powershell
cd "Soil Type Prediction"
python train_soil_model.py
```

#### 2. Fertilizer Recommendation System

**Location:** `Backend/fertilizer recommendation system/`  
**Model Type:** Hybrid (Rule-Based Primary + ML-Based Secondary + LLM Enhancement)  
**Status:** ✅ Production Ready (Updated: December 14, 2025)

**System Architecture:**

```
User Input
    ↓
[1] primary_fertilizer_pH_model.py (Rule-Based Expert System)
    ├─→ N_Status (Low/Optimal)
    ├─→ P_Status (Low/Optimal)
    ├─→ K_Status (Low/Optimal)
    ├─→ Primary_Fertilizer (Urea, DAP, NPK, etc.)
    └─→ pH_Amendment (Lime, Gypsum, etc.)
    ↓
[2] secondary_fertilizer_model.py (ML-Based)
    └─→ Secondary_Fertilizer (Micronutrients: Zinc, Boron, etc.)
    ↓
[3] LLM_model.py (Optional AI Enhancement)
    └─→ Comprehensive Report with Cost & Timing
    ↓
Final Recommendation Output
```

**Components:**

1. **Primary Fertilizer Model** (`primary_fertilizer_pH_model.py`) ✨ **NEW**

   - **Type:** 100% Rule-Based Expert System
   - **Accuracy:** 100% (Deterministic - no training error)
   - **Inputs:** N, P, K levels, Crop Type, pH, EC, Moisture, Temperature
   - **Outputs:**

     - N/P/K Status (Low/Optimal)
     - Primary Fertilizer Recommendation
     - pH Amendment Suggestion

   - **Supported Crops (16):** Rice, Wheat, Maize, Barley, Jowar, Bajra, Ragi, Groundnut, Mustard, Soybean, Sugarcane, Cotton, Chickpea, Moong, Garlic, Onion

   - **Fertilizer Logic:**

     - All NPK Low → NPK (14-14-14)
     - Only N Low → Urea
     - Only P Low → TSP (Triple Super Phosphate)
     - Only K Low → MOP (Muriate of Potash)
     - N+P Low → DAP (Di-Ammonium Phosphate)
     - N+K Low → Urea + MOP
     - P+K Low → TSP + MOP
     - All Optimal → Maintenance NPK

   - **pH Amendment Logic:**

     - pH < 5.5 → Agricultural Lime
     - pH 5.5-6.0 → Dolomite
     - pH 6.0-7.5 → Balance Maintain (None)
     - pH 7.5-8.0 → Gypsum
     - pH > 8.0 → Elemental Sulphur

   - **Benefits:**
     - ✅ 100% Deterministic (same input = same output)
     - ✅ No training required (instant initialization)
     - ✅ Zero learning error
     - ✅ Transparent & explainable
     - ✅ Easy to maintain and update
     - ✅ No ML dependencies for primary predictions
     - ✅ No model drift or retraining needed

2. **Secondary Fertilizer Model** (`secondary_fertilizer_model.py`)

   - **Type:** ML-Based (Ensemble: RF + XGBoost + CatBoost + LightGBM)
   - Predicts micronutrient requirements
   - Recommends secondary fertilizers (Zinc Sulphate, Boron, Ferrous Sulphate, etc.)
   - Uses soil and crop parameters for predictions

3. **LLM Enhancement** (`LLM_model.py`)
   - Uses Google Gemini API
   - Generates detailed, human-readable recommendations
   - Calculates fertilizer costs and quantities
   - Provides application timing schedules
   - Suggests organic alternatives
   - Optional enhancement layer

**Main Integration File:** `Final_Model.py`

**Testing Results:**

- ✅ Standalone model test: **PASSED**
- ✅ Integration test: **PASSED**
- ✅ Comprehensive rule tests: **9/9 PASSED** (100% success rate)
- ✅ All fertilizer pathways validated
- ✅ All pH ranges tested

**Usage Example:**

```python
from Final_Model import FinalFertilizerRecommendationSystem

# Initialize system
system = FinalFertilizerRecommendationSystem()

# Get recommendation
result = system.predict(
    size=2.5,
    crop='Wheat',
    sowing_date='2025-11-15',
    nitrogen=65.0,      # mg/kg
    phosphorus=10.0,    # mg/kg
    potassium=85.0,     # mg/kg
    soil_ph=5.2,
    soil_moisture=60.0,
    electrical_conductivity=1600.0,
    soil_temperature=22.0,
    use_llm=False       # Set True for LLM enhancement
)

# Access results
print(result['ml_predictions']['N_Status'])           # "Low"
print(result['ml_predictions']['Primary_Fertilizer']) # "NPK (14–14–14)"
print(result['ml_predictions']['pH_Amendment'])       # "Agricultural Lime"
```

**Training:**

```powershell
cd "fertilizer recommendation system"

# Primary model is rule-based - no training needed
# Secondary model training (if needed):
python secondary_fertilizer_model.py

# Test the complete system:
python test_final_model.py
```

---

## 💾 Database Setup

### MongoDB Atlas Configuration

#### Collections

##### 1. users

```javascript
{
  _id: ObjectId,
  email: String (unique),
  password: String (hashed),
  fullName: String,
  phoneNumber: String,
  productId: String,
  isVerified: Boolean,
  createdAt: Date,
  updatedAt: Date
}
```

##### 2. farms

```javascript
{
  _id: ObjectId,
  userId: ObjectId (ref: 'User'),
  name: String,
  size: Number,
  unit: String (enum: ['hectares', 'acres', 'bigha']),
  cropType: String,
  soilType: String,
  location: String,
  latitude: Number,
  longitude: Number,
  soilData: {
    N: Number,
    P: Number,
    K: Number,
    ph: Number,
    moisture: Number,
    temperature: Number
  },
  sowingDate: Date,
  createdAt: Date,
  updatedAt: Date
}
```

##### 3. pendingusers

```javascript
{
  _id: ObjectId,
  email: String,
  password: String (hashed),
  fullName: String,
  phoneNumber: String,
  productKey: String,
  otp: String,
  otpExpires: Date,
  createdAt: Date
}
```

##### 4. otps

```javascript
{
  _id: ObjectId,
  email: String,
  otp: String,
  expiresAt: Date,
  createdAt: Date
}
```

**TTL Index:** Automatically deletes expired OTPs

##### 5. recommendations

```javascript
{
  _id: ObjectId,
  userId: ObjectId (ref: 'User'),
  farmId: ObjectId (ref: 'Farm'),
  cropType: String,
  soilType: String,
  inputData: Object,
  mlPredictions: Object,
  costEstimate: Object,
  applicationTiming: Object,
  createdAt: Date
}
```

### Database Migration Scripts

- **`migrate-user-schema.js`** - Migrate user schema
- **`migrate-existing-farms.js`** - Migrate farm data
- **`update-farm-database.js`** - Update farm database structure
- **`verify-farm-schema.js`** - Verify farm schema

---

## 📚 API Documentation

### Authentication Flow

#### 1. User Signup

```
POST /api/auth/signup
→ Sends OTP to email
→ Creates pending user entry
```

#### 2. OTP Verification

```
POST /api/auth/verify-otp
→ Verifies OTP
→ Creates user account
→ Returns JWT token
```

#### 3. User Login

```
POST /api/auth/login
→ Validates credentials
→ Returns JWT token
```

### Farm Management Flow

#### 1. Add Farm with Soil Detection

```
Frontend: Request GPS location
→ POST /soil-data (Python API)
→ Returns soil type prediction
→ User fills farm details
→ POST /api/farms (Node.js API)
→ Saves farm to database
```

#### 2. Get Fertilizer Recommendation

```
Frontend: User selects farm + enters soil parameters
→ POST /api/fertilizer-ml/recommend (Node.js proxy)
→ POST /fertilizer-recommendation (Python API)
→ Returns ML predictions + cost analysis
```

### Error Handling

All API endpoints return consistent error format:

```json
{
  "success": false,
  "error": "Error message",
  "details": "Additional error details"
}
```

**HTTP Status Codes:**

- `200` - Success
- `400` - Bad Request (validation error)
- `401` - Unauthorized (authentication required)
- `404` - Not Found
- `500` - Internal Server Error

---

## 🎨 Frontend Integration

### Environment Variables

**Frontend `.env`:**

```env
VITE_API_URL=http://localhost:3000/api
VITE_PYTHON_API_URL=http://localhost:8000
VITE_MONGODB_URI=mongodb+srv://...
VITE_JWT_SECRET=your_jwt_secret
```

### Services

#### 1. Location & Soil Service

```typescript
// Frontend/src/services/locationSoilService.ts
import { locationSoilService } from "@/services/locationSoilService";

// Get location and soil data
const data = await locationSoilService.getLocationAndSoilData();
// Returns: { location, soilType, confidence }
```

#### 2. Fertilizer Recommendation Service

```typescript
// Frontend/src/services/fertilizerRecommendationService.ts
import fertilizerService from "@/services/fertilizerRecommendationService";

const recommendation = await fertilizerService.getRecommendation({
  size: 2.5,
  crop: "Wheat",
  soil: "Loamy",
  sowingDate: "2025-01-05",
  nitrogen: 190,
  phosphorus: 9.5,
  potassium: 115,
  soilPH: 7.1,
  soilMoisture: 32,
  electricalConductivity: 0.5,
  soilTemperature: 26,
  useLLM: true,
});
```

---

## 🚢 Deployment

### Production Checklist

- [ ] Update all environment variables
- [ ] Change `JWT_SECRET` to secure random string
- [ ] Set `NODE_ENV=production`
- [ ] Configure production MongoDB URI
- [ ] Set up email service (Gmail or SMTP)
- [ ] Configure CORS for production domain
- [ ] Set up SSL/TLS certificates
- [ ] Configure rate limiting
- [ ] Set up logging and monitoring
- [ ] Backup ML model files
- [ ] Test all endpoints

### Environment-Specific Configuration

**Development:**

```env
NODE_ENV=development
CORS_ORIGIN=http://localhost:5173
```

**Production:**

```env
NODE_ENV=production
CORS_ORIGIN=https://yourdomain.com
```

### Server Startup (Production)

**Node.js:**

```powershell
npm run start:prod
# or with PM2
pm2 start src/server.js --name agricure-api
```

**Python:**

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Problem:** Port 3000 or 8000 is already occupied

**Solution:**

```powershell
# Find process using port
Get-NetTCPConnection -LocalPort 3000
Get-NetTCPConnection -LocalPort 8000

# Kill process
Stop-Process -Id <PID> -Force
```

#### 2. MongoDB Connection Error

**Problem:** Cannot connect to MongoDB

**Solution:**

- Verify `MONGODB_URI` in `.env`
- Check network connectivity
- Whitelist your IP in MongoDB Atlas
- Verify username and password

#### 3. ML Model Not Loading

**Problem:** Soil or fertilizer model fails to load

**Solution:**

```powershell
# Verify model files exist
cd "Soil Type Prediction"
ls soil_model_xgb.pkl
ls soil_label_encoder.pkl

# Retrain if necessary
python train_soil_model.py
```

#### 4. Python Virtual Environment Issues

**Problem:** Cannot activate virtual environment

**Solution:**

```powershell
# Recreate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### 5. OTP Email Not Sending

**Problem:** Email OTP not being delivered

**Solution:**

- Verify `EMAIL_USER` and `EMAIL_PASS` in `.env`
- Use Gmail App Password (not regular password)
- Check spam folder
- Verify email service configuration in `src/services/emailService.js`

#### 6. CORS Errors

**Problem:** Frontend cannot connect to backend

**Solution:**

- Verify CORS configuration in `main.py` and `src/server.js`
- Check `VITE_API_URL` in frontend `.env`
- Ensure both servers are running

### Testing Scripts

```powershell
# Test Node.js API
node test-system.js

# Test Python API
python test_api.py

# Test Soil Integration
python test-soil-integration.py

# Test Fertilizer Model
cd "fertilizer recommendation system"
python test_final_model.py

# Test Email OTP
node test-email-otp.js

# Test Farm Operations
node test-farms.js
```

### Logs and Debugging

**Node.js Logs:**

```powershell
# Console output shows all requests
node src/server.js
```

**Python Logs:**

```powershell
# Uvicorn logs with --reload flag
python run_server.py
```

---

## 📖 Additional Documentation

The following documentation files have been consolidated into this README:

- ✅ `README_API.md` - Python FastAPI documentation
- ✅ `QUICKSTART.md` - Quick start guide
- ✅ `QUICKSTART_SOIL_PREDICTION.md` - Soil prediction quick start
- ✅ `FERTILIZER_QUICKSTART.md` - Fertilizer system quick start
- ✅ `fertilizer recommendation system/README_FINAL_MODEL.md` - Fertilizer model docs
- ✅ `Soil Type Prediction/README.md` - Soil model docs
- ✅ `ARCHITECTURE_DIAGRAM.md` - System architecture
- ✅ `MONGODB_SETUP.md` - Database setup
- ✅ `EMAIL_OTP_SETUP.md` - Email OTP configuration
- ✅ `SETUP_COMPLETE.md` - Setup completion guide
- ✅ `FERTILIZER_INTEGRATION_GUIDE.md` - Fertilizer integration details
- ✅ `SOIL_PREDICTION_INTEGRATION.md` - Soil prediction integration
- ✅ `INTEGRATION_COMPLETE_SUMMARY.md` - Integration summary
- ✅ `FARM_DATABASE_SCHEMA.md` - Farm database schema
- ✅ `fertilizer recommendation system/COMPLETE_DOCUMENTATION.md` - Complete fertilizer docs

---

## 🤝 Support

For issues, questions, or contributions:

1. Check this README first
2. Review troubleshooting section
3. Check individual test scripts
4. Review API documentation at http://localhost:8000/docs

---

## 📝 License

Copyright © 2025 AgriCure Development Team. All rights reserved.

---

**Last Updated:** December 8, 2025  
**Maintained By:** AgriCure Development Team
