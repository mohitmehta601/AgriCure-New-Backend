/**
 * Migrate Existing Farm Records
 * 
 * This script updates existing farm records to include all required fields
 * from the new schema. It adds default values for missing fields.
 */

require('dotenv').config();
const mongoose = require('mongoose');

async function migrateExistingFarms() {
  try {
    console.log('🔄 Connecting to MongoDB...');
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('✅ Connected to MongoDB\n');

    const db = mongoose.connection.db;
    const farmsCollection = db.collection('farms');

    console.log('🔄 Migrating existing farm records...\n');

    // Find all farms that are missing required fields
    const farms = await farmsCollection.find({}).toArray();
    console.log(`📊 Found ${farms.length} farm(s) in database\n`);

    let updatedCount = 0;
    let skippedCount = 0;

    for (const farm of farms) {
      const updates = {};
      let needsUpdate = false;

      // Check and add missing fields with default values
      if (!farm.cropType) {
        updates.cropType = 'Not Specified';
        needsUpdate = true;
        console.log(`  ⚠️  Farm "${farm.name}" missing cropType - will set to "Not Specified"`);
      }

      if (!farm.soilType) {
        updates.soilType = 'Not Detected';
        needsUpdate = true;
        console.log(`  ⚠️  Farm "${farm.name}" missing soilType - will set to "Not Detected"`);
      }

      if (!farm.sowingDate) {
        // Use createdAt as default sowing date if available
        updates.sowingDate = farm.createdAt || new Date();
        needsUpdate = true;
        console.log(`  ⚠️  Farm "${farm.name}" missing sowingDate - will set to ${updates.sowingDate}`);
      }

      if (!farm.unit) {
        updates.unit = 'hectares';
        needsUpdate = true;
        console.log(`  ⚠️  Farm "${farm.name}" missing unit - will set to "hectares"`);
      }

      if (needsUpdate) {
        await farmsCollection.updateOne(
          { _id: farm._id },
          { $set: updates }
        );
        updatedCount++;
        console.log(`  ✅ Updated farm: "${farm.name}"\n`);
      } else {
        skippedCount++;
        console.log(`  ✓  Farm "${farm.name}" already has all required fields\n`);
      }
    }

    console.log('=====================================');
    console.log(`✅ Migration completed!`);
    console.log(`   Updated: ${updatedCount} farm(s)`);
    console.log(`   Skipped: ${skippedCount} farm(s) (already complete)`);
    console.log(`   Total:   ${farms.length} farm(s)`);
    console.log('=====================================\n');

    // Verify all farms now have required fields
    console.log('🔍 Verifying all farms have required fields...');
    const missingFieldsFarms = await farmsCollection.find({
      $or: [
        { cropType: { $exists: false } },
        { soilType: { $exists: false } },
        { sowingDate: { $exists: false } },
        { unit: { $exists: false } }
      ]
    }).toArray();

    if (missingFieldsFarms.length === 0) {
      console.log('✅ All farms now have all required fields!\n');
    } else {
      console.log(`⚠️  Warning: ${missingFieldsFarms.length} farm(s) still missing required fields`);
      missingFieldsFarms.forEach(farm => {
        console.log(`   - Farm "${farm.name}" (ID: ${farm._id})`);
      });
      console.log('\n');
    }

  } catch (error) {
    console.error('❌ Error migrating farms:', error);
    process.exit(1);
  } finally {
    await mongoose.connection.close();
    console.log('🔌 Database connection closed');
    process.exit(0);
  }
}

// Run the migration
migrateExistingFarms();
