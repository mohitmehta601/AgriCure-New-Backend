# Email OTP Verification Setup Guide

## Overview

Email OTP (One-Time Password) verification has been integrated into the signup flow. Users must verify their email address before completing registration.

## How It Works

### User Flow

1. User fills out the signup form with their details
2. Backend validates the data and sends a 6-digit OTP to the user's email
3. User receives the OTP email and enters the code on the verification page
4. Backend verifies the OTP and creates the user account
5. User is redirected to login

### Security Features

- OTPs expire after 10 minutes
- Pending user data expires after 1 hour
- Product keys are validated but not consumed until OTP verification
- Email uniqueness is enforced
- Password hashing is maintained

## Backend Implementation

### New Files Created

1. **`src/models/OTP.js`**

   - Stores OTP codes with email
   - Auto-expires after 10 minutes using MongoDB TTL index
   - Tracks verification status

2. **`src/models/PendingUser.js`**

   - Temporarily stores user registration data
   - Auto-expires after 1 hour
   - Password is hashed before storage

3. **`src/services/emailService.js`**
   - Handles email sending via nodemailer
   - Beautiful HTML email template
   - Configurable for Gmail or custom SMTP

### Updated Files

4. **`src/routes/auth.js`**
   - Modified `/signup` endpoint to send OTP instead of creating user immediately
   - Added `/verify-otp` endpoint for OTP verification
   - Added `/resend-otp` endpoint for OTP resending

### API Endpoints

#### POST /auth/signup

Initiates signup and sends OTP to email.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "fullName": "John Doe",
  "productKey": "ABC123XYZ",
  "phoneNumber": "+91 1234567890"
}
```

**Response:**

```json
{
  "message": "OTP sent to your email. Please verify to complete registration.",
  "email": "user@example.com"
}
```

#### POST /auth/verify-otp

Verifies OTP and completes user registration.

**Request Body:**

```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

**Response:**

```json
{
  "message": "Email verified successfully! Account created.",
  "token": "jwt-token-here",
  "user": {
    "id": "user-id",
    "email": "user@example.com",
    "fullName": "John Doe",
    "phoneNumber": "+91 1234567890",
    "productId": "product-id",
    "productName": "Product Name"
  }
}
```

#### POST /auth/resend-otp

Resends OTP to email.

**Request Body:**

```json
{
  "email": "user@example.com"
}
```

**Response:**

```json
{
  "message": "OTP resent successfully"
}
```

## Frontend Implementation

### New Files Created

1. **`src/pages/VerifyOTP.tsx`**
   - OTP input interface with 6 digit boxes
   - Auto-focus and auto-submit functionality
   - Resend OTP with 60-second countdown timer
   - Paste support for OTP codes

### Updated Files

2. **`src/pages/Signup.tsx`**

   - Modified to show OTP verification page after signup
   - State management for OTP flow

3. **`src/services/authService.ts`**
   - Updated `signUp()` to handle OTP response
   - Added `verifyOTP()` method
   - Added `resendOTP()` method

## Email Configuration

### Environment Variables

Add these to your `.env` file:

```env
# Email Configuration for OTP
EMAIL_SERVICE=gmail
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### Gmail Setup (Recommended for Development)

1. **Enable 2-Step Verification:**

   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Create App Password:**

   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Name it "AgriCure OTP"
   - Copy the 16-character password
   - Use this as `EMAIL_PASSWORD` in .env

3. **Update .env:**

```env
EMAIL_SERVICE=gmail
EMAIL_USER=your-gmail@gmail.com
EMAIL_PASSWORD=your-16-char-app-password
```

### Custom SMTP Setup (Production)

For production, use a dedicated email service like SendGrid, AWS SES, or Mailgun:

```env
EMAIL_SERVICE=smtp
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_SECURE=false
EMAIL_USER=noreply@yourdomain.com
EMAIL_PASSWORD=your-smtp-password
```

### Ethereal Email (Testing Only)

For testing without real emails, use Ethereal:

1. Go to https://ethereal.email/
2. Create a test account
3. Use the provided SMTP credentials

## Testing

### Manual Testing

1. **Start the backend server:**

   ```powershell
   cd Backend
   npm start
   ```

2. **Start the frontend:**

   ```powershell
   cd Frontend
   npm run dev
   ```

3. **Test the flow:**
   - Go to signup page
   - Fill in all details
   - Submit the form
   - Check email for OTP (or terminal logs if using test service)
   - Enter OTP on verification page
   - Should redirect to login after success

### API Testing with curl

**Signup:**

```powershell
curl -X POST http://localhost:3000/api/auth/signup `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "fullName": "Test User",
    "productKey": "valid-product-key",
    "phoneNumber": "+91 1234567890"
  }'
