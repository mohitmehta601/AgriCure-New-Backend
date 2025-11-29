/**
 * Quick Product Key Verification Script
 * Checks MongoDB database for product keys
 */

const mongoose = require('mongoose');
require('dotenv').config();

const ProductKey = require('./src/models/ProductKey');

async function verifyProductKeys() {
  try {
    console.log('🔍 Connecting to MongoDB...\n');
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('✅ Connected to MongoDB\n');

    // Get all product keys
    const allKeys = await ProductKey.find({}).sort({ key: 1 });
    
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('                  PRODUCT KEY VERIFICATION                     ');
    console.log('═══════════════════════════════════════════════════════════════\n');

    console.log(`Total Product Keys: ${allKeys.length}\n`);

    if (allKeys.length === 0) {
      console.log('❌ No product keys found in database!');
      console.log('   Run: node seed-product-keys.js to add product keys\n');
    } else {
      console.log('┌────────────┬───────────────────────────┬────────┬────────┐');
      console.log('│ Key        │ Product Name              │ Active │ Used   │');
      console.log('├────────────┼───────────────────────────┼────────┼────────┤');
      
      let available = 0;
      let used = 0;
      
      allKeys.forEach(key => {
        const keyStr = key.key.padEnd(10);
        const nameStr = key.productName.padEnd(25);
        const activeStr = (key.isActive ? '✅ Yes' : '❌ No').padEnd(6);
        const usedStr = (key.isUsed ? '🔒 Yes' : '✅ No').padEnd(6);
        
        if (key.isActive && !key.isUsed) available++;
        if (key.isUsed) used++;
        
        console.log(`│ ${keyStr} │ ${nameStr} │ ${activeStr} │ ${usedStr} │`);
      });
      
      console.log('└────────────┴───────────────────────────┴────────┴────────┘\n');
      
      console.log('📊 Summary:');
      console.log(`   Available for signup: ${available} keys`);
      console.log(`   Already used:         ${used} keys`);
      console.log(`   Total:                ${allKeys.length} keys\n`);
      
      if (available > 0) {
        console.log('✅ SYSTEM STATUS: Ready for signups!');
        console.log(`   ${available} product key(s) available for new users.\n`);
      } else {
        console.log('⚠️  SYSTEM STATUS: No available keys!');
        console.log('   All product keys have been used or are inactive.\n');
      }
    }

    console.log('═══════════════════════════════════════════════════════════════\n');

    await mongoose.connection.close();
    console.log('✅ Database connection closed\n');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

verifyProductKeys();
