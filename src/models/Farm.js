const mongoose = require('mongoose');

/**
 * Farm Schema - Stores farm/field information
 * Matches the "Add Farm" form fields:
 * - Field Name (name)
 * - Field Size (size) 
 * - Unit (unit)
 * - Crop Type (cropType)
 * - Soil Type - Auto-detected (soilType)
 * - Location & Soil Detection (location, latitude, longitude, soilData)
 * - Sowing Date (sowingDate)
 */
const farmSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: [true, 'User ID is required'],
    index: true
  },
  name: {
    type: String,
    required: [true, 'Field name is required'],
    trim: true,
    maxlength: [200, 'Field name cannot exceed 200 characters']
  },
  size: {
    type: Number,
    required: [true, 'Field size is required'],
    min: [0.01, 'Field size must be greater than 0'],
    validate: {
      validator: function(v) {
        return v > 0;
      },
      message: 'Field size must be a positive number'
    }
  },
  unit: {
    type: String,
    enum: {
      values: ['hectares', 'acres', 'bigha'],
      message: '{VALUE} is not a valid unit. Choose from: hectares, acres, bigha'
    },
    required: [true, 'Unit is required'],
    default: 'hectares'
  },
  cropType: {
    type: String,
    required: [true, 'Crop type is required'],
    trim: true,
    index: true
  },
  soilType: {
    type: String,
    required: [true, 'Soil type is required (auto-detected via location)'],
    trim: true,
    index: true
  },
  location: {
    type: String,
    trim: true,
    maxlength: [500, 'Location cannot exceed 500 characters']
  },
  latitude: {
    type: Number,
    min: [-90, 'Latitude must be between -90 and 90'],
    max: [90, 'Latitude must be between -90 and 90']
  },
  longitude: {
    type: Number,
    min: [-180, 'Longitude must be between -180 and 180'],
    max: [180, 'Longitude must be between -180 and 180']
  },
  soilData: {
    type: mongoose.Schema.Types.Mixed,
    // Stores detailed soil properties as JSON from the soil detection API
    // Example: { ph: 6.5, nitrogen: 45, phosphorus: 30, potassium: 35, ... }
  },
  sowingDate: {
    type: Date,
    required: [true, 'Sowing date is required'],
    validate: {
      validator: function(v) {
        // Sowing date should not be in the future
        return v <= new Date();
      },
      message: 'Sowing date cannot be in the future'
    }
  }
}, {
  timestamps: true, // Adds createdAt and updatedAt automatically
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

// Compound index for location-based queries
farmSchema.index({ latitude: 1, longitude: 1 });

// Index for date-based queries
farmSchema.index({ sowingDate: 1 });

// Compound index for user's farms sorted by creation
farmSchema.index({ userId: 1, createdAt: -1 });

module.exports = mongoose.model('Farm', farmSchema);
