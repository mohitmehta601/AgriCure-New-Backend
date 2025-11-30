// Add sample farms matching the image
require('dotenv').config();
const mongoose = require('mongoose');
const Farm = require('./src/models/Farm');

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/agricure';

mongoose.connect(MONGODB_URI)
  .then(async () => {
    console.log('✅ Connected to MongoDB');
    
    const userId = '692c10a3ca94322e73ab32f9'; // Your user ID
    
    // Sample farms data matching the image
    const sampleFarms = [
      {
        userId: userId,
        name: 'field 2',
        size: 5,
        unit: 'acres',
        cropType: 'Cotton',
        soilType: 'Clayey',
        location: 'Greater Noida, Uttar Pradesh, India',
        latitude: 28.4744,
        longitude: 77.5040,
        sowingDate: new Date('2025-05-05'),
        soilData: {
          soil_type: 'Clayey',
          confidence: 0.85
        }
      },
      {
        userId: userId,
        name: 'field 1',
        size: 30,
        unit: 'bigha',
        cropType: 'Sugarcane',
        soilType: 'Clayey',
        location: 'Greater Noida, Uttar Pradesh, India',
        latitude: 28.4595,
        longitude: 77.5051,
        sowingDate: new Date('2025-05-12'),
        soilData: {
          soil_type: 'Clayey',
          confidence: 0.88
        }
      },
      {
        userId: userId,
        name: 'North Field',
        size: 5.5,
        unit: 'acres',
        cropType: 'Cotton',
        soilType: 'Clayey',
        location: 'Greater Noida, Uttar Pradesh, India',
        latitude: 28.4649,
        longitude: 77.5046,
        sowingDate: new Date('2025-05-06'),
        soilData: {
          soil_type: 'Clayey',
          confidence: 0.87
        }
      }
    ];
    
    // Delete existing farms for this user (optional)
    await Farm.deleteMany({ userId: userId });
    console.log('🗑️  Cleared existing farms');
    
    // Insert sample farms
    const inserted = await Farm.insertMany(sampleFarms);
    console.log(`✅ Inserted ${inserted.length} sample farms`);
    
    // Display the farms
    const farms = await Farm.find({ userId: userId }).sort({ createdAt: -1 });
    console.log('\n📊 Farms in database:');
    farms.forEach((farm, index) => {
      console.log(`\n${index + 1}. ${farm.name}`);
      console.log(`   - Crop: ${farm.cropType}`);
      console.log(`   - Soil: ${farm.soilType}`);
      console.log(`   - Size: ${farm.size} ${farm.unit}`);
      console.log(`   - Location: ${farm.location}`);
      console.log(`   - Sown: ${farm.sowingDate.toLocaleDateString()}`);
    });
    
    await mongoose.connection.close();
    console.log('\n✅ Done!');
  })
  .catch(err => {
    console.error('❌ Error:', err);
    process.exit(1);
  });
