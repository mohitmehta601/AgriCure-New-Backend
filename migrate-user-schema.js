const mongoose = require('mongoose');
require('dotenv').config();

// Connect to MongoDB
const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI || process.env.DATABASE_URL, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log('✅ MongoDB Connected');
  } catch (error) {
    console.error('❌ MongoDB connection error:', error);
    process.exit(1);
  }
};

// Migration function
const migrateUserSchema = async () => {
  try {
    console.log('\n🔄 Starting User Schema Migration...\n');

    const db = mongoose.connection.db;
    const usersCollection = db.collection('users');

    // Get all users
    const users = await usersCollection.find({}).toArray();
    console.log(`📊 Found ${users.length} users to migrate\n`);

    let updated = 0;
    let skipped = 0;
    let errors = 0;

    for (const user of users) {
      try {
        const updates = {};
        const fieldsToUnset = {};
        let needsUpdate = false;

        // Add default phone number if missing
        if (!user.phoneNumber) {
          updates.phoneNumber = '+91 0000000000'; // Default placeholder
          needsUpdate = true;
          console.log(`  ➕ Adding default phone number for user: ${user.email}`);
        }

        // Remove deprecated fields
        if (user.farmLocation !== undefined) {
          fieldsToUnset.farmLocation = '';
          needsUpdate = true;
          console.log(`  ➖ Removing farmLocation from user: ${user.email}`);
        }

        if (user.farmSize !== undefined) {
          fieldsToUnset.farmSize = '';
          needsUpdate = true;
          console.log(`  ➖ Removing farmSize from user: ${user.email}`);
        }

        if (user.farmSizeUnit !== undefined) {
          fieldsToUnset.farmSizeUnit = '';
          needsUpdate = true;
          console.log(`  ➖ Removing farmSizeUnit from user: ${user.email}`);
        }

        if (needsUpdate) {
          const updateOperation = {};
          
          if (Object.keys(updates).length > 0) {
            updateOperation.$set = updates;
          }
          
          if (Object.keys(fieldsToUnset).length > 0) {
            updateOperation.$unset = fieldsToUnset;
          }

          await usersCollection.updateOne(
            { _id: user._id },
            updateOperation
          );
          
          updated++;
          console.log(`  ✅ Updated user: ${user.email}\n`);
        } else {
          skipped++;
          console.log(`  ⏭️  Skipped user (already migrated): ${user.email}\n`);
        }
      } catch (error) {
        errors++;
        console.error(`  ❌ Error updating user ${user.email}:`, error.message, '\n');
      }
    }

    console.log('\n📈 Migration Summary:');
    console.log(`   Total Users: ${users.length}`);
    console.log(`   ✅ Updated: ${updated}`);
    console.log(`   ⏭️  Skipped: ${skipped}`);
    console.log(`   ❌ Errors: ${errors}`);
    console.log('\n✨ Migration completed!\n');

  } catch (error) {
    console.error('❌ Migration failed:', error);
    process.exit(1);
  }
};

// Run migration
const runMigration = async () => {
  await connectDB();
  await migrateUserSchema();
  await mongoose.connection.close();
  console.log('🔌 Database connection closed\n');
  process.exit(0);
};

runMigration();
