# User Schema Migration Guide

## Overview

This migration script updates the User collection to match the new schema requirements:

- Adds default `phoneNumber` to users who don't have one
- Removes deprecated fields: `farmLocation`, `farmSize`, `farmSizeUnit`

## Prerequisites

- Node.js installed
- MongoDB running and accessible
- `.env` file configured with `MONGODB_URI` or `DATABASE_URL`

## How to Run the Migration

### Step 1: Backup Your Database (Important!)

Before running any migration, always backup your database:

```bash
# For MongoDB Atlas: Use the Atlas backup feature

# For local MongoDB:
mongodump --uri="your_mongodb_connection_string" --out=./backup
```

### Step 2: Run the Migration Script

```bash
# Navigate to Backend folder
cd Backend

# Run the migration
node migrate-user-schema.js
```

### Step 3: Verify the Migration

The script will output:

- Number of users found
- Which users were updated
- Which fields were added/removed
- Summary statistics

### Step 4: Update User Phone Numbers

After migration, users with the default phone number `+91 0000000000` should update their phone numbers via the Edit Profile page.

## What the Script Does

1. **Connects to MongoDB** using your environment variables
2. **Scans all users** in the database
3. **For each user:**
   - Adds `phoneNumber: '+91 0000000000'` if missing
   - Removes `farmLocation` field if present
   - Removes `farmSize` field if present
   - Removes `farmSizeUnit` field if present
4. **Provides detailed logging** of each operation
5. **Shows summary** of updates, skips, and errors

## Rollback (If Needed)

If you need to rollback the migration:

```bash
# Restore from backup
mongorestore --uri="your_mongodb_connection_string" ./backup
```

## Important Notes

- ⚠️ **Always backup before migrating**
- The script is idempotent (safe to run multiple times)
- Users will need to update their phone numbers from the default placeholder
- New signups will require phone number from the start

## Troubleshooting

**Error: Cannot connect to MongoDB**

- Check your `.env` file has correct `MONGODB_URI` or `DATABASE_URL`
- Ensure MongoDB is running

**Error: Permission denied**

- Ensure your MongoDB user has write permissions
- Check your connection string includes authentication

**Some users not updated**

- Check the error messages in the output
- Verify the user documents exist in the database
