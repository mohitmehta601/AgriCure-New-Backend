const express = require('express');
const ProductKey = require('../models/ProductKey');
const auth = require('../middleware/auth');
const router = express.Router();

// Get all product keys (admin only)
router.get('/', auth, async (req, res) => {
  try {
    const productKeys = await ProductKey.find({})
      .populate('usedBy', 'email fullName')
      .sort({ createdAt: -1 });
    
    res.json(productKeys);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Get product key status
router.get('/status/:key', async (req, res) => {
  try {
    const productKey = await ProductKey.findOne({ key: req.params.key });
    
    if (!productKey) {
      return res.status(404).json({ message: 'Product key not found' });
    }
    
    res.json({
      key: productKey.key,
      productName: productKey.productName,
      isActive: productKey.isActive,
      isUsed: productKey.isUsed,
      available: productKey.isActive && !productKey.isUsed
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Validate product key (without consuming it)
router.post('/validate', async (req, res) => {
  try {
    const { key } = req.body;
    
    if (!key) {
      return res.status(400).json({ message: 'Product key is required' });
    }
    
    const productKey = await ProductKey.findOne({ key, isActive: true });
    
    if (!productKey) {
      return res.status(404).json({ 
        valid: false, 
        message: 'Invalid product key' 
      });
    }
    
    if (productKey.isUsed) {
      return res.status(400).json({ 
        valid: false, 
        message: 'Product key has already been used' 
      });
    }
    
    res.json({
      valid: true,
      productName: productKey.productName,
      message: 'Product key is valid and available'
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Create new product key (admin only)
router.post('/', auth, async (req, res) => {
  try {
    const { key, productName } = req.body;
    
    if (!key || !productName) {
      return res.status(400).json({ message: 'Key and product name are required' });
    }
    
    const existingKey = await ProductKey.findOne({ key });
    if (existingKey) {
      return res.status(400).json({ message: 'Product key already exists' });
    }
    
    const productKey = new ProductKey({ key, productName });
    await productKey.save();
    
    res.status(201).json(productKey);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Deactivate product key (admin only)
router.patch('/:id/deactivate', auth, async (req, res) => {
  try {
    const productKey = await ProductKey.findById(req.params.id);
    
    if (!productKey) {
      return res.status(404).json({ message: 'Product key not found' });
    }
    
    productKey.isActive = false;
    await productKey.save();
    
    res.json({ message: 'Product key deactivated', productKey });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Get usage statistics
router.get('/stats', auth, async (req, res) => {
  try {
    const total = await ProductKey.countDocuments({});
    const active = await ProductKey.countDocuments({ isActive: true });
    const used = await ProductKey.countDocuments({ isUsed: true });
    const available = await ProductKey.countDocuments({ isActive: true, isUsed: false });
    
    res.json({
      total,
      active,
      used,
      available,
      inactive: total - active
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;
