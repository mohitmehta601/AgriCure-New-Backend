// Test Email OTP Setup
// This script tests if email configuration is working correctly

require('dotenv').config();
const { sendOTPEmail } = require('./src/services/emailService');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

console.log('\n==================================');
console.log('  Email OTP Configuration Test');
console.log('==================================\n');

// Check if email environment variables are set
console.log('Checking environment variables...\n');

const checks = [
  { name: 'EMAIL_USER', value: process.env.EMAIL_USER },
  { name: 'EMAIL_PASSWORD', value: process.env.EMAIL_PASSWORD },
  { name: 'EMAIL_SERVICE', value: process.env.EMAIL_SERVICE }
];

let allConfigured = true;

checks.forEach(check => {
  if (check.value) {
    console.log(`✅ ${check.name}: ${check.name === 'EMAIL_PASSWORD' ? '****' : check.value}`);
  } else {
    console.log(`❌ ${check.name}: Not set`);
    allConfigured = false;
  }
});

if (!allConfigured) {
  console.log('\n⚠️  Some email configuration variables are missing!');
  console.log('Please run: node setup-email-otp.ps1');
  console.log('Or manually edit the .env file\n');
  rl.close();
  process.exit(1);
}

console.log('\n✅ All email configuration variables are set!\n');

// Ask if user wants to send a test email
rl.question('Do you want to send a test OTP email? (y/n): ', async (answer) => {
  if (answer.toLowerCase() !== 'y') {
    console.log('\nTest cancelled.\n');
    rl.close();
    return;
  }

  rl.question('Enter email address to send test OTP: ', async (email) => {
    console.log(`\nSending test OTP to: ${email}...`);
    
    try {
      const testOTP = '123456';
      const result = await sendOTPEmail(email, testOTP);
      
      console.log('\n✅ Test email sent successfully!');
      console.log(`Message ID: ${result.messageId}`);
      console.log(`\nPlease check the inbox of: ${email}`);
      console.log('Test OTP code: 123456\n');
      
      if (process.env.EMAIL_SERVICE === 'gmail') {
        console.log('Note: Check your spam folder if you don\'t see the email.');
      }
      
    } catch (error) {
      console.log('\n❌ Failed to send test email!');
      console.log(`Error: ${error.message}\n`);
      
      if (error.message.includes('Invalid login')) {
        console.log('Troubleshooting tips:');
        console.log('1. For Gmail: Make sure you\'re using an App Password, not your regular password');
        console.log('2. Enable 2-Step Verification at: https://myaccount.google.com/security');
        console.log('3. Generate App Password at: https://myaccount.google.com/apppasswords');
        console.log('4. Use the 16-character App Password in your .env file\n');
      } else if (error.message.includes('ECONNREFUSED')) {
        console.log('Troubleshooting tips:');
        console.log('1. Check your internet connection');
        console.log('2. Verify SMTP_HOST and SMTP_PORT are correct');
        console.log('3. Check if firewall is blocking the connection\n');
      } else {
        console.log('Please check your email configuration in .env file\n');
      }
    }
    
    rl.close();
  });
});
