/**
 * MongoDB Farm Collection Update Script
 * 
 * This script ensures the farms collection has:
 * - Proper validation rules
 * - Required indexes for performance
 * - All fields from the Add Farm form
 * 
 * Run this script to update your MongoDB database
 */

require('dotenv').config();
const mongoose = require('mongoose');

async function updateFarmCollection() {
  try {
    console.log('🔄 Connecting to MongoDB...');
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('✅ Connected to MongoDB\n');

    const db = mongoose.connection.db;
    const farmsCollection = db.collection('farms');

    console.log('📋 Farm Collection Update Process Started\n');

    // Step 1: Check if collection exists
    const collections = await db.listCollections({ name: 'farms' }).toArray();
    if (collections.length === 0) {
      console.log('⚠️  Farms collection does not exist. Creating it...');
      await db.createCollection('farms');
      console.log('✅ Farms collection created\n');
    } else {
      console.log('✅ Farms collection already exists\n');
    }

    // Step 2: Create/Update indexes
    console.log('📊 Creating indexes...');
    
    try {
      // User ID index (for RLS-like queries)
      await farmsCollection.createIndex({ userId: 1 });
      console.log('  ✅ Index created: userId');

      // Location indexes
      await farmsCollection.createIndex({ latitude: 1, longitude: 1 });
      console.log('  ✅ Index created: latitude + longitude (compound)');

      // Sowing date index
      await farmsCollection.createIndex({ sowingDate: 1 });
      console.log('  ✅ Index created: sowingDate');

      // Crop type index
      await farmsCollection.createIndex({ cropType: 1 });
      console.log('  ✅ Index created: cropType');

      // Soil type index
      await farmsCollection.createIndex({ soilType: 1 });
      console.log('  ✅ Index created: soilType');

      // Compound index for user's farms sorted by creation
      await farmsCollection.createIndex({ userId: 1, createdAt: -1 });
      console.log('  ✅ Index created: userId + createdAt (compound)');

      // Timestamp indexes
      await farmsCollection.createIndex({ createdAt: -1 });
      console.log('  ✅ Index created: createdAt');

      console.log('\n✅ All indexes created successfully\n');
    } catch (indexError) {
      console.log('⚠️  Some indexes may already exist (this is OK)');
      console.log(`   Details: ${indexError.message}\n`);
    }

    // Step 3: Add validation schema
    console.log('🔒 Setting up validation schema...');
    
    try {
      await db.command({
        collMod: 'farms',
        validator: {
          $jsonSchema: {
            bsonType: 'object',
            required: ['userId', 'name', 'size', 'unit', 'cropType', 'soilType', 'sowingDate'],
            properties: {
              userId: {
                bsonType: 'objectId',
                description: 'User ID is required and must be an ObjectId'
              },
              name: {
                bsonType: 'string',
                minLength: 1,
                maxLength: 200,
                description: 'Field name is required and must be 1-200 characters'
              },
              size: {
                bsonType: 'number',
                minimum: 0.01,
                description: 'Field size must be a positive number greater than 0'
              },
              unit: {
                enum: ['hectares', 'acres', 'bigha'],
                description: 'Unit must be one of: hectares, acres, bigha'
              },
              cropType: {
                bsonType: 'string',
                minLength: 1,
                description: 'Crop type is required'
              },
              soilType: {
                bsonType: 'string',
                minLength: 1,
                description: 'Soil type is required (auto-detected via location)'
              },
              location: {
                bsonType: 'string',
                maxLength: 500,
                description: 'Human-readable location name/address'
              },
              latitude: {
                bsonType: 'number',
                minimum: -90,
                maximum: 90,
                description: 'GPS latitude coordinate (-90 to 90)'
              },
              longitude: {
                bsonType: 'number',
                minimum: -180,
                maximum: 180,
                description: 'GPS longitude coordinate (-180 to 180)'
              },
              soilData: {
                bsonType: 'object',
                description: 'Detailed soil properties from API (JSON format)'
              },
              sowingDate: {
                bsonType: 'date',
                description: 'Date when crop was sowed/planted'
              },
              createdAt: {
                bsonType: 'date',
                description: 'Record creation timestamp'
              },
              updatedAt: {
                bsonType: 'date',
                description: 'Record last update timestamp'
              }
            }
          }
        },
        validationLevel: 'moderate', // Apply to new inserts and updates
        validationAction: 'error'     // Reject invalid documents
      });
      console.log('✅ Validation schema applied successfully\n');
    } catch (validationError) {
      console.log('⚠️  Validation schema update failed (may already exist)');
      console.log(`   Details: ${validationError.message}\n`);
    }

    // Step 4: Display current schema
    console.log('📄 Current Farm Collection Schema:');
    console.log('=====================================');
    console.log('Required Fields:');
    console.log('  • userId         - Reference to user (ObjectId)');
    console.log('  • name           - Field Name (string, 1-200 chars)');
    console.log('  • size           - Field Size (number, > 0)');
    console.log('  • unit           - Unit (hectares/acres/bigha)');
    console.log('  • cropType       - Crop Type (string)');
    console.log('  • soilType       - Soil Type - Auto-detected (string)');
    console.log('  • sowingDate     - Sowing Date (date)');
    console.log('\nOptional Fields:');
    console.log('  • location       - Location name/address (string, max 500 chars)');
    console.log('  • latitude       - GPS latitude (-90 to 90)');
    console.log('  • longitude      - GPS longitude (-180 to 180)');
    console.log('  • soilData       - Detailed soil properties (JSON)');
    console.log('\nAuto-Generated:');
    console.log('  • createdAt      - Creation timestamp');
    console.log('  • updatedAt      - Last update timestamp');
    console.log('=====================================\n');

    // Step 5: Count existing farms
    const farmCount = await farmsCollection.countDocuments();
    console.log(`📊 Total farms in database: ${farmCount}\n`);

    // Step 6: Show sample document structure
    if (farmCount > 0) {
      console.log('📋 Sample Farm Document:');
      const sampleFarm = await farmsCollection.findOne();
      console.log(JSON.stringify(sampleFarm, null, 2));
      console.log('\n');
    }

    // Step 7: List all indexes
    console.log('📑 Current Indexes:');
    const indexes = await farmsCollection.indexes();
    indexes.forEach((index, i) => {
      console.log(`  ${i + 1}. ${index.name}: ${JSON.stringify(index.key)}`);
    });
    console.log('\n');

    console.log('✅ Farm collection update completed successfully!\n');

  } catch (error) {
    console.error('❌ Error updating farm collection:', error);
    process.exit(1);
  } finally {
    await mongoose.connection.close();
    console.log('🔌 Database connection closed');
    process.exit(0);
  }
}

// Run the update
updateFarmCollection();
