const express = require('express');
const axios = require('axios');
const router = express.Router();

// Python API URL - should be configurable via environment variable
const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:8000';

/**
 * POST /api/fertilizer-ml/recommend
 * Get fertilizer recommendations from Python ML model
 */
router.post('/recommend', async (req, res) => {
  try {
    const {
      size,
      crop,
      soil,
      sowing_date,
      nitrogen,
      phosphorus,
      potassium,
      soil_ph,
      soil_moisture,
      electrical_conductivity,
      soil_temperature,
      use_llm = false
    } = req.body;

    // Validate required fields
    if (!size || !crop || !soil || !sowing_date || 
        nitrogen === undefined || phosphorus === undefined || 
        potassium === undefined || soil_ph === undefined ||
        soil_moisture === undefined || electrical_conductivity === undefined ||
        soil_temperature === undefined) {
      return res.status(400).json({
        success: false,
        message: 'Missing required fields'
      });
    }

    // Call Python API
    const response = await axios.post(
      `${PYTHON_API_URL}/fertilizer-recommendation`,
      {
        size: parseFloat(size),
        crop,
        soil,
        sowing_date,
        nitrogen: parseFloat(nitrogen),
        phosphorus: parseFloat(phosphorus),
        potassium: parseFloat(potassium),
        soil_ph: parseFloat(soil_ph),
        soil_moisture: parseFloat(soil_moisture),
        electrical_conductivity: parseFloat(electrical_conductivity),
        soil_temperature: parseFloat(soil_temperature),
        use_llm
      },
      {
        timeout: 30000, // 30 second timeout
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );

    res.json(response.data);

  } catch (error) {
    console.error('Error calling Python ML API:', error.message);
    
    if (error.response) {
      // Python API returned an error
      res.status(error.response.status).json({
        success: false,
        message: error.response.data.detail || 'ML model error',
        error: error.response.data
      });
    } else if (error.request) {
      // No response from Python API
      res.status(503).json({
        success: false,
        message: 'Python ML API is not available. Please ensure the Python server is running.',
        error: error.message
      });
    } else {
      // Other errors
      res.status(500).json({
        success: false,
        message: 'Internal server error',
        error: error.message
      });
    }
  }
});

/**
 * POST /api/fertilizer-ml/recommend-enhanced
 * Get LLM-enhanced fertilizer recommendations
 */
router.post('/recommend-enhanced', async (req, res) => {
  try {
    const requestData = {
      ...req.body,
      use_llm: true // Force LLM usage
    };

    const response = await axios.post(
      `${PYTHON_API_URL}/fertilizer-recommendation`,
      requestData,
      {
        timeout: 60000, // 60 second timeout for LLM
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );

    res.json(response.data);

  } catch (error) {
    console.error('Error calling Python LLM API:', error.message);
    
    if (error.response) {
      res.status(error.response.status).json({
        success: false,
        message: error.response.data.detail || 'LLM model error',
        error: error.response.data
      });
    } else if (error.request) {
      res.status(503).json({
        success: false,
        message: 'Python ML API is not available',
        error: error.message
      });
    } else {
      res.status(500).json({
        success: false,
        message: 'Internal server error',
        error: error.message
      });
    }
  }
});

/**
 * GET /api/fertilizer-ml/health
 * Check Python ML API health
 */
router.get('/health', async (req, res) => {
  try {
    const response = await axios.get(`${PYTHON_API_URL}/health`, {
      timeout: 5000
    });
    
    res.json({
      success: true,
      python_api: response.data,
      endpoint: PYTHON_API_URL
    });
  } catch (error) {
    res.status(503).json({
      success: false,
      message: 'Python ML API is not available',
      endpoint: PYTHON_API_URL,
      error: error.message
    });
  }
});

/**
 * GET /api/fertilizer-ml/model-info
 * Get ML model information
 */
router.get('/model-info', async (req, res) => {
  try {
    const response = await axios.get(`${PYTHON_API_URL}/api-info`, {
      timeout: 5000
    });
    
    res.json(response.data);
  } catch (error) {
    res.status(503).json({
      success: false,
      message: 'Unable to fetch model info',
      error: error.message
    });
  }
});

module.exports = router;
