const mongoose = require('mongoose');

const recommendationSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  farmId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Farm'
  },
  fieldName: String,
  fieldSize: Number,
  fieldSizeUnit: String,
  cropType: String,
  soilPh: Number,
  nitrogen: Number,
  phosphorus: Number,
  potassium: Number,
  temperature: Number,
  humidity: Number,
  soilMoisture: Number,
  primaryFertilizer: String,
  secondaryFertilizer: String,
  mlPrediction: String,
  confidenceScore: Number,
  applicationRate: Number,
  applicationRateUnit: String,
  applicationMethod: String,
  applicationTiming: String,
  recommendations: mongoose.Schema.Types.Mixed,
  status: {
    type: String,
    enum: ['pending', 'applied', 'scheduled'],
    default: 'pending'
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Recommendation', recommendationSchema);
