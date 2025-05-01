from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv
import os
import requests
import logging

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)



# Fetch USDA API key 
USDA_API_KEY = os.getenv("NUTRITION_API_KEY")
USDA_BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"



# --- fetch Function ---
def fetch_nutrition_data(food_name: Text, desired_unit: Optional[Text] = None) -> Optional[Dict[Text, Any]]:
    headers = {
        'Content-Type': 'application/json'
    }
    params = {
        'query': food_name,
        'api_key': USDA_API_KEY
    }

    try:
        response = requests.get(USDA_BASE_URL, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            foods = data.get('foods', [])

            if not foods:
                logger.warning(f"No food data found for: {food_name}")
                return None

            selected_food = None

            # Look through top 5 foods for a matching unit
            for food in foods[:5]:
                food_measures = food.get('foodMeasures', [])
                for measure in food_measures:
                    if desired_unit and desired_unit.lower() in measure.get('measureUnitAbbreviation', '').lower():
                        selected_food = food
                        logger.debug(f"Found matching unit '{desired_unit}' in food: {food.get('description')}")
                        break
                    if desired_unit and desired_unit.lower() in measure.get('measure', '').lower():
                        selected_food = food
                        logger.debug(f"Found matching unit '{desired_unit}' in food: {food.get('description')}")
                        break
                if selected_food:
                    break

            # If no matching unit found, fallback to first result
            if not selected_food:
                selected_food = foods[0]
                logger.debug(f"No matching unit found. Using top result: {selected_food.get('description')}")

            nutrition = selected_food.get('foodNutrients', [])

            nutrition_data = {
                'calories': None,
                'protein': None,
                'carbs': None,
                'fats': None
            }

            for nutrient in nutrition:
                if nutrient.get('nutrientName') == 'Energy':
                    nutrition_data['calories'] = nutrient.get('value')
                elif nutrient.get('nutrientName') == 'Protein':
                    nutrition_data['protein'] = nutrient.get('value')
                elif nutrient.get('nutrientName') == 'Carbohydrate, by difference':
                    nutrition_data['carbs'] = nutrient.get('value')
                elif nutrient.get('nutrientName') == 'Total lipid (fat)':
                    nutrition_data['fats'] = nutrient.get('value')

            return nutrition_data

        else:
            logger.error(f"API request failed for {food_name} with status code {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data for {food_name}: {e}")
        return None



# ------------ Actions-----------------

class ActionGetCalories(Action):
    def name(self) -> Text:
        return "action_get_calories"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food = next(tracker.get_latest_entity_values("food"), None)
        quantity = next(tracker.get_latest_entity_values("quantity"), None)
        unit = next(tracker.get_latest_entity_values("unit"), None)

        logger.debug(f"Detected food: {food}, quantity: {quantity}, unit: {unit}")

        nutrient = "calories"  # This is the only hardcoded part

        if not food:
            dispatcher.utter_message(response="utter_no_food_found")
            return []

        try:
            quantity = float(quantity) if quantity else 100.0
        except ValueError:
            quantity = 100.0

        nutrition = fetch_nutrition_data(food, desired_unit=unit)
        if not nutrition or nutrition.get(nutrient) is None:
            dispatcher.utter_message(
                response="utter_no_nutrition_info",
                food=food, 
                nutrient=nutrient
            )
            return []

        amount_per_100g = nutrition[nutrient]
        amount_for_quantity = (amount_per_100g / 100) * quantity

        valid_gram_units = ["g", "gram", "grams"]
        if unit and unit.lower() not in valid_gram_units:
         dispatcher.utter_message(
        response="utter_unit_not_found_default_100g",
        unit=unit,
        food=food,
        amount=round(amount_for_quantity, 1),
        nutrient=nutrient
        )
        else:
            
         dispatcher.utter_message(
        response="utter_quantity_found",
        quantity=quantity,
        food=food,
        amount=round(amount_for_quantity, 1),
        nutrient=nutrient
    )


        return []


class ActionGetProtein(Action):
    def name(self) -> Text:
        return "action_get_protein"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food = next(tracker.get_latest_entity_values("food"), None)
        quantity = next(tracker.get_latest_entity_values("quantity"), None)
        unit = next(tracker.get_latest_entity_values("unit"), None)

        logger.debug(f"Detected food: {food}, quantity: {quantity}, unit: {unit}")

        nutrient = "protein"  # Only hardcoded text

        if not food:
            dispatcher.utter_message(response="utter_no_food_found")
            return []

        try:
            quantity = float(quantity) if quantity else 100.0
        except ValueError:
            quantity = 100.0

        nutrition = fetch_nutrition_data(food, desired_unit=unit)
        if not nutrition or nutrition.get(nutrient) is None:
            dispatcher.utter_message(
                response="utter_no_nutrition_info",
                food=food, 
                nutrient=nutrient
            )
            return []

        amount_per_100g = nutrition[nutrient]
        amount_for_quantity = (amount_per_100g / 100) * quantity

        valid_gram_units = ["g", "gram", "grams"]
        if unit and unit.lower() not in valid_gram_units:
         dispatcher.utter_message(
        response="utter_unit_not_found_default_100g",
        unit=unit,
        food=food,
        amount=round(amount_for_quantity, 1),
        nutrient=nutrient
        )
        else:
         dispatcher.utter_message(
        response="utter_quantity_found",
        quantity=quantity,
        food=food,
        amount=round(amount_for_quantity, 1),
        nutrient=nutrient
    )

        return []

class ActionGetCarbs(Action):
    def name(self) -> Text:
        return "action_get_carbs"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food = next(tracker.get_latest_entity_values("food"), None)
        quantity = next(tracker.get_latest_entity_values("quantity"), None)
        unit = next(tracker.get_latest_entity_values("unit"), None)

        logger.debug(f"Detected food: {food}, quantity: {quantity}, unit: {unit}")

        nutrient = "carbs"  # Only hardcoded text

        if not food:
            dispatcher.utter_message(response="utter_no_food_found")
            return []

        try:
            quantity = float(quantity) if quantity else 100.0
        except ValueError:
            quantity = 100.0

        nutrition = fetch_nutrition_data(food, desired_unit=unit)
        if not nutrition or nutrition.get(nutrient) is None:
            dispatcher.utter_message(
                response="utter_no_nutrition_info",
                food=food, 
                nutrient=nutrient
            )
            return []

        amount_per_100g = nutrition[nutrient]
        amount_for_quantity = (amount_per_100g / 100) * quantity

        valid_gram_units = ["g", "gram", "grams"]
        if unit and unit.lower() not in valid_gram_units:
         dispatcher.utter_message(
        response="utter_unit_not_found_default_100g",
        unit=unit,
        food=food,
        amount=round(amount_for_quantity, 1),
        nutrient=nutrient
        )
        else:
         dispatcher.utter_message(
        response="utter_quantity_found",
        quantity=quantity,
        food=food,
        amount=round(amount_for_quantity, 1),
        nutrient=nutrient
    )

        return []


class ActionGetFats(Action):
    def name(self) -> Text:
        return "action_get_fats"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food = next(tracker.get_latest_entity_values("food"), None)
        quantity = next(tracker.get_latest_entity_values("quantity"), None)
        unit = next(tracker.get_latest_entity_values("unit"), None)

        logger.debug(f"Detected food: {food}, quantity: {quantity}, unit: {unit}")

        nutrient = "fats"  # Only hardcoded text

        if not food:
            dispatcher.utter_message(response="utter_no_food_found")
            return []

        try:
            quantity = float(quantity) if quantity else 100.0
        except ValueError:
            quantity = 100.0

        nutrition = fetch_nutrition_data(food, desired_unit=unit)
        if not nutrition or nutrition.get(nutrient) is None:
            dispatcher.utter_message(
                response="utter_no_nutrition_info",
                food=food, 
                nutrient=nutrient
            )
            return []

        amount_per_100g = nutrition[nutrient]
        amount_for_quantity = (amount_per_100g / 100) * quantity

        valid_gram_units = ["g", "gram", "grams"]
        if unit and unit.lower() not in valid_gram_units:
         dispatcher.utter_message(
        response="utter_unit_not_found_default_100g",
        unit=unit,
        food=food,
        amount=round(amount_for_quantity, 1),
        nutrient=nutrient
        )
        else:
         dispatcher.utter_message(
        response="utter_quantity_found",
        quantity=quantity,
        food=food,
        amount=round(amount_for_quantity, 1),
        nutrient=nutrient
    )

        return []

