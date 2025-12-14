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
  electricalConductivity: Number,
  soilTemperature: Number,
  sowingDate: String,
  
  // ML Predictions
  primaryFertilizer: String,
  secondaryFertilizer: String,
  mlPrediction: String,
  confidenceScore: Number,
  
  // ML Response Data - storing complete response
  mlPredictions: mongoose.Schema.Types.Mixed, // Full ML predictions object
  costEstimate: mongoose.Schema.Types.Mixed, // Cost estimate details
  applicationTimingData: mongoose.Schema.Types.Mixed, // Application timing details
  organicAlternatives: mongoose.Schema.Types.Mixed, // Organic alternatives array
  enhancedReport: mongoose.Schema.Types.Mixed, // LLM enhanced report
  
  // Legacy fields for backward compatibility
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
  timestamps: true,
  toJSON: {
    virtuals: true,
    transform: function(doc, ret) {
      ret.id = ret._id.toString();
      delete ret._id;
      delete ret.__v;
      return ret;
    }
  }
});

module.exports = mongoose.model('Recommendation', recommendationSchema);
