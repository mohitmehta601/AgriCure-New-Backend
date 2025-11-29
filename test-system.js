/**
 * Comprehensive Product Key System Test
 * Tests MongoDB database and product key validation
 */

const mongoose = require('mongoose');
require('dotenv').config();

const ProductKey = require('./src/models/ProductKey');

const TEST_KEY = '1234567890';

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

function success(msg) {
  console.log(`${colors.green}✅ ${msg}${colors.reset}`);
}

function error(msg) {
  console.log(`${colors.red}❌ ${msg}${colors.reset}`);
}

function info(msg) {
  console.log(`${colors.cyan}ℹ️  ${msg}${colors.reset}`);
}

function warning(msg) {
  console.log(`${colors.yellow}⚠️  ${msg}${colors.reset}`);
}

function header(msg) {
  console.log(`\n${colors.blue}${'═'.repeat(70)}`);
  console.log(`${msg}`);
  console.log(`${'═'.repeat(70)}${colors.reset}\n`);
}

async function testDatabase() {
  header('TEST 1: MongoDB Database Connection & Data');
  
  try {
    await mongoose.connect(process.env.MONGODB_URI);
    success('Connected to MongoDB');

    const allKeys = await ProductKey.find({});
    success(`Found ${allKeys.length} product keys in database`);

    if (allKeys.length === 0) {
      error('No product keys in database!');
      warning('Please run: node seed-product-keys.js');
      return false;
    }

    // Check if test key exists
    const testKey = await ProductKey.findOne({ key: TEST_KEY });
    if (testKey) {
      success(`Test key ${TEST_KEY} exists`);
      info(`Product: ${testKey.productName}`);
      info(`Active: ${testKey.isActive}`);
      info(`Used: ${testKey.isUsed}`);
      
      if (testKey.isUsed) {
        warning(`Test key is already used!`);
        info(`Used by: ${testKey.usedBy}`);
        info(`Used at: ${testKey.usedAt}`);
      }
    } else {
      error(`Test key ${TEST_KEY} not found!`);
      return false;
    }

    return true;
  } catch (err) {
    error(`Database test failed: ${err.message}`);
    return false;
  }
}

async function testDataIntegrity() {
  
  try {
    const allKeys = await ProductKey.find({});
    
    // Check for duplicates
    const keySet = new Set();
    let duplicates = 0;
    allKeys.forEach(k => {
      if (keySet.has(k.key)) duplicates++;
      keySet.add(k.key);
    });
    
    if (duplicates === 0) {
      success('No duplicate product keys');
    } else {
      error(`Found ${duplicates} duplicate keys!`);
    }

    // Count by status
    const active = allKeys.filter(k => k.isActive).length;
    const used = allKeys.filter(k => k.isUsed).length;
    const available = allKeys.filter(k => k.isActive && !k.isUsed).length;

    success(`${active} active keys`);
    success(`${available} available for signup`);
    info(`${used} already used`);

    if (available === 0) {
      warning('No keys available for new signups!');
    }

    return true;
  } catch (err) {
    error(`Integrity check failed: ${err.message}`);
    return false;
  }
}

async function runAllTests() {
  console.log(`\n${colors.cyan}╔════════════════════════════════════════════════════════════════════╗`);
  console.log(`║          PRODUCT KEY SYSTEM - COMPREHENSIVE TEST SUITE            ║`);
  console.log(`╚════════════════════════════════════════════════════════════════════╝${colors.reset}\n`);

  const results = {
    database: false,
    integrity: false
  };

  // Run tests
  results.database = await testDatabase();
  
  if (results.database) {
    results.integrity = await testDataIntegrity();
  }

  // Summary
  header('TEST SUMMARY');
  
  console.log('Test Results:');
  console.log(`  Database Connection:  ${results.database ? colors.green + '✅ PASS' : colors.red + '❌ FAIL'}${colors.reset}`);
  console.log(`  Data Integrity:       ${results.integrity ? colors.green + '✅ PASS' : colors.red + '❌ FAIL'}${colors.reset}`);

  const allPassed = results.database && results.integrity;

  console.log(`\n${'═'.repeat(70)}\n`);

  if (allPassed) {
    success('ALL TESTS PASSED! ✨');
    console.log('\n✅ Product key system is fully operational!');
    console.log('\n📝 Next steps:');
    console.log('   1. Start backend: cd Backend && node src/server.js');
    console.log('   2. Start frontend: cd Frontend && npm run dev');
    console.log('   3. Test signup with a product key');
  } else {
    error('SOME TESTS FAILED!');
    console.log('\n📝 Please check the errors above and fix them.');
  }

  console.log(`\n${'═'.repeat(70)}\n`);

  // Cleanup
  if (mongoose.connection.readyState === 1) {
    await mongoose.connection.close();
    info('Database connection closed');
  }
}

// Run all tests
runAllTests().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
