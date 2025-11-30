# Farm Database Schema Documentation

## Overview

The `farms` table stores all farm/field information submitted by users through the "Add Farm" form. Each farm is associated with a user and includes comprehensive location, crop, and soil data.

## Database Structure

### Table: `farms`

| Column Name   | Data Type      | Constraints                                                                  | Description                            | Form Field                                  |
| ------------- | -------------- | ---------------------------------------------------------------------------- | -------------------------------------- | ------------------------------------------- |
| `id`          | UUID           | PRIMARY KEY, DEFAULT gen_random_uuid()                                       | Unique identifier for each farm        | Auto-generated                              |
| `user_id`     | UUID           | NOT NULL, REFERENCES user_profiles(id) ON DELETE CASCADE                     | Owner of the farm                      | Auto-detected from auth                     |
| `name`        | TEXT           | NOT NULL                                                                     | Name of the farm/field                 | **Field Name**                              |
| `size`        | NUMERIC        | NOT NULL, CHECK (size > 0)                                                   | Size of the farm                       | **Field Size**                              |
| `unit`        | TEXT           | NOT NULL, DEFAULT 'hectares', CHECK (unit IN ('hectares', 'acres', 'bigha')) | Unit of measurement                    | **Unit** dropdown                           |
| `crop_type`   | TEXT           | NOT NULL                                                                     | Type of crop being grown               | **Crop Type** dropdown                      |
| `soil_type`   | TEXT           | NOT NULL                                                                     | Type of soil (auto-detected or manual) | **Soil Type (Auto-detected)**               |
| `location`    | TEXT           | NULL                                                                         | Human-readable location name/address   | Part of **Location & Soil Detection**       |
| `latitude`    | DECIMAL(10, 8) | NULL                                                                         | GPS latitude coordinate                | From **Get My Location & Soil Type** button |
| `longitude`   | DECIMAL(11, 8) | NULL                                                                         | GPS longitude coordinate               | From **Get My Location & Soil Type** button |
| `soil_data`   | JSONB          | NULL                                                                         | Detailed soil properties from API      | From soil detection API                     |
| `sowing_date` | DATE           | NULL                                                                         | Date when crop was sown/planted        | **Sowing Date**                             |
| `created_at`  | TIMESTAMPTZ    | DEFAULT now()                                                                | Record creation timestamp              | Auto-generated                              |
| `updated_at`  | TIMESTAMPTZ    | DEFAULT now()                                                                | Last update timestamp                  | Auto-updated                                |

## Form Field Mapping

### 1. Field Name \*

- **Database Column:** `name`
- **Type:** TEXT, NOT NULL
- **Validation:** Required
- **Example:** "North Field", "East Paddy Field"

### 2. Field Size \*

- **Database Column:** `size`
- **Type:** NUMERIC, NOT NULL
- **Validation:** Must be > 0
- **Example:** 2.5, 10, 0.75

### 3. Unit

- **Database Column:** `unit`
- **Type:** TEXT, NOT NULL
- **Allowed Values:** 'hectares', 'acres', 'bigha'
- **Default:** 'hectares'
- **Example:** "Hectares"

### 4. Crop Type \*

- **Database Column:** `crop_type`
- **Type:** TEXT, NOT NULL
- **Validation:** Required, selected from dropdown
- **Example:** "Rice", "Wheat", "Cotton", "Sugarcane"

### 5. Soil Type (Auto-detected) \*

- **Database Column:** `soil_type`
- **Type:** TEXT, NOT NULL
- **Population:** Auto-filled after clicking "Get My Location & Soil Type" button
- **Example:** "Loamy", "Clay", "Sandy", "Red Soil", "Black Soil"

### 6. Location & Soil Detection \*

- **Button Action:** "Get My Location & Soil Type"
- **Database Columns Populated:**
  - `latitude` - GPS latitude coordinate
  - `longitude` - GPS longitude coordinate
  - `location` - Human-readable address/location name
  - `soil_type` - Auto-detected soil type
  - `soil_data` - Detailed soil properties (JSON)
- **Process:**
  1. Browser requests user's GPS coordinates
  2. Backend calls soil detection API with coordinates
  3. Returns soil type and detailed soil data
  4. Populates form and database fields

### 7. Sowing Date \*

- **Database Column:** `sowing_date`
- **Type:** DATE
- **Format:** dd-mm-yyyy
- **Validation:** Required, must be a valid date
- **Description:** The date when the crop was sowed/planted
- **Example:** "15-10-2024"

## Indexes

