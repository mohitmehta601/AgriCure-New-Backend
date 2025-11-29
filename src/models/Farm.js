const mongoose = require('mongoose');

const farmSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  name: {
    type: String,
    required: true
  },
  size: {
    type: Number,
    required: true
  },
  unit: {
    type: String,
    enum: ['hectares', 'acres', 'bigha'],
    required: true
  },
  cropType: String,
  soilType: String,
  location: String,
  latitude: Number,
  longitude: Number,
  soilData: mongoose.Schema.Types.Mixed,
  sowingDate: Date
}, {
  timestamps: true
});

module.exports = mongoose.model('Farm', farmSchema);
