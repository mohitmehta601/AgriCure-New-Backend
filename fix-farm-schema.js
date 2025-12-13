/**
 * Script to remove MongoDB collection validators for Farm model
 * This fixes the issue where MongoDB has cached the old schema with soilType field
 */
const mongoose = require('mongoose');
require('dotenv').config();

async function fixFarmSchema() {
  try {
    // Connect to MongoDB
    await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/agricure');
    console.log('✅ Connected to MongoDB');

    // Get the farms collection
    const db = mongoose.connection.db;
    const collection = db.collection('farms');

    // Remove collection validators by updating with empty validator
    await db.command({
      collMod: 'farms',
      validator: {},
      validationLevel: 'off'
    });

    console.log('✅ Removed old collection validators');

    // Get Farm model to reapply current schema validators
    const Farm = require('./src/models/Farm');
    
    console.log('✅ Farm model loaded with current schema (no soilType)');
    console.log('Current schema fields:', Object.keys(Farm.schema.paths));

    await mongoose.connection.close();
    console.log('✅ Done! Server will use updated schema.');
    process.exit(0);
  } catch (error) {
    console.error('❌ Error:', error);
    process.exit(1);
  }
}

fixFarmSchema();
