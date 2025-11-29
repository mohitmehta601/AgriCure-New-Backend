/**
 * Product Key Status Dashboard
 * 
 * This script displays the current status of all product keys in the system.
 * It shows which keys are available and which have been used.
 */

const ProductKey = require('./src/models/ProductKey');
const User = require('./src/models/User');
const mongoose = require('mongoose');
require('dotenv').config();

async function displayProductKeyStatus() {
  try {
    // Connect to MongoDB
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('✅ Connected to MongoDB\n');

    // Get all product keys
    const productKeys = await ProductKey.find({})
      .populate('usedBy', 'email fullName createdAt')
      .sort({ key: 1 });

    console.log('╔════════════════════════════════════════════════════════════════════════╗');
    console.log('║              PRODUCT KEY STATUS DASHBOARD                              ║');
    console.log('╚════════════════════════════════════════════════════════════════════════╝\n');

    // Statistics
    const total = productKeys.length;
    const available = productKeys.filter(k => k.isActive && !k.isUsed).length;
    const used = productKeys.filter(k => k.isUsed).length;
    const inactive = productKeys.filter(k => !k.isActive).length;

    console.log('📊 STATISTICS');
    console.log('─'.repeat(76));
    console.log(`Total Product Keys:     ${total}`);
    console.log(`✅ Available:           ${available} (${Math.round(available/total*100)}%)`);
    console.log(`🔒 Used:                ${used} (${Math.round(used/total*100)}%)`);
    console.log(`❌ Inactive:            ${inactive} (${Math.round(inactive/total*100)}%)`);
    console.log('');

    // Progress bar
    const barLength = 50;
    const usedBars = Math.round(used/total * barLength);
    const availableBars = barLength - usedBars;
    console.log('Usage Progress:');
    console.log('🔒'.repeat(usedBars) + '✅'.repeat(availableBars));
    console.log('');

    // Available Keys
    console.log('═'.repeat(76));
    console.log('✅ AVAILABLE PRODUCT KEYS (Ready for Signup)');
    console.log('═'.repeat(76));
    
    const availableKeys = productKeys.filter(k => k.isActive && !k.isUsed);
    if (availableKeys.length === 0) {
      console.log('⚠️  No available product keys! All keys have been used.');
      console.log('   Consider adding more product keys to allow new signups.\n');
    } else {
      console.log('┌──────────────┬───────────────────────────┬──────────┬─────────────┐');
      console.log('│ Product Key  │ Product Name              │ Active   │ Status      │');
      console.log('├──────────────┼───────────────────────────┼──────────┼─────────────┤');
      
      availableKeys.forEach(key => {
        const keyStr = key.key.padEnd(12);
        const nameStr = key.productName.padEnd(25);
        const activeStr = (key.isActive ? '✅ Yes' : '❌ No').padEnd(8);
        const statusStr = 'Available'.padEnd(11);
        console.log(`│ ${keyStr} │ ${nameStr} │ ${activeStr} │ ${statusStr} │`);
      });
      
      console.log('└──────────────┴───────────────────────────┴──────────┴─────────────┘');
      console.log('');
    }

    // Used Keys
    console.log('═'.repeat(76));
    console.log('🔒 USED PRODUCT KEYS (Already Consumed)');
    console.log('═'.repeat(76));
    
    const usedKeys = productKeys.filter(k => k.isUsed);
    if (usedKeys.length === 0) {
      console.log('No product keys have been used yet.\n');
    } else {
      console.log('┌──────────────┬───────────────────────────┬──────────────────────────┬─────────────────────┐');
      console.log('│ Product Key  │ Product Name              │ Used By                  │ Used At             │');
      console.log('├──────────────┼───────────────────────────┼──────────────────────────┼─────────────────────┤');
      
      usedKeys.forEach(key => {
        const keyStr = key.key.padEnd(12);
        const nameStr = key.productName.padEnd(25);
        const userStr = (key.usedBy?.email || 'Unknown').substring(0, 24).padEnd(24);
        const dateStr = key.usedAt ? 
          new Date(key.usedAt).toLocaleString('en-IN', { 
            timeZone: 'Asia/Kolkata',
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
          }).padEnd(19) : 
          'N/A'.padEnd(19);
        
        console.log(`│ ${keyStr} │ ${nameStr} │ ${userStr} │ ${dateStr} │`);
        
        // Show user details if available
        if (key.usedBy) {
          const fullName = key.usedBy.fullName || 'N/A';
          const userCreated = new Date(key.usedBy.createdAt).toLocaleString('en-IN', { 
            timeZone: 'Asia/Kolkata',
            dateStyle: 'medium',
            timeStyle: 'short'
          });
          console.log(`│              │   User: ${fullName.substring(0, 20).padEnd(20)} │ Created: ${userCreated.substring(0, 15).padEnd(15)}│                     │`);
        }
      });
      
      console.log('└──────────────┴───────────────────────────┴──────────────────────────┴─────────────────────┘');
      console.log('');
    }

    // Inactive Keys (if any)
    const inactiveKeys = productKeys.filter(k => !k.isActive);
    if (inactiveKeys.length > 0) {
      console.log('═'.repeat(76));
      console.log('❌ INACTIVE PRODUCT KEYS (Disabled)');
      console.log('═'.repeat(76));
      
      inactiveKeys.forEach(key => {
        console.log(`- ${key.key} (${key.productName})`);
      });
      console.log('');
    }

    // Warnings
    if (available <= 2 && available > 0) {
      console.log('⚠️  WARNING: Only ' + available + ' product key(s) remaining!');
      console.log('   Consider adding more product keys soon.\n');
    }

    // Footer
    console.log('═'.repeat(76));
    console.log('ℹ️  Note: Each product key can only be used ONCE to create an account.');
    console.log('   Used keys cannot be reused unless manually reset by an administrator.');
    console.log('═'.repeat(76));

  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    await mongoose.connection.close();
    console.log('\n✅ Disconnected from MongoDB');
  }
}

// Run the dashboard
console.log('Loading product key status...\n');
displayProductKeyStatus().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
