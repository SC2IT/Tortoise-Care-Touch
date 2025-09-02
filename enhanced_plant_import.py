#!/usr/bin/env python3
"""
Enhanced Plant Database Import from The Tortoise Table
Comprehensive data from all plant categories
"""

from database.db_manager import DatabaseManager

# Comprehensive plant data from The Tortoise Table categories
COMPREHENSIVE_PLANTS = [
    # WILD FLOWERS - Safe to Feed
    {'name': 'Alexanders', 'scientific_name': 'Smyrnium olusatrum', 'safety_level': 'safe', 'category': 'wild_flowers', 'nutrition_notes': 'Young leaves and stems edible', 'feeding_frequency': 'Daily when available'},
    {'name': 'Blue Sowthistle', 'scientific_name': 'Cicerbita macrophylla', 'safety_level': 'safe', 'category': 'wild_flowers', 'nutrition_notes': 'High calcium content', 'feeding_frequency': 'Daily'},
    {'name': 'Cat\'s Ear', 'scientific_name': 'Hypochaeris radicata', 'safety_level': 'safe', 'category': 'wild_flowers', 'nutrition_notes': 'Dandelion-like properties', 'feeding_frequency': 'Daily'},
    {'name': 'Mallow', 'scientific_name': 'Malva sylvestris', 'safety_level': 'safe', 'category': 'wild_flowers', 'nutrition_notes': 'Mucilaginous, aids digestion', 'feeding_frequency': 'Daily'},
    {'name': 'Plantain', 'scientific_name': 'Plantago major', 'safety_level': 'safe', 'category': 'wild_flowers', 'nutrition_notes': 'Natural antibiotic properties', 'feeding_frequency': 'Daily - staple food'},
    {'name': 'Sow Thistle', 'scientific_name': 'Sonchus oleraceus', 'safety_level': 'safe', 'category': 'wild_flowers', 'nutrition_notes': 'High calcium, excellent base food', 'feeding_frequency': 'Daily - staple food'},
    {'name': 'Violet', 'scientific_name': 'Viola species', 'safety_level': 'safe', 'category': 'wild_flowers', 'nutrition_notes': 'Flowers and leaves edible', 'feeding_frequency': 'Weekly'},
    {'name': 'White Deadnettle', 'scientific_name': 'Lamium album', 'safety_level': 'safe', 'category': 'wild_flowers', 'nutrition_notes': 'Young leaves and flowers', 'feeding_frequency': '2-3 times weekly'},
    {'name': 'Forget-Me-Not', 'scientific_name': 'Myosotis species', 'safety_level': 'safe', 'category': 'wild_flowers', 'nutrition_notes': 'Small amounts of flowers and leaves', 'feeding_frequency': 'Weekly treat'},
    {'name': 'Knapweed', 'scientific_name': 'Centaurea species', 'safety_level': 'safe', 'category': 'wild_flowers', 'nutrition_notes': 'Flowers particularly enjoyed', 'feeding_frequency': '2-3 times weekly'},

    # WILD FLOWERS - Feed in Moderation  
    {'name': 'Chickweed', 'scientific_name': 'Stellaria media', 'safety_level': 'caution', 'category': 'wild_flowers', 'nutrition_notes': 'High water content, mild diuretic', 'feeding_frequency': '2-3 times weekly'},
    {'name': 'Dandelion', 'scientific_name': 'Taraxacum officinale', 'safety_level': 'caution', 'category': 'wild_flowers', 'nutrition_notes': 'Excellent but can be diuretic in large amounts', 'feeding_frequency': 'Daily in moderation'},
    {'name': 'Clover', 'scientific_name': 'Trifolium species', 'safety_level': 'caution', 'category': 'wild_flowers', 'nutrition_notes': 'High protein, limit to prevent bloat', 'feeding_frequency': '2-3 times weekly'},
    {'name': 'Bindweed', 'scientific_name': 'Convolvulus arvensis', 'safety_level': 'caution', 'category': 'wild_flowers', 'nutrition_notes': 'Related to morning glory, feed sparingly', 'feeding_frequency': 'Weekly only'},
    {'name': 'Chicory', 'scientific_name': 'Cichorium intybus', 'safety_level': 'caution', 'category': 'wild_flowers', 'nutrition_notes': 'Can be slightly bitter', 'feeding_frequency': '2-3 times weekly'},

    # GARDEN & HOUSE PLANTS - Safe to Feed
    {'name': 'African Violet', 'scientific_name': 'Saintpaulia ionantha', 'safety_level': 'safe', 'category': 'garden_plants', 'nutrition_notes': 'Flowers are safe treats', 'feeding_frequency': 'Weekly treat'},
    {'name': 'Snapdragon', 'scientific_name': 'Antirrhinum majus', 'safety_level': 'safe', 'category': 'garden_plants', 'nutrition_notes': 'Flowers and young leaves', 'feeding_frequency': 'Weekly'},
    {'name': 'Aster', 'scientific_name': 'Symphyotrichum species', 'safety_level': 'safe', 'category': 'garden_plants', 'nutrition_notes': 'Fall blooming flowers', 'feeding_frequency': 'Weekly'},
    {'name': 'Geranium', 'scientific_name': 'Pelargonium species', 'safety_level': 'safe', 'category': 'garden_plants', 'nutrition_notes': 'Flowers and leaves, aromatic', 'feeding_frequency': '2-3 times weekly'},
    {'name': 'Hollyhock', 'scientific_name': 'Alcea rosea', 'safety_level': 'safe', 'category': 'garden_plants', 'nutrition_notes': 'Large flowers, leaves also edible', 'feeding_frequency': 'Weekly'},
    {'name': 'Marjoram', 'scientific_name': 'Origanum majorana', 'safety_level': 'safe', 'category': 'garden_plants', 'nutrition_notes': 'Aromatic herb, use fresh', 'feeding_frequency': '2-3 times weekly'},
    {'name': 'Mint', 'scientific_name': 'Mentha species', 'safety_level': 'safe', 'category': 'garden_plants', 'nutrition_notes': 'Digestive aid, use fresh', 'feeding_frequency': '2-3 times weekly'},
    {'name': 'Oregano', 'scientific_name': 'Origanum vulgare', 'safety_level': 'safe', 'category': 'garden_plants', 'nutrition_notes': 'Natural antibiotic properties', 'feeding_frequency': '2-3 times weekly'},
    {'name': 'Pansy', 'scientific_name': 'Viola tricolor', 'safety_level': 'safe', 'category': 'garden_plants', 'nutrition_notes': 'Flowers and young leaves', 'feeding_frequency': 'Weekly treat'},
    {'name': 'Spider Plant', 'scientific_name': 'Chlorophytum comosum', 'safety_level': 'safe', 'category': 'garden_plants', 'nutrition_notes': 'Houseplant leaves safe in small amounts', 'feeding_frequency': 'Weekly'},
    {'name': 'Thyme', 'scientific_name': 'Thymus vulgaris', 'safety_level': 'safe', 'category': 'garden_plants', 'nutrition_notes': 'Aromatic herb, respiratory benefits', 'feeding_frequency': '2-3 times weekly'},

    # GARDEN & HOUSE PLANTS - Feed in Moderation
    {'name': 'Basil', 'scientific_name': 'Ocimum basilicum', 'safety_level': 'caution', 'category': 'garden_plants', 'nutrition_notes': 'Strong essential oils, use sparingly', 'feeding_frequency': 'Weekly treat'},
    {'name': 'Begonia', 'scientific_name': 'Begonia species', 'safety_level': 'caution', 'category': 'garden_plants', 'nutrition_notes': 'Oxalic acid content, limit quantity', 'feeding_frequency': 'Monthly treat'},
    {'name': 'Chrysanthemum', 'scientific_name': 'Chrysanthemum species', 'safety_level': 'caution', 'category': 'garden_plants', 'nutrition_notes': 'Natural pesticide compounds', 'feeding_frequency': 'Monthly treat'},
    {'name': 'Day Lily', 'scientific_name': 'Hemerocallis species', 'safety_level': 'caution', 'category': 'garden_plants', 'nutrition_notes': 'Flowers only, not leaves', 'feeding_frequency': 'Weekly treat'},
    {'name': 'Hosta', 'scientific_name': 'Hosta species', 'safety_level': 'caution', 'category': 'garden_plants', 'nutrition_notes': 'Young leaves only, can be tough', 'feeding_frequency': 'Weekly'},
    {'name': 'Lemon Balm', 'scientific_name': 'Melissa officinalis', 'safety_level': 'caution', 'category': 'garden_plants', 'nutrition_notes': 'Strong citrus oils, calming effect', 'feeding_frequency': 'Weekly'},

    # TREES, SHRUBS & CLIMBERS - Safe
    {'name': 'Apple Tree', 'scientific_name': 'Malus domestica', 'safety_level': 'safe', 'category': 'trees_shrubs', 'nutrition_notes': 'Leaves and fruit safe, remove seeds', 'feeding_frequency': 'Weekly - fruit as treat'},
    {'name': 'Mulberry', 'scientific_name': 'Morus species', 'safety_level': 'safe', 'category': 'trees_shrubs', 'nutrition_notes': 'Excellent calcium ratio, preferred food', 'feeding_frequency': 'Daily when available'},
    {'name': 'Rose', 'scientific_name': 'Rosa species', 'safety_level': 'safe', 'category': 'trees_shrubs', 'nutrition_notes': 'Petals and hips, high vitamin C', 'feeding_frequency': 'Weekly'},
    {'name': 'Hibiscus', 'scientific_name': 'Hibiscus rosa-sinensis', 'safety_level': 'safe', 'category': 'trees_shrubs', 'nutrition_notes': 'Flowers and leaves, high vitamin C', 'feeding_frequency': '2-3 times weekly'},
    {'name': 'Grape Vine', 'scientific_name': 'Vitis vinifera', 'safety_level': 'safe', 'category': 'trees_shrubs', 'nutrition_notes': 'Young leaves preferred, avoid old/tough leaves', 'feeding_frequency': '2-3 times weekly'},

    # CACTI & SUCCULENTS - Safe
    {'name': 'Prickly Pear Cactus', 'scientific_name': 'Opuntia species', 'safety_level': 'safe', 'category': 'cacti_succulents', 'nutrition_notes': 'Remove spines, high water content', 'feeding_frequency': 'Weekly'},
    {'name': 'Sedum', 'scientific_name': 'Sedum species', 'safety_level': 'safe', 'category': 'cacti_succulents', 'nutrition_notes': 'Various species, good water content', 'feeding_frequency': '2-3 times weekly'},
    {'name': 'Echeveria', 'scientific_name': 'Echeveria species', 'safety_level': 'safe', 'category': 'cacti_succulents', 'nutrition_notes': 'Rosette-forming succulent', 'feeding_frequency': 'Weekly'},
    {'name': 'Christmas Cactus', 'scientific_name': 'Schlumbergera species', 'safety_level': 'safe', 'category': 'cacti_succulents', 'nutrition_notes': 'Flowers and pads safe', 'feeding_frequency': 'Weekly treat'},

    # GRASSES & FERNS - Safe  
    {'name': 'Timothy Grass', 'scientific_name': 'Phleum pratense', 'safety_level': 'safe', 'category': 'grasses_ferns', 'nutrition_notes': 'High fiber hay grass', 'feeding_frequency': 'Daily - dried as hay'},
    {'name': 'Meadow Grass', 'scientific_name': 'Poa species', 'safety_level': 'safe', 'category': 'grasses_ferns', 'nutrition_notes': 'Common lawn grass', 'feeding_frequency': 'Daily when available'},
    {'name': 'Oat Grass', 'scientific_name': 'Avena sativa', 'safety_level': 'safe', 'category': 'grasses_ferns', 'nutrition_notes': 'Young shoots preferred', 'feeding_frequency': '2-3 times weekly'},

    # FRUIT & VEGETABLES - Safe
    {'name': 'Bell Pepper', 'scientific_name': 'Capsicum annuum', 'safety_level': 'safe', 'category': 'fruits_vegetables', 'nutrition_notes': 'High vitamin C, remove seeds', 'feeding_frequency': 'Weekly treat'},
    {'name': 'Cucumber', 'scientific_name': 'Cucumis sativus', 'safety_level': 'safe', 'category': 'fruits_vegetables', 'nutrition_notes': 'High water content, cooling', 'feeding_frequency': 'Weekly treat'},
    {'name': 'Strawberry', 'scientific_name': 'Fragaria ananassa', 'safety_level': 'safe', 'category': 'fruits_vegetables', 'nutrition_notes': 'Fruit and leaves, high vitamin C', 'feeding_frequency': 'Weekly treat'},
    {'name': 'Pumpkin', 'scientific_name': 'Cucurbita pepo', 'safety_level': 'safe', 'category': 'fruits_vegetables', 'nutrition_notes': 'Flesh and flowers, good beta-carotene', 'feeding_frequency': 'Weekly treat'},

    # FRUIT & VEGETABLES - Caution
    {'name': 'Spinach', 'scientific_name': 'Spinacia oleracea', 'safety_level': 'caution', 'category': 'fruits_vegetables', 'nutrition_notes': 'High oxalates bind calcium', 'feeding_frequency': 'Monthly only'},
    {'name': 'Kale', 'scientific_name': 'Brassica oleracea acephala', 'safety_level': 'caution', 'category': 'fruits_vegetables', 'nutrition_notes': 'Goitrogens affect thyroid', 'feeding_frequency': 'Monthly only'},
    {'name': 'Swiss Chard', 'scientific_name': 'Beta vulgaris cicla', 'safety_level': 'caution', 'category': 'fruits_vegetables', 'nutrition_notes': 'Very high oxalates', 'feeding_frequency': 'Rarely'},
    {'name': 'Lettuce (Iceberg)', 'scientific_name': 'Lactuca sativa', 'safety_level': 'caution', 'category': 'fruits_vegetables', 'nutrition_notes': 'Low nutrition, can cause diarrhea', 'feeding_frequency': 'Avoid - use romaine instead'},

    # TOXIC PLANTS - Never Feed
    {'name': 'Buttercup', 'scientific_name': 'Ranunculus species', 'safety_level': 'toxic', 'category': 'wild_flowers', 'nutrition_notes': 'TOXIC - Contains ranunculin, severe irritation', 'feeding_frequency': 'NEVER'},
    {'name': 'Foxglove', 'scientific_name': 'Digitalis purpurea', 'safety_level': 'toxic', 'category': 'garden_plants', 'nutrition_notes': 'TOXIC - Cardiac glycosides, potentially fatal', 'feeding_frequency': 'NEVER'},
    {'name': 'Daffodil', 'scientific_name': 'Narcissus species', 'safety_level': 'toxic', 'category': 'garden_plants', 'nutrition_notes': 'TOXIC - Lycorine alkaloids, all parts toxic', 'feeding_frequency': 'NEVER'},
    {'name': 'Azalea', 'scientific_name': 'Rhododendron species', 'safety_level': 'toxic', 'category': 'trees_shrubs', 'nutrition_notes': 'TOXIC - Grayanotoxins, severe poisoning', 'feeding_frequency': 'NEVER'},
    {'name': 'Yew', 'scientific_name': 'Taxus baccata', 'safety_level': 'toxic', 'category': 'trees_shrubs', 'nutrition_notes': 'TOXIC - Taxine alkaloids, extremely dangerous', 'feeding_frequency': 'NEVER'},
    {'name': 'Oleander', 'scientific_name': 'Nerium oleander', 'safety_level': 'toxic', 'category': 'trees_shrubs', 'nutrition_notes': 'TOXIC - Cardiac glycosides, highly poisonous', 'feeding_frequency': 'NEVER'},
    {'name': 'Avocado', 'scientific_name': 'Persea americana', 'safety_level': 'toxic', 'category': 'fruits_vegetables', 'nutrition_notes': 'TOXIC - Persin harmful to reptiles', 'feeding_frequency': 'NEVER'},
    {'name': 'Tomato Leaves', 'scientific_name': 'Solanum lycopersicum', 'safety_level': 'toxic', 'category': 'fruits_vegetables', 'nutrition_notes': 'TOXIC - Solanine and tomatine alkaloids', 'feeding_frequency': 'NEVER'},
    {'name': 'Potato Leaves', 'scientific_name': 'Solanum tuberosum', 'safety_level': 'toxic', 'category': 'fruits_vegetables', 'nutrition_notes': 'TOXIC - Solanine, especially in green parts', 'feeding_frequency': 'NEVER'},
    {'name': 'Ivy', 'scientific_name': 'Hedera helix', 'safety_level': 'toxic', 'category': 'trees_shrubs', 'nutrition_notes': 'TOXIC - Saponins cause digestive issues', 'feeding_frequency': 'NEVER'},
    {'name': 'Lily', 'scientific_name': 'Lilium species', 'safety_level': 'toxic', 'category': 'garden_plants', 'nutrition_notes': 'TOXIC - Various toxic compounds', 'feeding_frequency': 'NEVER'},
    {'name': 'Morning Glory', 'scientific_name': 'Ipomoea species', 'safety_level': 'toxic', 'category': 'garden_plants', 'nutrition_notes': 'TOXIC - Ergot alkaloids in seeds', 'feeding_frequency': 'NEVER'}
]

