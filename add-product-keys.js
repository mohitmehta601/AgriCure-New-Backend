/**
 * Add New Product Keys to Database
 * Adds multiple product keys to the MongoDB database
 */

const mongoose = require('mongoose');
require('dotenv').config();

const ProductKey = require('./src/models/ProductKey');

// Product keys to add
const productKeysToAdd = [
  { key: "5819273401", productName: "AgriCure Growth" },
  { key: "7291046852", productName: "AgriCure Plus" },
  { key: "6472910583", productName: "AgriCure Essential" },
  { key: "9031782645", productName: "AgriCure Core" },
  { key: "7845129036", productName: "AgriCure Platinum" },
  { key: "6583091742", productName: "AgriCure Infinity" },
  { key: "2109873456", productName: "AgriCure Supreme" },
  { key: "5173928460", productName: "AgriCure Ultra Pro" },
  { key: "3648291057", productName: "AgriCure Digital" },
  { key: "2487139650", productName: "AgriCure AgroMax" },
  { key: "9836415270", productName: "AgriCure Agro Plus" },
  { key: "4526198370", productName: "AgriCure Complete" },
  { key: "6492837150", productName: "AgriCure Smart" },
  { key: "7315928461", productName: "AgriCure Smart Max" },
  { key: "5039271648", productName: "AgriCure Shield" },
  { key: "9823714560", productName: "AgriCure Green" },
  { key: "1649278305", productName: "AgriCure Organic" },
  { key: "7823614590", productName: "AgriCure Assist" },
  { key: "9648173502", productName: "AgriCure Boost" },
  { key: "7142938560", productName: "AgriCure Prime" },
  { key: "8251937460", productName: "AgriCure Vision" },
  { key: "5102946837", productName: "AgriCure Ultra" },
  { key: "6497285301", productName: "AgriCure Turbo" },
  { key: "8392756410", productName: "AgriCure Focus" },
  { key: "2918643750", productName: "AgriCure Edge" },
  { key: "5761489320", productName: "AgriCure Maxx" },
  { key: "9187346520", productName: "AgriCure Elevate" },
  { key: "7829051643", productName: "AgriCure Deluxe" },
  { key: "4502931876", productName: "AgriCure Master" },
  { key: "9082516473", productName: "AgriCure Insight" },
  { key: "3618794520", productName: "AgriCure Command" },
  { key: "5821673490", productName: "AgriCure Next" },
  { key: "7932465810", productName: "AgriCure Pro Max" },
  { key: "6827593140", productName: "AgriCure One" },
  { key: "7349128056", productName: "AgriCure AgroPro" },
  { key: "5249078136", productName: "AgriCure Champion" },
  { key: "6907158423", productName: "AgriCure Titan" },
  { key: "8592736140", productName: "AgriCure Hero" },
  { key: "4162958073", productName: "AgriCure Velocity" },
  { key: "7918532406", productName: "AgriCure Vision Pro" }
];

async function addProductKeys() {
  try {
    console.log('🔍 Connecting to MongoDB...\n');
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('✅ Connected to MongoDB\n');

    console.log('═══════════════════════════════════════════════════════════════');
    console.log('              ADDING NEW PRODUCT KEYS TO DATABASE              ');
    console.log('═══════════════════════════════════════════════════════════════\n');

    let addedCount = 0;
    let skippedCount = 0;
    let errorCount = 0;

    console.log(`📦 Processing ${productKeysToAdd.length} product keys...\n`);

    for (const keyData of productKeysToAdd) {
      try {
        // Check if key already exists
        const existingKey = await ProductKey.findOne({ key: keyData.key });
        
        if (existingKey) {
          console.log(`⚠️  SKIPPED: ${keyData.key} - "${keyData.productName}" (Already exists)`);
          skippedCount++;
        } else {
          // Add productId (using key as productId for now)
          const productKey = new ProductKey({
            key: keyData.key,
            productId: keyData.key,
            productName: keyData.productName,
            isActive: true,
            isUsed: false
          });
          
          await productKey.save();
          console.log(`✅ ADDED: ${keyData.key} - "${keyData.productName}"`);
          addedCount++;
        }
      } catch (error) {
        console.log(`❌ ERROR: ${keyData.key} - ${error.message}`);
        errorCount++;
      }
    }

    console.log('\n═══════════════════════════════════════════════════════════════');
    console.log('                         SUMMARY                                ');
    console.log('═══════════════════════════════════════════════════════════════\n');
    console.log(`✅ Successfully Added:  ${addedCount}`);
    console.log(`⚠️  Skipped (Existing): ${skippedCount}`);
    console.log(`❌ Errors:              ${errorCount}`);
    console.log(`📊 Total Processed:     ${productKeysToAdd.length}\n`);

    // Show current database stats
    const totalKeys = await ProductKey.countDocuments({});
    const availableKeys = await ProductKey.countDocuments({ isActive: true, isUsed: false });
    const usedKeys = await ProductKey.countDocuments({ isUsed: true });

    console.log('📈 Current Database Status:');
    console.log(`   Total Keys in DB:     ${totalKeys}`);
    console.log(`   Available for Signup: ${availableKeys}`);
    console.log(`   Already Used:         ${usedKeys}\n`);

    console.log('✨ Done! Product keys have been processed.\n');

  } catch (error) {
    console.error('❌ Error:', error.message);
    console.error(error);
  } finally {
    await mongoose.connection.close();
    console.log('🔒 Database connection closed.');
  }
}

// Run the script
addProductKeys();
