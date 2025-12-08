const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const pendingUserSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true
  },
  password: {
    type: String,
    required: true,
    minlength: 6
  },
  fullName: {
    type: String,
    required: true
  },
  phoneNumber: {
    type: String,
    required: true
  },
  productKey: {
    type: String,
    required: true
  },
  createdAt: {
    type: Date,
    default: Date.now,
    expires: 3600 // Pending user data expires after 1 hour
  }
}, {
  timestamps: true
});

pendingUserSchema.pre('save', async function() {
  if (!this.isModified('password')) return;
  this.password = await bcrypt.hash(this.password, 12);
});

module.exports = mongoose.model('PendingUser', pendingUserSchema);