```sql
-- Primary key index (automatic)
PRIMARY KEY (id)

-- User lookup index (automatic from foreign key)
FOREIGN KEY (user_id) REFERENCES user_profiles(id)

-- Location-based queries
CREATE INDEX idx_farms_location ON farms(latitude, longitude);

-- Sowing date queries
CREATE INDEX idx_farms_sowing_date ON farms(sowing_date);

-- Soil data JSON queries
CREATE INDEX idx_farms_soil_data ON farms USING GIN(soil_data);
```

## Row Level Security (RLS)

The table has RLS enabled with the following policies:

1. **Read Policy:** Users can only view their own farms

   ```sql
   user_id = (SELECT id FROM user_profiles WHERE id = auth.uid())
   ```

2. **Insert Policy:** Users can only create farms for themselves

   ```sql
   user_id = (SELECT id FROM user_profiles WHERE id = auth.uid())
   ```

3. **Update Policy:** Users can only update their own farms

   ```sql
   user_id = (SELECT id FROM user_profiles WHERE id = auth.uid())
   ```

4. **Delete Policy:** Users can only delete their own farms
   ```sql
   user_id = (SELECT id FROM user_profiles WHERE id = auth.uid())
   ```

## Sample Data Structure

### Example Insert Query

```sql
INSERT INTO farms (
  user_id,
  name,
  size,
  unit,
  crop_type,
  soil_type,
  location,
  latitude,
  longitude,
  soil_data,
  sowing_date
) VALUES (
  'user-uuid-here',
  'North Field',
  2.5,
  'hectares',
  'Rice',
  'Loamy',
  'Pune, Maharashtra, India',
  18.5204,
  73.8567,
  '{
    "ph": 6.5,
    "nitrogen": 45,
    "phosphorus": 30,
    "potassium": 35,
    "organic_carbon": 0.8,
    "moisture": 22,
    "texture": "loamy"
  }'::jsonb,
  '2024-06-15'
);
```

### Example Complete Record

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user-uuid-here",
  "name": "North Field",
  "size": 2.5,
  "unit": "hectares",
  "crop_type": "Rice",
  "soil_type": "Loamy",
  "location": "Pune, Maharashtra, India",
  "latitude": 18.5204,
  "longitude": 73.8567,
  "soil_data": {
    "ph": 6.5,
    "nitrogen": 45,
    "phosphorus": 30,
    "potassium": 35,
    "organic_carbon": 0.8,
    "moisture": 22,
    "texture": "loamy",
    "detected_via": "soil_prediction_api",
    "confidence": 0.92
  },
  "sowing_date": "2024-06-15",
  "created_at": "2024-06-15T10:30:00Z",
  "updated_at": "2024-06-15T10:30:00Z"
}
```

## Migration Files

The complete schema was created through these migrations:

1. **20250812123452_tiny_wood.sql** - Initial farms table creation

   - Core fields: id, user_id, name, size, unit, crop_type, soil_type, location
   - RLS policies
   - Timestamps

2. **20240820_add_location_soil_data.sql** - Added GPS and soil data

   - latitude, longitude columns
   - soil_data JSONB column
   - Location and soil data indexes

3. **20250830032616_gentle_dream.sql** - Added sowing date
   - sowing_date DATE column
   - Sowing date index

## API Endpoints (Reference)

The following API endpoints should interact with this table:

- `POST /api/farms` - Create new farm
- `GET /api/farms` - List user's farms
- `GET /api/farms/:id` - Get specific farm details
- `PUT /api/farms/:id` - Update farm information
- `DELETE /api/farms/:id` - Delete farm
- `POST /api/farms/detect-soil` - Auto-detect soil type from coordinates

## Notes

1. All fields marked with `*` in the form are required (NOT NULL in database)
2. The "Get My Location & Soil Type" button populates multiple fields simultaneously
3. Soil detection uses the backend ML model at `/api/farms/detect-soil`
4. The `soil_data` JSONB field can store any additional soil properties from the API
5. Location can be null if user doesn't want to share GPS coordinates
6. Users must own a farm (via user_id) to view/edit it due to RLS policies

## Validation Rules

### Frontend Validation

- Field Name: Required, non-empty string
- Field Size: Required, must be a positive number
- Unit: Required, one of predefined options
- Crop Type: Required, selected from dropdown
- Soil Type: Required, auto-populated or manually selected
- Location Detection: Required to click button before saving
- Sowing Date: Required, valid date in dd-mm-yyyy format

### Database Constraints

- size > 0
- unit IN ('hectares', 'acres', 'bigha')
- user_id must reference valid user_profiles.id
- All TEXT fields with NOT NULL must have values
