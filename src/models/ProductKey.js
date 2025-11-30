const mongoose = require('mongoose');

const productKeySchema = new mongoose.Schema({
  key: {
    type: String,
    required: true,
    unique: true,
    trim: true
  },
  productId: {
    type: String,
    required: true,
    trim: true
  },
  productName: {
    type: String,
    required: true
  },
  isActive: {
    type: Boolean,
    default: true
  },
  isUsed: {
    type: Boolean,
    default: false
  },
  usedBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    default: null
  },
  usedAt: {
    type: Date,
    default: null
  }
}, {
  timestamps: true
});

// Method to mark key as used
productKeySchema.methods.markAsUsed = async function(userId) {
  this.isUsed = true;
  this.usedBy = userId;
  this.usedAt = new Date();
  return await this.save();
};

// Static method to validate and consume a product key
productKeySchema.statics.validateAndConsume = async function(key) {
  const productKey = await this.findOne({ key, isActive: true });
  
  if (!productKey) {
    throw new Error('Invalid product key');
  }
  
  if (productKey.isUsed) {
    throw new Error('Product key has already been used');
  }
  
  return productKey;
};

module.exports = mongoose.model('ProductKey', productKeySchema);
