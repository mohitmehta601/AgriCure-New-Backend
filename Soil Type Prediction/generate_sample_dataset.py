# generate_sample_dataset.py
# Creates a realistic India soil dataset for testing

import pandas as pd
import numpy as np

np.random.seed(42)

# Define soil types and their typical characteristics in India
soil_types = {
    "Alluvial": {
        "lat_range": (20, 30),
        "lon_range": (75, 88),
        "elevation_range": (0, 300),
        "rainfall_range": (600, 1500),
        "temp_range": (22, 30),
        "aridity_range": (0.4, 0.7),
        "dist_river_range": (0, 20),
        "dist_coast_range": (100, 1000),
        "ndvi_range": (0.4, 0.7),
        "landcovers": ["cropland", "rice_paddy", "mixed_agriculture"],
        "geologies": ["alluvium", "sedimentary", "fluvial"]
    },
    "Black": {
        "lat_range": (15, 25),
        "lon_range": (72, 82),
        "elevation_range": (300, 700),
        "rainfall_range": (600, 1000),
        "temp_range": (24, 32),
        "aridity_range": (0.3, 0.6),
        "dist_river_range": (5, 50),
        "dist_coast_range": (200, 800),
        "ndvi_range": (0.3, 0.6),
        "landcovers": ["cropland", "cotton_field", "mixed_agriculture"],
        "geologies": ["basalt", "volcanic", "deccan_trap"]
    },
    "Red": {
        "lat_range": (12, 20),
        "lon_range": (74, 85),
        "elevation_range": (400, 900),
        "rainfall_range": (700, 1200),
        "temp_range": (23, 29),
        "aridity_range": (0.4, 0.7),
        "dist_river_range": (10, 60),
        "dist_coast_range": (50, 600),
        "ndvi_range": (0.35, 0.65),
        "landcovers": ["cropland", "forest", "plantation"],
        "geologies": ["granite", "gneiss", "metamorphic"]
    },
    "Laterite": {
        "lat_range": (8, 16),
        "lon_range": (73, 88),
        "elevation_range": (100, 600),
        "rainfall_range": (1500, 3000),
        "temp_range": (25, 32),
        "aridity_range": (0.6, 0.9),
        "dist_river_range": (5, 40),
        "dist_coast_range": (10, 300),
        "ndvi_range": (0.5, 0.8),
        "landcovers": ["forest", "plantation", "tropical_forest"],
        "geologies": ["laterite", "weathered_rock", "tropical_soil"]
    },
    "Arid": {
        "lat_range": (24, 32),
        "lon_range": (68, 76),
        "elevation_range": (100, 500),
        "rainfall_range": (100, 400),
        "temp_range": (26, 35),
        "aridity_range": (0.05, 0.3),
        "dist_river_range": (30, 150),
        "dist_coast_range": (300, 1200),
        "ndvi_range": (0.1, 0.3),
        "landcovers": ["desert", "scrubland", "barren"],
        "geologies": ["sandstone", "aeolian", "desert_sand"]
    },
    "Clayey": {
        "lat_range": (18, 26),
        "lon_range": (76, 86),
        "elevation_range": (200, 600),
        "rainfall_range": (800, 1400),
        "temp_range": (23, 30),
        "aridity_range": (0.4, 0.7),
        "dist_river_range": (5, 35),
        "dist_coast_range": (150, 700),
        "ndvi_range": (0.35, 0.65),
        "landcovers": ["cropland", "mixed_agriculture", "grassland"],
        "geologies": ["clay", "alluvium", "sedimentary"]
    },
    "Alkaline": {
        "lat_range": (26, 32),
        "lon_range": (72, 78),
        "elevation_range": (150, 400),
        "rainfall_range": (200, 600),
        "temp_range": (25, 34),
        "aridity_range": (0.2, 0.5),
        "dist_river_range": (15, 80),
        "dist_coast_range": (400, 1000),
        "ndvi_range": (0.15, 0.4),
        "landcovers": ["scrubland", "grassland", "semi_arid"],
        "geologies": ["saline", "alkaline", "evaporite"]
    }
}

# Generate samples for each soil type
samples_per_type = 200
data = []

for soil_type, characteristics in soil_types.items():
    for _ in range(samples_per_type):
        sample = {
            "lat": np.random.uniform(*characteristics["lat_range"]),
            "lon": np.random.uniform(*characteristics["lon_range"]),
            "elevation": np.random.uniform(*characteristics["elevation_range"]),
            "rainfall": np.random.uniform(*characteristics["rainfall_range"]),
            "temperature": np.random.uniform(*characteristics["temp_range"]),
            "aridity_index": np.random.uniform(*characteristics["aridity_range"]),
            "dist_river_km": np.random.uniform(*characteristics["dist_river_range"]),
            "dist_coast_km": np.random.uniform(*characteristics["dist_coast_range"]),
            "ndvi": np.random.uniform(*characteristics["ndvi_range"]),
            "landcover": np.random.choice(characteristics["landcovers"]),
            "geology": np.random.choice(characteristics["geologies"]),
            "soil_type": soil_type
        }
        data.append(sample)

# Create DataFrame
df = pd.DataFrame(data)

# Shuffle the dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to CSV
output_file = "india_soil_dataset.csv"
df.to_csv(output_file, index=False)

print(f"✓ Generated {len(df)} samples across {len(soil_types)} soil types")
print(f"✓ Dataset saved to: {output_file}")
print(f"\nSoil type distribution:")
print(df['soil_type'].value_counts().sort_index())
print(f"\nDataset shape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head())
