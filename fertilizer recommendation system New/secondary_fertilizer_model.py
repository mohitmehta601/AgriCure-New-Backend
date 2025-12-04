"""
Secondary Fertilizer (Micronutrient) Recommendation Model
This model predicts micronutrient fertilizer requirements based on soil parameters and crop type.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple


class SecondaryFertilizerModel:
    """
    Model to predict secondary fertilizer (micronutrient) requirements
    based on soil conditions and crop type.
    """
    
    def __init__(self):
        """Initialize the model with crop-specific micronutrient requirements."""
        
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
            'Ni': 'Nickel Sulphate'
        }
        
    def identify_deficiencies(self, 
                            nitrogen: float,
                            phosphorus: float,
                            potassium: float,
                            pH: float,
                            ec: float,
                            moisture: float,
                            temperature: float,
                            crop_type: str) -> List[str]:
        """
        Identify micronutrient deficiencies based on soil parameters and mapping rules.
        
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
                           temperature: float) -> str:
        """
        Recommend secondary fertilizer based on input parameters.
        
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
            
        Returns:
        --------
        str
            Recommended fertilizer(s) in format "Fertilizer1 + Fertilizer2 + ..."
        """
        
        # Identify deficiencies
        deficiencies = self.identify_deficiencies(
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            pH=pH,
            ec=ec,
            moisture=moisture,
            temperature=temperature,
            crop_type=crop_type
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
            temperature=input_data.get('Soil_Temperature', 25)
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
                temperature=row.get('Soil_Temperature', 25)
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
    print("=" * 70)
    print("\nAvailable crops:")
    print("Rice, Wheat, Maize, Barley, Jowar, Bajra, Ragi, Groundnut,")
    print("Mustard, Soybean, Sugarcane, Cotton, Chickpea, Moong, Garlic, Onion")
    print("=" * 70)
    
    try:
        # Get user inputs
        print("\nPlease enter the following soil parameters:\n")
        
        nitrogen = float(input("Nitrogen (mg/kg): "))
        phosphorus = float(input("Phosphorus (mg/kg): "))
        potassium = float(input("Potassium (mg/kg): "))
        crop_type = input("Crop Type: ").strip()
        pH = float(input("pH: "))
        ec = float(input("Electrical Conductivity (µS/cm): "))
        moisture = float(input("Soil Moisture (%): "))
        temperature = float(input("Soil Temperature (°C): "))
        
        print("\n" + "=" * 70)
        print("PROCESSING...")
        print("=" * 70)
        
        # Get recommendation
        recommendation = model.recommend_fertilizer(
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            crop_type=crop_type,
            pH=pH,
            ec=ec,
            moisture=moisture,
            temperature=temperature
        )
        
        # Display results
        print("\n" + "=" * 70)
        print("RECOMMENDATION RESULTS")
        print("=" * 70)
        print(f"\nCrop: {crop_type}")
        print(f"Soil pH: {pH}")
        print(f"Nitrogen: {nitrogen} mg/kg")
        print(f"Phosphorus: {phosphorus} mg/kg")
        print(f"Potassium: {potassium} mg/kg")
        print(f"EC: {ec} µS/cm")
        print(f"Moisture: {moisture}%")
        print(f"Temperature: {temperature}°C")
        print("\n" + "-" * 70)
        print(f"RECOMMENDED SECONDARY FERTILIZER:")
        print(f"{recommendation}")
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
            crop_type=crop_type
        )
        
        if deficiencies:
            print(f"\nIdentified Micronutrient Deficiencies: {', '.join(deficiencies)}")
            print("=" * 70)
        
    except ValueError as e:
        print(f"\nError: Invalid input. Please enter numeric values for all parameters except crop type.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
