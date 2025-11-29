const express = require('express');
const Recommendation = require('../models/Recommendation');
const authMiddleware = require('../middleware/auth');
const router = express.Router();

router.use(authMiddleware);

// Create recommendation
router.post('/', async (req, res) => {
  try {
    const recommendation = new Recommendation({
      ...req.body,
      userId: req.user._id
    });
    await recommendation.save();
    res.status(201).json(recommendation);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

// Get user's recommendations
router.get('/user/:userId', async (req, res) => {
  try {
    const recommendations = await Recommendation.find({ userId: req.params.userId })
      .sort({ createdAt: -1 });
    res.json(recommendations);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Get recommendation by ID
router.get('/:id', async (req, res) => {
  try {
    const recommendation = await Recommendation.findById(req.params.id);
    if (!recommendation) {
      return res.status(404).json({ message: 'Recommendation not found' });
    }
    res.json(recommendation);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Update recommendation
router.patch('/:id', async (req, res) => {
  try {
    const recommendation = await Recommendation.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true, runValidators: true }
    );
    if (!recommendation) {
      return res.status(404).json({ message: 'Recommendation not found' });
    }
    res.json(recommendation);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

// Delete recommendation
router.delete('/:id', async (req, res) => {
  try {
    const recommendation = await Recommendation.findByIdAndDelete(req.params.id);
    if (!recommendation) {
      return res.status(404).json({ message: 'Recommendation not found' });
    }
    res.json({ message: 'Recommendation deleted successfully' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;
