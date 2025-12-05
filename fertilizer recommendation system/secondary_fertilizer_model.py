"""
Secondary Fertilizer (Micronutrient) Recommendation Model
This model predicts micronutrient fertilizer requirements based on soil parameters and crop type.
Uses dataset-based lookup with rule-based validation.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import os


class SecondaryFertilizerModel:
    """
    Model to predict secondary fertilizer (micronutrient) requirements
    based on soil conditions and crop type using dataset lookup.
    """
    
    def __init__(self, dataset_path: str = None):
        """Initialize the model with dataset and crop-specific micronutrient requirements."""
        
        # Load the dataset
        if dataset_path is None:
            dataset_path = os.path.join(os.path.dirname(__file__), 'Secondary_fertilizer_dataset.csv')
        
        try:
            self.dataset = pd.read_csv(dataset_path)
            print(f"✓ Dataset loaded successfully: {len(self.dataset)} records")
        except FileNotFoundError:
            print(f"⚠ Warning: Dataset file not found at '{dataset_path}'. Using rule-based mode only.")
            self.dataset = None
        except Exception as e:
            print(f"⚠ Error loading dataset: {e}. Using rule-based mode only.")
            self.dataset = None
        
        # Crop-wise micronutrient requirements mapping
        self.crop_micronutrients = {
            'Rice': ['Zn', 'Fe', 'Mn', 'Cu', 'B', 'Mo'],
            'Wheat': ['Zn', 'Fe', 'Mn', 'Cu', 'B', 'Mo'],
            'Maize': ['Zn', 'Fe', 'Mn', 'Cu', 'B', 'Mo'],
            'Barley': ['Zn', 'Fe', 'Mn', 'Cu', 'B', 'Mo'],
            'Jowar': ['Fe', 'Zn', 'Mn', 'Cu', 'B'],
            'Sorghum': ['Fe', 'Zn', 'Mn', 'Cu', 'B'],
            'Bajra': ['Fe', 'Zn', 'Mn', 'Cu', 'B'],
            'Pearl Millet': ['Fe', 'Zn', 'Mn', 'Cu', 'B'],
            'Ragi': ['Zn', 'Fe', 'Mn', 'Cu', 'B'],
            'Finger Millet': ['Zn', 'Fe', 'Mn', 'Cu', 'B'],
            'Groundnut': ['Ca', 'B', 'Mn', 'Fe', 'Zn', 'Mo'],
            'Mustard': ['B', 'Mo', 'Mn', 'Zn', 'Fe'],
            'Soybean': ['Fe', 'Mo', 'Zn', 'Mn', 'B', 'Cu'],
            'Sugarcane': ['Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo'],
            'Cotton': ['B', 'Zn', 'Mn', 'Fe', 'Cu', 'Mo'],
            'Chickpea': ['Zn', 'Fe', 'B', 'Mo', 'Mn'],
            'Gram': ['Zn', 'Fe', 'B', 'Mo', 'Mn'],
            'Moong': ['Mo', 'Zn', 'Fe', 'Mn', 'B'],
            'Green Gram': ['Mo', 'Zn', 'Fe', 'Mn', 'B'],
            'Garlic': ['Zn', 'Fe', 'Mn', 'B', 'Cu', 'Mo'],
            'Onion': ['Zn', 'B', 'Mn', 'Fe', 'Cu', 'Mo']
        }
        
        # Micronutrient to fertilizer mapping
        self.micronutrient_to_fertilizer = {
            'Zn': 'Zinc Sulphate',
            'Fe': 'Ferrous Sulphate',
            'B': 'Borax',
            'Mn': 'Manganese Sulphate',
            'Cu': 'Copper Sulphate',
            'Mo': 'Ammonium Molybdate',
            'Ca': 'Calcium Chloride',
            'Mg': 'Magnesium Sulphate',
            'Ni': 'Nickel Sulphate',
            'Cl': 'Potassium Chloride'
        }
        
        # Soil type mapping
        self.soil_types = ['Alluvial', 'Black', 'Red', 'Laterite', 'Desert', 'Mountain']
    
    def categorize_ph(self, pH: float) -> str:
        """
        Categorize pH value into ranges used in dataset.
        
        Ranges:
        - Acidic (<6.0)
        - Neutral (6.0-7.5)
        - Alkaline (>7.5)
        """
        if pH < 6.0:
            return "Acidic (<6.0)"
        elif 6.0 <= pH <= 7.5:
            return "Neutral (6.0-7.5)"
        else:
            return "Alkaline (>7.5)"
    
    def categorize_ec(self, ec: float) -> str:
        """
        Categorize EC value into ranges used in dataset.
        
        Ranges (in µS/cm):
        - Low (<500)
        - Medium (500-2000)
        - High (>2000)
        """
        if ec < 500:
            return "Low (<500)"
        elif 500 <= ec <= 2000:
            return "Medium (500-2000)"
        else:
            return "High (>2000)"
    
    def get_deficiencies_from_dataset(self, 
                                     soil_type: str,
                                     ph_range: str,
                                     ec_range: str,
                                     crop_type: str) -> Optional[List[str]]:
        """
        Query dataset for micronutrient deficiencies based on soil and crop parameters.
        
        Parameters:
        -----------
        soil_type : str
            Soil type (e.g., 'Alluvial', 'Black', 'Red')
        ph_range : str
            pH range category
        ec_range : str
            EC range category
        crop_type : str
            Crop type
            
        Returns:
        --------
        List[str] or None
            List of deficient micronutrients or None if no match found
        """
        if self.dataset is None:
            return None
        
        # Normalize crop type to lowercase for matching
        crop_normalized = crop_type.strip().lower()
        
        # Query the dataset
        match = self.dataset[
            (self.dataset['Soil_Type'].str.lower() == soil_type.lower()) &
            (self.dataset['pH_Range'] == ph_range) &
            (self.dataset['EC_Range_µS_cm'] == ec_range) &
            (self.dataset['Crop_Type'].str.lower() == crop_normalized)
        ]
        
        if match.empty:
            return None
        
        # Extract deficiencies from status columns
        status_columns = ['Zn_Status', 'Fe_Status', 'Mn_Status', 'Cu_Status', 
                         'B_Status', 'Mo_Status', 'Cl_Status', 'Ni_Status']
        
        deficiencies = []
        for col in status_columns:
            if col in match.columns:
                status_value = match[col].values[0]
                if status_value == 'Low':
                    # Extract nutrient name (remove '_Status' suffix)
                    nutrient = col.replace('_Status', '')
                    deficiencies.append(nutrient)
        
        return deficiencies
    
    def identify_deficiencies_rule_based(self,
                                         nitrogen: float,
                                         phosphorus: float,
                                         potassium: float,
                                         pH: float,
                                         ec: float,
                                         moisture: float,
                                         temperature: float) -> List[str]:
        """
        Identify micronutrient deficiencies using rule-based logic (fallback method).
        
        Parameters:
        -----------
        nitrogen : float
            Nitrogen content in mg/kg
        phosphorus : float
            Phosphorus content in mg/kg
        potassium : float
            Potassium content in mg/kg
        pH : float
            Soil pH value
        ec : float
            Electrical Conductivity in µS/cm
        moisture : float
            Soil Moisture in %
        temperature : float
            Soil Temperature in °C
            
        Returns:
        --------
        List[str]
            List of deficient micronutrients
        """
        
        deficiencies = set()
        
        # Rule 1: pH > 7.5 + P > 40 mg/kg + N 100–250 mg/kg + K 100–300 mg/kg
        if (pH > 7.5 and phosphorus > 40 and 
            100 <= nitrogen <= 250 and 100 <= potassium <= 300):
            deficiencies.update(['Zn', 'Fe', 'Mn', 'Cu'])
        
        # Rule 2: pH < 5.5 + EC < 200 µS/cm
        if pH < 5.5 and ec < 200:
            deficiencies.update(['Mo', 'Ca', 'Mg'])
        
        # Rule 3: N > 300 mg/kg
        if nitrogen > 300:
            deficiencies.update(['Zn', 'Cu'])
        
        # Rule 4: K > 350 mg/kg + EC 250–750 µS/cm
        if potassium > 350 and 250 <= ec <= 750:
            deficiencies.add('Mg')
        
        # Rule 5: EC < 200 µS/cm + N < 100 mg/kg + Moisture < 15%
        if ec < 200 and nitrogen < 100 and moisture < 15:
            deficiencies.update(['Zn', 'Fe', 'B'])
        
        # Rule 6: Moisture < 12–15% + pH > 7.5
        if moisture < 15 and pH > 7.5:
            deficiencies.update(['B', 'Fe', 'Zn'])
        
        # Rule 7: Temperature < 15°C + pH > 7.5
        if temperature < 15 and pH > 7.5:
            deficiencies.add('Fe')
        
        # Additional rules based on pH ranges
        if pH > 7.5:  # Alkaline soils - common deficiencies
            deficiencies.update(['Zn', 'Fe', 'Mn'])
        
        if pH < 5.5:  # Acidic soils - common deficiencies
            deficiencies.update(['Mo', 'Ca'])
        
        # Additional rule for low EC (nutrient-poor soils)
        if ec < 200:
            deficiencies.update(['Zn', 'Fe'])
        
        return list(deficiencies)
    
    def identify_deficiencies(self, 
                            nitrogen: float,
                            phosphorus: float,
                            potassium: float,
                            pH: float,
                            ec: float,
                            moisture: float,
                            temperature: float,
                            crop_type: str,
                            soil_type: str = 'Alluvial') -> List[str]:
        """
        Identify micronutrient deficiencies using dataset-based lookup with rule-based fallback.
        
        Parameters:
        -----------
        nitrogen : float
            Nitrogen content in mg/kg
        phosphorus : float
            Phosphorus content in mg/kg
        potassium : float
            Potassium content in mg/kg
        pH : float
            Soil pH value
        ec : float
            Electrical Conductivity in µS/cm
        moisture : float
            Soil Moisture in %
        temperature : float
            Soil Temperature in °C
        crop_type : str
            Type of crop to be grown
        soil_type : str, optional
            Soil type (default: 'Alluvial')
            
        Returns:
        --------
        List[str]
            List of deficient micronutrients
        """
        
        # Step 1: Try dataset-based lookup first
        ph_range = self.categorize_ph(pH)
        ec_range = self.categorize_ec(ec)
        
        dataset_deficiencies = self.get_deficiencies_from_dataset(
            soil_type=soil_type,
            ph_range=ph_range,
            ec_range=ec_range,
            crop_type=crop_type
        )
        
        if dataset_deficiencies is not None:
            # Dataset match found - use it as primary source
            deficiencies = set(dataset_deficiencies)
            
            # Augment with rule-based logic for extreme conditions
            if temperature < 15 and pH > 7.5:
                deficiencies.add('Fe')
            
            if moisture < 12:
                deficiencies.add('B')
            
            if nitrogen > 300:
                deficiencies.update(['Zn', 'Cu'])
            
            if potassium > 350 and 250 <= ec <= 750:
                deficiencies.add('Mg')
        else:
            # No dataset match - use rule-based logic
            deficiencies = set(self.identify_deficiencies_rule_based(
                nitrogen=nitrogen,
                phosphorus=phosphorus,
                potassium=potassium,
                pH=pH,
                ec=ec,
                moisture=moisture,
                temperature=temperature
            ))
        
        # Filter deficiencies based on crop requirements
        crop_type_normalized = crop_type.strip().title()
        if crop_type_normalized in self.crop_micronutrients:
            crop_needs = set(self.crop_micronutrients[crop_type_normalized])
            # Return only deficiencies that the crop actually needs
            relevant_deficiencies = list(deficiencies & crop_needs)
        else:
            # If crop not found, return all detected deficiencies
            relevant_deficiencies = list(deficiencies)
        
        return relevant_deficiencies
    
    def recommend_fertilizer(self,
                           nitrogen: float,
                           phosphorus: float,
                           potassium: float,
                           crop_type: str,
                           pH: float,
                           ec: float,
                           moisture: float,
                           temperature: float,
                           soil_type: str = 'Alluvial') -> str:
        """
        Recommend secondary fertilizer based on input parameters using dataset lookup.
        
        Parameters:
        -----------
        nitrogen : float
            Nitrogen content in mg/kg
        phosphorus : float
            Phosphorus content in mg/kg
        potassium : float
            Potassium content in mg/kg
        crop_type : str
            Type of crop to be grown
        pH : float
            Soil pH value
        ec : float
            Electrical Conductivity in µS/cm
        moisture : float
            Soil Moisture in %
        temperature : float
            Soil Temperature in °C
        soil_type : str, optional
            Soil type (default: 'Alluvial')
            
        Returns:
        --------
        str
            Recommended fertilizer(s) in format "Fertilizer1 + Fertilizer2 + ..."
        """
        
        # Identify deficiencies using dataset-based lookup
        deficiencies = self.identify_deficiencies(
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            pH=pH,
            ec=ec,
            moisture=moisture,
            temperature=temperature,
            crop_type=crop_type,
            soil_type=soil_type
        )
        
        if not deficiencies:
            return "No Secondary Fertilizer Required"
        
        # Map micronutrients to fertilizers
        fertilizers = []
        for nutrient in deficiencies:
            if nutrient in self.micronutrient_to_fertilizer:
                fertilizers.append(self.micronutrient_to_fertilizer[nutrient])
        
        # Sort fertilizers for consistent output
        fertilizers = sorted(set(fertilizers))
        
        return " + ".join(fertilizers)
    
    def predict(self, input_data: Dict) -> str:
        """
        Predict secondary fertilizer requirement from input dictionary.
        
        Parameters:
        -----------
        input_data : dict
            Dictionary containing soil and crop parameters
            
        Returns:
        --------
        str
            Recommended fertilizer(s)
        """
        
        return self.recommend_fertilizer(
            nitrogen=input_data.get('Nitrogen', 0),
            phosphorus=input_data.get('Phosphorus', 0),
            potassium=input_data.get('Potassium', 0),
            crop_type=input_data.get('Crop_Type', ''),
            pH=input_data.get('pH', 7.0),
            ec=input_data.get('Electrical_Conductivity', 0),
            moisture=input_data.get('Soil_Moisture', 0),
            temperature=input_data.get('Soil_Temperature', 25),
            soil_type=input_data.get('Soil_Type', 'Alluvial')
        )
    
    def predict_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Predict secondary fertilizer requirements for a batch of samples.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with columns: Nitrogen, Phosphorus, Potassium, Crop_Type,
            pH, Electrical_Conductivity, Soil_Moisture, Soil_Temperature
            
        Returns:
        --------
        pd.DataFrame
            Original DataFrame with added 'Secondary_Fertilizer' column
        """
        
        df_copy = df.copy()
        
        predictions = []
        for idx, row in df_copy.iterrows():
            prediction = self.recommend_fertilizer(
                nitrogen=row.get('Nitrogen', 0),
                phosphorus=row.get('Phosphorus', 0),
                potassium=row.get('Potassium', 0),
                crop_type=row.get('Crop_Type', ''),
                pH=row.get('pH', 7.0),
                ec=row.get('Electrical_Conductivity', 0),
                moisture=row.get('Soil_Moisture', 0),
                temperature=row.get('Soil_Temperature', 25),
                soil_type=row.get('Soil_Type', 'Alluvial')
            )
            predictions.append(prediction)
        
        df_copy['Secondary_Fertilizer'] = predictions
        return df_copy
    
    def get_crop_requirements(self, crop_type: str) -> List[str]:
        """
        Get micronutrient requirements for a specific crop.
        
        Parameters:
        -----------
        crop_type : str
            Name of the crop
            
        Returns:
        --------
        List[str]
            List of micronutrients required by the crop
        """
        
        crop_type_normalized = crop_type.strip().title()
        return self.crop_micronutrients.get(crop_type_normalized, [])


