const mongoose = require('mongoose');
require('dotenv').config();

const ProductKey = require('./src/models/ProductKey');

const productKeys = [
  { key: '1029384756', productId: '1029384756', productName: 'AgriCure Standard' },
  { key: '1234567890', productId: '1234567890', productName: 'AgriCure Starter' },
  { key: '3141592653', productId: '3141592653', productName: 'AgriCure Advanced' },
  { key: '4516273980', productId: '4516273980', productName: 'AgriCure Ultimate' },
  { key: '5647382910', productId: '5647382910', productName: 'AgriCure Premium' },
  { key: '6758493021', productId: '6758493021', productName: 'AgriCure Basic' },
  { key: '7263549810', productId: '7263549810', productName: 'AgriCure Professional' },
  { key: '8391027465', productId: '8391027465', productName: 'AgriCure Elite' },
  { key: '8972345610', productId: '8972345610', productName: 'AgriCure Pro' },
  { key: '9081726354', productId: '9081726354', productName: 'AgriCure Enterprise' }
];

const seedProductKeys = async () => {
  try {
    // Connect to MongoDB
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('✅ Connected to MongoDB');

    // Clear existing product keys (optional - comment out if you want to keep existing ones)
    await ProductKey.deleteMany({});
    console.log('🗑️  Cleared existing product keys');

    // Insert product keys
    const result = await ProductKey.insertMany(productKeys);
    console.log(`✅ Successfully added ${result.length} product keys`);

    // Display all product keys
    const allKeys = await ProductKey.find({});
    console.log('\n📋 Product Keys in Database:');
    console.log('================================');
    allKeys.forEach(key => {
      console.log(`Key: ${key.key} | Product ID: ${key.productId} | Product: ${key.productName} | Used: ${key.isUsed}`);
    });

    mongoose.connection.close();
    console.log('\n✅ Database connection closed');
  } catch (error) {
    console.error('❌ Error seeding product keys:', error);
    process.exit(1);
  }
};

seedProductKeys();
