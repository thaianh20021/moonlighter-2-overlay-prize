"""
Price Database Module for Moonlighter 2 Overlay
Loads relic data and provides fuzzy search functionality
"""

import json
from typing import Optional, Dict, List
from rapidfuzz import fuzz, process


class PriceDatabase:
    def __init__(self, data_file: str = "data.json"):
        """Initialize the price database"""
        self.data = self._load_data(data_file)
        self.all_items = self._flatten_items()
        
    def _load_data(self, data_file: str) -> Dict:
        """Load relic data from JSON file"""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {data_file} not found!")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {data_file}")
            return {}
    
    def _flatten_items(self) -> List[Dict]:
        """Flatten all items from all locations into a single list"""
        items = []
        for location, relics in self.data.items():
            for relic in relics:
                item = relic.copy()
                item['location'] = location
                items.append(item)
        return items
    
    def find_item(self, item_name: str, threshold: int = 80) -> Optional[Dict]:
        """
        Find an item using fuzzy matching to handle OCR errors
        
        Args:
            item_name: The item name to search for
            threshold: Minimum similarity score (0-100)
            
        Returns:
            Dict with item info or None if not found
        """
        if not item_name or not item_name.strip():
            return None
        
        # Clean the input
        item_name = item_name.strip()
        
        # Create a list of item names for fuzzy matching
        item_names = [item['name'] for item in self.all_items]
        
        # Find the best match
        result = process.extractOne(
            item_name, 
            item_names, 
            scorer=fuzz.ratio,
            score_cutoff=threshold
        )
        
        if result:
            matched_name, score, _ = result
            # Find the full item data
            for item in self.all_items:
                if item['name'] == matched_name:
                    return {
                        **item,
                        'match_score': score,
                        'original_query': item_name
                    }
        
        return None
    
    def get_item_by_exact_name(self, item_name: str) -> Optional[Dict]:
        """Get item by exact name match"""
        for item in self.all_items:
            if item['name'].lower() == item_name.lower():
                return item
        return None
    
    def get_items_by_location(self, location: str) -> List[Dict]:
        """Get all items from a specific location"""
        return self.data.get(location, [])
    
    def get_items_by_rarity(self, rarity: str) -> List[Dict]:
        """Get all items of a specific rarity"""
        return [item for item in self.all_items if item['rarity'].lower() == rarity.lower()]


if __name__ == "__main__":
    # Test the database
    db = PriceDatabase()
    
    # Test exact match
    print("Testing exact match:")
    item = db.find_item("Broken Battery")
    if item:
        print(f"Found: {item['name']} - {item['rarity']} - {item['price']}g - {item['location']}")
    
    # Test fuzzy match (simulating OCR error)
    print("\nTesting fuzzy match (OCR error simulation):")
    item = db.find_item("Broken Baftery")  # Intentional typo
    if item:
        print(f"Found: {item['name']} (score: {item['match_score']}) - {item['price']}g")
    
    # Test another fuzzy match
    print("\nTesting fuzzy match 2:")
    item = db.find_item("Sacred Sickle")
    if item:
        print(f"Found: {item['name']} - {item['rarity']} - {item['price']}g")
