const express = require('express');
const Farm = require('../models/Farm');
const authMiddleware = require('../middleware/auth');
const router = express.Router();

router.use(authMiddleware);

// Create farm
router.post('/', async (req, res) => {
  try {
    const farm = new Farm({
      ...req.body,
      userId: req.user._id
    });
    await farm.save();
    res.status(201).json(farm);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

// Get user's farms
router.get('/user/:userId', async (req, res) => {
  try {
    const farms = await Farm.find({ userId: req.params.userId })
      .sort({ createdAt: -1 });
    res.json(farms);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Get farm by ID
router.get('/:id', async (req, res) => {
  try {
    const farm = await Farm.findById(req.params.id);
    if (!farm) {
      return res.status(404).json({ message: 'Farm not found' });
    }
    res.json(farm);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Update farm
router.put('/:id', async (req, res) => {
  try {
    const farm = await Farm.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true, runValidators: true }
    );
    if (!farm) {
      return res.status(404).json({ message: 'Farm not found' });
    }
    res.json(farm);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

// Delete farm
router.delete('/:id', async (req, res) => {
  try {
    const farm = await Farm.findByIdAndDelete(req.params.id);
    if (!farm) {
      return res.status(404).json({ message: 'Farm not found' });
    }
    res.json({ message: 'Farm deleted successfully' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;