# Interactive user input
if __name__ == "__main__":
    # Initialize the model
    model = SecondaryFertilizerModel()
    
    print("=" * 70)
    print("SECONDARY FERTILIZER RECOMMENDATION SYSTEM")
    print("(Dataset-Based with Rule-Based Fallback)")
    print("=" * 70)
    print("\nAvailable crops:")
    print("Rice, Wheat, Maize, Barley, Jowar, Bajra, Ragi, Groundnut,")
    print("Mustard, Soybean, Sugarcane, Cotton, Chickpea, Moong, Garlic, Onion")
    print("\nAvailable soil types:")
    print("Alluvial, Black, Red, Laterite, Desert, Mountain")
    print("=" * 70)
    
    try:
        # Get user inputs
        print("\nPlease enter the following soil parameters:\n")
        
        nitrogen = float(input("Nitrogen (mg/kg): "))
        phosphorus = float(input("Phosphorus (mg/kg): "))
        potassium = float(input("Potassium (mg/kg): "))
        crop_type = input("Crop Type: ").strip()
        soil_type = input("Soil Type [default: Alluvial]: ").strip() or 'Alluvial'
        pH = float(input("pH: "))
        ec = float(input("Electrical Conductivity (µS/cm): "))
        moisture = float(input("Soil Moisture (%): "))
        temperature = float(input("Soil Temperature (°C): "))
        
        print("\n" + "=" * 70)
        print("PROCESSING...")
        print("=" * 70)
        
        # Categorize inputs
        ph_range = model.categorize_ph(pH)
        ec_range = model.categorize_ec(ec)
        
        print(f"\n📊 Categorized Parameters:")
        print(f"   pH Range: {ph_range}")
        print(f"   EC Range: {ec_range}")
        print(f"   Soil Type: {soil_type}")
        
        # Get recommendation
        recommendation = model.recommend_fertilizer(
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            crop_type=crop_type,
            pH=pH,
            ec=ec,
            moisture=moisture,
            temperature=temperature,
            soil_type=soil_type
        )
        
        # Display results
        print("\n" + "=" * 70)
        print("RECOMMENDATION RESULTS")
        print("=" * 70)
        print(f"\n📍 Location & Soil Information:")
        print(f"   Soil Type: {soil_type}")
        print(f"   pH: {pH} ({ph_range})")
        print(f"   EC: {ec} µS/cm ({ec_range})")
        print(f"\n🌱 Crop Information:")
        print(f"   Crop: {crop_type}")
        print(f"\n🧪 Soil Nutrients:")
        print(f"   Nitrogen: {nitrogen} mg/kg")
        print(f"   Phosphorus: {phosphorus} mg/kg")
        print(f"   Potassium: {potassium} mg/kg")
        print(f"\n🌡️ Environmental Conditions:")
        print(f"   Moisture: {moisture}%")
        print(f"   Temperature: {temperature}°C")
        print("\n" + "-" * 70)
        print(f"💊 RECOMMENDED SECONDARY FERTILIZER:")
        print(f"   {recommendation}")
        print("=" * 70)
        
        # Show identified deficiencies
        deficiencies = model.identify_deficiencies(
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            pH=pH,
            ec=ec,
            moisture=moisture,
            temperature=temperature,
            crop_type=crop_type,
            soil_type=soil_type
        )
        
        if deficiencies:
            print(f"\n🔍 Identified Micronutrient Deficiencies:")
            print(f"   {', '.join(deficiencies)}")
            print("=" * 70)
        
    except ValueError as e:
        print(f"\nError: Invalid input. Please enter numeric values for all parameters except crop type.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