def clear_and_populate_enhanced_database():
    """Clear existing plants and populate with comprehensive Tortoise Table data"""
    
    print("Enhanced Plant Database Import from The Tortoise Table")
    print("=" * 55)
    
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        # Clear existing plants
        print("Clearing existing plant database...")
        cursor.execute('DELETE FROM plants')
        deleted = cursor.rowcount
        print(f"Deleted {deleted} existing plants")
        
        # Insert comprehensive plant data
        print(f"\nImporting {len(COMPREHENSIVE_PLANTS)} plants from all categories...")
        inserted_count = 0
        
        for plant in COMPREHENSIVE_PLANTS:
            cursor.execute('''
                INSERT INTO plants (
                    name, scientific_name, safety_level, nutrition_notes, 
                    feeding_frequency, description, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                plant['name'],
                plant.get('scientific_name'),
                plant['safety_level'],
                plant.get('nutrition_notes'),
                plant.get('feeding_frequency'),
                plant.get('description', f"{plant['category'].replace('_', ' ').title()} plant")
            ))
            inserted_count += 1
            category_display = plant['category'].replace('_', ' ').title()
            print(f"  Added: {plant['name']} ({plant['safety_level']}) - {category_display}")
        
        # Commit changes
        conn.commit()
        
        print(f"\nSuccessfully imported {inserted_count} plants!")
        
        # Show comprehensive statistics
        cursor.execute('SELECT safety_level, COUNT(*) FROM plants GROUP BY safety_level ORDER BY safety_level')
        stats = cursor.fetchall()
        
        print(f"\nComprehensive plant safety statistics:")
        total_safe = total_caution = total_toxic = 0
        for safety, count in stats:
            print(f"  {safety.title()}: {count} plants")
            if safety == 'safe': total_safe = count
            elif safety == 'caution': total_caution = count  
            elif safety == 'toxic': total_toxic = count
        
        print(f"\nSafety Summary:")
        print(f"  ✅ Safe for daily/regular feeding: {total_safe}")
        print(f"  ⚠️  Feed with caution/moderation: {total_caution}")
        print(f"  ❌ Never feed (toxic): {total_toxic}")
        
        # Show category breakdown
        print(f"\nPlants by category:")
        categories = set(plant['category'] for plant in COMPREHENSIVE_PLANTS)
        for category in sorted(categories):
            count = len([p for p in COMPREHENSIVE_PLANTS if p['category'] == category])
            category_display = category.replace('_', ' ').title()
            print(f"  {category_display}: {count} plants")
        
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"ERROR: Failed to populate database: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        conn.close()

if __name__ == "__main__":
    success = clear_and_populate_enhanced_database()
    if success:
        print(f"\nEnhanced plant database ready for use!")
        print("Data source: The Tortoise Table (thetortoisetable.org.uk)")
        print("Categories: Wild Flowers, Garden Plants, Trees/Shrubs, Cacti/Succulents, Grasses/Ferns, Fruits/Vegetables")
    else:
        print(f"\nDatabase population failed.")