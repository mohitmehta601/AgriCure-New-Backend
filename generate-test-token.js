// Test API endpoint with authentication
require('dotenv').config();
const express = require('express');
const jwt = require('jsonwebtoken');

// Generate a test token for the user
const userId = '692c10a3ca94322e73ab32f9';
const token = jwt.sign(
  { userId: userId, email: 'g.mehta1971@gmail.com' },
  process.env.JWT_SECRET || 'your-secret-key-change-this-in-production',
  { expiresIn: '7d' }
);

console.log('Test Token:', token);
console.log('\nUser ID:', userId);

console.log('\n📝 To test in browser console:');
console.log('1. Open browser DevTools (F12)');
console.log('2. Go to Console tab');
console.log('3. Run this:');
console.log(`
localStorage.setItem('auth_token', '${token}');
location.reload();
`);

console.log('\n🔗 Test API directly with curl:');
console.log(`
curl -H "Authorization: Bearer ${token}" http://localhost:3000/api/farms/user/${userId}
`);
