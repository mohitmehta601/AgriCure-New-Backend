// Test script to check farms in database
require('dotenv').config();
const mongoose = require('mongoose');

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/agricure';

mongoose.connect(MONGODB_URI)
  .then(() => console.log('✅ Connected to MongoDB'))
  .catch(err => console.error('❌ MongoDB connection error:', err));

const farmSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  name: String,
  size: Number,
  unit: String,
  cropType: String,
  soilType: String,
  location: String,
  latitude: Number,
  longitude: Number,
  soilData: mongoose.Schema.Types.Mixed,
  sowingDate: Date
}, { timestamps: true });

const Farm = mongoose.model('Farm', farmSchema);
const User = mongoose.model('User', new mongoose.Schema({
  email: String,
  fullName: String,
  phoneNumber: String
}, { timestamps: true }));

async function testFarms() {
  try {
    // Get all users
    const users = await User.find().limit(5);
    console.log('\n📊 Users in database:', users.length);
    
    if (users.length > 0) {
      console.log('\nFirst user:', {
        id: users[0]._id.toString(),
        email: users[0].email,
        fullName: users[0].fullName
      });
      
      // Get farms for first user
      const farms = await Farm.find({ userId: users[0]._id });
      console.log(`\n🌾 Farms for ${users[0].email}:`, farms.length);
      
      if (farms.length > 0) {
        console.log('\nFirst farm data:');
        console.log(JSON.stringify(farms[0], null, 2));
      } else {
        console.log('\n⚠️  No farms found for this user');
      }
    } else {
      console.log('\n⚠️  No users in database');
    }
    
    // Get all farms
    const allFarms = await Farm.find().limit(10);
    console.log('\n🌾 Total farms in database:', allFarms.length);
    
    if (allFarms.length > 0) {
      console.log('\nSample farm:');
      const farm = allFarms[0];
      console.log({
        id: farm._id.toString(),
        name: farm.name,
        size: farm.size,
        unit: farm.unit,
        cropType: farm.cropType,
        soilType: farm.soilType,
        location: farm.location,
        sowingDate: farm.sowingDate,
        createdAt: farm.createdAt
      });
    }
    
  } catch (error) {
    console.error('❌ Error:', error);
  } finally {
    await mongoose.connection.close();
    console.log('\n✅ Connection closed');
  }
}

testFarms();
