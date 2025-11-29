const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
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
  farmLocation: String,
  phoneNumber: String,
  farmSize: Number,
  farmSizeUnit: {
    type: String,
    enum: ['hectares', 'acres', 'bigha'],
    default: 'hectares'
  },
  productId: String,
  productKey: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'ProductKey',
    required: true
  },
  productName: String,
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true
});

userSchema.pre('save', async function() {
  if (!this.isModified('password')) return;
  this.password = await bcrypt.hash(this.password, 12);
});

userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', userSchema);
