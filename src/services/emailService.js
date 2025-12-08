const nodemailer = require('nodemailer');

// Create transporter
const createTransporter = () => {
  // For development, you can use a service like Gmail or a testing service like Ethereal
  // For production, use a proper email service like SendGrid, AWS SES, etc.
  
  if (process.env.EMAIL_SERVICE === 'gmail') {
    return nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASSWORD // Use App Password for Gmail
      }
    });
  }
  
  // Default SMTP configuration
  return nodemailer.createTransport({
    host: process.env.SMTP_HOST || 'smtp.gmail.com',
    port: process.env.SMTP_PORT || 587,
    secure: process.env.SMTP_SECURE === 'true', // true for 465, false for other ports
    auth: {
      user: process.env.EMAIL_USER,
      pass: process.env.EMAIL_PASSWORD
    }
  });
};

const sendOTPEmail = async (email, otp) => {
  try {
    const transporter = createTransporter();

    const mailOptions = {
      from: `"AgriCure" <${process.env.EMAIL_USER}>`,
      to: email,
      subject: 'Verify Your Email - AgriCure',
      html: `
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Email Verification</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
          <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f4f4; padding: 20px;">
            <tr>
              <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                  <!-- Header -->
                  <tr>
                    <td style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 40px 20px; text-align: center;">
                      <h1 style="color: #ffffff; margin: 0; font-size: 28px;">AgriCure</h1>
                      <p style="color: #ffffff; margin: 10px 0 0 0; font-size: 16px;">Email Verification</p>
                    </td>
                  </tr>
                  
                  <!-- Content -->
                  <tr>
                    <td style="padding: 40px 30px;">
                      <h2 style="color: #333333; margin: 0 0 20px 0; font-size: 24px;">Verify Your Email Address</h2>
                      <p style="color: #666666; line-height: 1.6; margin: 0 0 20px 0; font-size: 16px;">
                        Thank you for signing up with AgriCure! To complete your registration, please use the following One-Time Password (OTP):
                      </p>
                      
                      <!-- OTP Box -->
                      <table width="100%" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                          <td align="center" style="padding: 20px 0;">
                            <div style="background-color: #f0fdf4; border: 2px solid #10b981; border-radius: 8px; padding: 20px; display: inline-block;">
                              <span style="font-size: 36px; font-weight: bold; color: #10b981; letter-spacing: 8px;">${otp}</span>
                            </div>
                          </td>
                        </tr>
                      </table>
                      
                      <p style="color: #666666; line-height: 1.6; margin: 20px 0; font-size: 16px;">
                        This OTP will expire in <strong>1 minutes</strong>. Please do not share this code with anyone.
                      </p>
                      
                      <p style="color: #666666; line-height: 1.6; margin: 20px 0 0 0; font-size: 14px;">
                        If you didn't request this verification, please ignore this email.
                      </p>
                    </td>
                  </tr>
                  
                  <!-- Footer -->
                  <tr>
                    <td style="background-color: #f9fafb; padding: 30px; text-align: center; border-top: 1px solid #e5e7eb;">
                      <p style="color: #9ca3af; margin: 0; font-size: 14px;">
                        © ${new Date().getFullYear()} AgriCure. All rights reserved.
                      </p>
                      <p style="color: #9ca3af; margin: 10px 0 0 0; font-size: 12px;">
                        This is an automated email, please do not reply.
                      </p>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
      `
    };

    const info = await transporter.sendMail(mailOptions);
    console.log('📧 OTP email sent:', info.messageId);
    return { success: true, messageId: info.messageId };
  } catch (error) {
    console.error('❌ Error sending OTP email:', error);
    throw new Error('Failed to send OTP email');
  }
};

module.exports = {
  sendOTPEmail
};
