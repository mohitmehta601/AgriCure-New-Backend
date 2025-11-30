// Test Farm model toJSON transformation
require('dotenv').config();
const mongoose = require('mongoose');
const Farm = require('./src/models/Farm');

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/agricure';

mongoose.connect(MONGODB_URI)
  .then(async () => {
    console.log('✅ Connected to MongoDB');
    
    // Find a farm
    const farm = await Farm.findOne();
    if (farm) {
      console.log('\n📦 Farm document from MongoDB:');
      console.log('_id:', farm._id);
      console.log('name:', farm.name);
      
      console.log('\n🔄 Farm as JSON (with toJSON transform):');
      const jsonFarm = farm.toJSON();
      console.log(JSON.stringify(jsonFarm, null, 2));
      
      console.log('\n✅ Check: Does JSON have "id"?', 'id' in jsonFarm);
      console.log('✅ Check: Does JSON have "_id"?', '_id' in jsonFarm);
    } else {
      console.log('⚠️  No farms found');
    }
    
    await mongoose.connection.close();
  })
  .catch(err => {
    console.error('❌ Error:', err);
    process.exit(1);
  });
