const express = require('express');
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const ProductKey = require('../models/ProductKey');
const router = express.Router();

// Sign up
router.post('/signup', async (req, res) => {
  try {
    const { email, password, fullName, productKey, phoneNumber } = req.body;

    // Validate product key is provided
    if (!productKey) {
      return res.status(400).json({ message: 'Product key is required' });
    }

    // Validate phone number is provided
    if (!phoneNumber) {
      return res.status(400).json({ message: 'Phone number is required' });
    }

    // Check if email already registered
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ message: 'Email already registered' });
    }

    // Validate and consume product key
    let validatedKey;
    try {
      validatedKey = await ProductKey.validateAndConsume(productKey);
    } catch (keyError) {
      return res.status(400).json({ message: keyError.message });
    }

    // Create user
    const user = new User({
      email,
      password,
      fullName,
      productKey: validatedKey._id,
      productId: validatedKey.productId,
      productName: validatedKey.productName,
      phoneNumber
    });

    await user.save();

    // Mark product key as used
    await validatedKey.markAsUsed(user._id);

    const token = jwt.sign(
      { userId: user._id, email: user.email },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRES_IN }
    );

    res.status(201).json({
      token,
      user: {
        id: user._id,
        email: user.email,
        fullName: user.fullName,
        productId: user.productId,
        productName: user.productName,
        phoneNumber: user.phoneNumber,
        createdAt: user.createdAt,
        updatedAt: user.updatedAt
      }
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Login
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    const user = await User.findOne({ email });
    if (!user) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    const isMatch = await user.comparePassword(password);
    if (!isMatch) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    const token = jwt.sign(
      { userId: user._id, email: user.email },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRES_IN }
    );

    res.json({
      token,
      user: {
        id: user._id,
        email: user.email,
        fullName: user.fullName,
        productId: user.productId,
        phoneNumber: user.phoneNumber,
        createdAt: user.createdAt,
        updatedAt: user.updatedAt
      }
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Update password
router.post('/update-password', async (req, res) => {
  try {
    const { currentPassword, newPassword } = req.body;
    const token = req.headers.authorization?.replace('Bearer ', '');

    if (!token) {
      return res.status(401).json({ message: 'No token provided' });
    }

    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = await User.findById(decoded.userId);

    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    // Verify current password
    const isMatch = await user.comparePassword(currentPassword);
    if (!isMatch) {
      return res.status(401).json({ message: 'Current password is incorrect' });
    }

    // Update password
    user.password = newPassword;
    await user.save();

    res.json({ message: 'Password updated successfully' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;
