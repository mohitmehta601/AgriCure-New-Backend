const express = require('express');
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const ProductKey = require('../models/ProductKey');
const PendingUser = require('../models/PendingUser');
const OTP = require('../models/OTP');
const { sendOTPEmail } = require('../services/emailService');
const router = express.Router();

// Generate 6-digit OTP
const generateOTP = () => {
  return Math.floor(100000 + Math.random() * 900000).toString();
};

// Step 1: Sign up - Store user data and send OTP
router.post('/signup', async (req, res) => {
  try {
    const { email, password, fullName, productKey, phoneNumber } = req.body;

    // Validate required fields
    if (!productKey) {
      return res.status(400).json({ message: 'Product key is required' });
    }

    if (!phoneNumber) {
      return res.status(400).json({ message: 'Phone number is required' });
    }

    // Check if email already registered
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ message: 'Email already registered' });
    }

    // Validate product key (but don't consume it yet)
    let validatedKey;
    try {
      validatedKey = await ProductKey.findOne({ 
        key: productKey, 
        isUsed: false 
      });
      
      if (!validatedKey) {
        throw new Error('Invalid or already used product key');
      }
    } catch (keyError) {
      return res.status(400).json({ message: keyError.message });
    }

    // Delete any existing pending user with this email
    await PendingUser.deleteOne({ email });
    
    // Delete any existing OTPs for this email
    await OTP.deleteMany({ email });

    // Store user data temporarily
    const pendingUser = new PendingUser({
      email,
      password, // Will be hashed by pre-save hook
      fullName,
      phoneNumber,
      productKey
    });

    await pendingUser.save();

    // Generate and store OTP
    const otp = generateOTP();
    const otpDoc = new OTP({
      email,
      otp
    });

    await otpDoc.save();

    // Send OTP email
    try {
      await sendOTPEmail(email, otp);
    } catch (emailError) {
      // Clean up if email fails
      await PendingUser.deleteOne({ email });
      await OTP.deleteOne({ email });
      return res.status(500).json({ 
        message: 'Failed to send verification email. Please try again.' 
      });
    }

    res.status(200).json({
      message: 'OTP sent to your email. Please verify to complete registration.',
      email
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Step 2: Verify OTP and create user
router.post('/verify-otp', async (req, res) => {
  try {
    const { email, otp } = req.body;

    if (!email || !otp) {
      return res.status(400).json({ message: 'Email and OTP are required' });
    }

    // Find the OTP
    const otpDoc = await OTP.findOne({ 
      email, 
      otp,
      verified: false 
    }).sort({ createdAt: -1 });

    if (!otpDoc) {
      return res.status(400).json({ message: 'Invalid or expired OTP' });
    }

    // Find pending user data
    const pendingUser = await PendingUser.findOne({ email });
    if (!pendingUser) {
      return res.status(400).json({ message: 'User data not found. Please sign up again.' });
    }

    // Validate and consume product key
    let validatedKey;
    try {
      validatedKey = await ProductKey.validateAndConsume(pendingUser.productKey);
    } catch (keyError) {
      return res.status(400).json({ message: keyError.message });
    }

    // Create actual user
    const user = new User({
      email: pendingUser.email,
      password: pendingUser.password, // Already hashed
      fullName: pendingUser.fullName,
      productKey: validatedKey._id,
      productId: validatedKey.productId,
      productName: validatedKey.productName,
      phoneNumber: pendingUser.phoneNumber
    });

    // Save without re-hashing password
    user.isModified = () => false;
    await user.save();

    // Mark product key as used
    await validatedKey.markAsUsed(user._id);

    // Mark OTP as verified and clean up
    otpDoc.verified = true;
    await otpDoc.save();
    await PendingUser.deleteOne({ email });

    // Generate JWT token
    const token = jwt.sign(
      { userId: user._id, email: user.email },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRES_IN }
    );

    res.status(201).json({
      message: 'Email verified successfully! Account created.',
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

// Resend OTP
router.post('/resend-otp', async (req, res) => {
  try {
    const { email } = req.body;

    if (!email) {
      return res.status(400).json({ message: 'Email is required' });
    }

    // Check if pending user exists
    const pendingUser = await PendingUser.findOne({ email });
    if (!pendingUser) {
      return res.status(400).json({ message: 'No pending registration found for this email' });
    }

    // Delete old OTPs
    await OTP.deleteMany({ email });

    // Generate new OTP
    const otp = generateOTP();
    const otpDoc = new OTP({
      email,
      otp
    });

    await otpDoc.save();

    // Send OTP email
    await sendOTPEmail(email, otp);

    res.status(200).json({
      message: 'OTP resent successfully'
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