```

**Verify OTP:**

```powershell
curl -X POST http://localhost:3000/api/auth/verify-otp `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com",
    "otp": "123456"
  }'
```

**Resend OTP:**

```powershell
curl -X POST http://localhost:3000/api/auth/resend-otp `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com"
  }'
```

## Error Handling

### Common Errors

1. **"Failed to send verification email"**

   - Check email credentials in .env
   - Verify Gmail app password is correct
   - Check internet connection

2. **"Invalid or expired OTP"**

   - OTP expires after 10 minutes
   - User can request a new OTP
   - Check OTP was entered correctly

3. **"User data not found. Please sign up again."**

   - Pending user data expired (1 hour limit)
   - User needs to start signup process again

4. **"Invalid or already used product key"**
   - Product key already consumed
   - Product key doesn't exist
   - Check product key is valid

## Database Collections

### otps

```javascript
{
  email: "user@example.com",
  otp: "123456",
  verified: false,
  createdAt: ISODate("2025-12-08T..."),
  // Auto-deletes after 10 minutes
}
```

### pendingusers

```javascript
{
  email: "user@example.com",
  password: "hashed-password",
  fullName: "John Doe",
  phoneNumber: "+91 1234567890",
  productKey: "ABC123XYZ",
  createdAt: ISODate("2025-12-08T..."),
  // Auto-deletes after 1 hour
}
```

## Security Considerations

1. **Rate Limiting:** Consider adding rate limiting to prevent OTP spam
2. **IP Tracking:** Track failed OTP attempts by IP
3. **Email Validation:** Implement additional email validation
4. **Captcha:** Add CAPTCHA to signup form to prevent bots
5. **Production Emails:** Use dedicated email service (SendGrid, AWS SES) in production

## UI/UX Features

### OTP Input

- 6 separate input boxes for better UX
- Auto-focus next box after entering digit
- Backspace navigates to previous box
- Paste support (ctrl+v)
- Mobile-friendly numeric keyboard

### Timer

- 60-second countdown before resend
- Visual feedback for waiting time
- Automatic unlock after countdown

### Email Template

- Branded AgriCure design
- Clear OTP display with large font
- Mobile-responsive HTML
- Professional appearance

## Troubleshooting

### OTP Not Received

1. Check spam/junk folder
2. Verify email address is correct
3. Check backend logs for email errors
4. Test SMTP connection

### Backend Errors

1. Check MongoDB connection
2. Verify environment variables
3. Check nodemailer configuration
4. Review server logs

### Frontend Issues

1. Clear browser cache
2. Check API endpoint URLs
3. Verify token storage
4. Check network requests in DevTools

## Future Enhancements

- [ ] SMS OTP option
- [ ] Rate limiting for OTP requests
- [ ] Email verification link as alternative
- [ ] Remember device functionality
- [ ] Admin panel for OTP monitoring
- [ ] Email templates customization
- [ ] Multi-language email support

## Dependencies Added

```json
{
  "nodemailer": "^6.9.x"
}
```

## Deployment Notes

### Production Checklist

1. ✅ Update email credentials in production .env
2. ✅ Use dedicated email service (not Gmail)
3. ✅ Enable rate limiting
4. ✅ Configure proper CORS settings
5. ✅ Set up email monitoring
6. ✅ Test email deliverability
7. ✅ Configure SPF/DKIM records for domain
8. ✅ Set up error alerting

### Environment Variables Required

```env
# Required for OTP functionality
EMAIL_SERVICE=gmail
EMAIL_USER=
EMAIL_PASSWORD=

# Optional for custom SMTP
SMTP_HOST=
SMTP_PORT=
SMTP_SECURE=
```

## Support

If you encounter any issues:

1. Check this documentation
2. Review error messages in console/logs
3. Verify all environment variables
4. Test with a different email address
5. Check MongoDB connection and collections

---

**Created:** December 8, 2025  
**Author:** GitHub Copilot  
**Version:** 1.0
