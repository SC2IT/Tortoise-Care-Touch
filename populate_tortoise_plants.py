#!/usr/bin/env python3
"""
Populate plant database with curated data from The Tortoise Table
Based on authoritative tortoise diet information from thetortoisetable.org.uk
"""

from database.db_manager import DatabaseManager

# Curated plant data based on The Tortoise Table recommendations
TORTOISE_PLANTS = [
    # SAFE PLANTS - Regular feeding recommended
    {
        'name': 'Dandelion',
        'scientific_name': 'Taraxacum officinale',
        'safety_level': 'safe',
        'nutrition_notes': 'High in calcium, vitamins A, C, K. Excellent base plant.',
        'feeding_frequency': 'Daily - staple food',
        'description': 'Leaves, flowers, and stems all edible. One of the best tortoise foods.'
    },
    {
        'name': 'Plantain',
        'scientific_name': 'Plantago major',
        'safety_level': 'safe',
        'nutrition_notes': 'Good source of fiber and vitamins. Natural antibiotic properties.',
        'feeding_frequency': 'Daily - staple food',
        'description': 'Common weed, all parts edible. Ribbed leaves distinctive.'
    },
    {
        'name': 'Clover',
        'scientific_name': 'Trifolium repens',
        'safety_level': 'safe',
        'nutrition_notes': 'High protein content, good calcium levels.',
        'feeding_frequency': '2-3 times weekly',
        'description': 'White or red clover, leaves and flowers edible.'
    },
    {
        'name': 'Chickweed',
        'scientific_name': 'Stellaria media',
        'safety_level': 'safe',
        'nutrition_notes': 'High water content, good source of vitamins.',
        'feeding_frequency': 'Daily when available',
        'description': 'Small white flowers, soft leaves. Excellent winter food.'
    },
    {
        'name': 'Hibiscus',
        'scientific_name': 'Hibiscus rosa-sinensis',
        'safety_level': 'safe',
        'nutrition_notes': 'Flowers high in vitamin C. Leaves also nutritious.',
        'feeding_frequency': '2-3 times weekly',
        'description': 'Large colorful flowers. Both flowers and leaves edible.'
    },
    {
        'name': 'Nasturtium',
        'scientific_name': 'Tropaeolum majus',
        'safety_level': 'safe',
        'nutrition_notes': 'High vitamin C, natural antibiotic properties.',
        'feeding_frequency': '2-3 times weekly',
        'description': 'Peppery taste. Flowers, leaves, and seeds all edible.'
    },
    {
        'name': 'Mallow',
        'scientific_name': 'Malva sylvestris',
        'safety_level': 'safe',
        'nutrition_notes': 'Good fiber content, mucilaginous properties aid digestion.',
        'feeding_frequency': 'Daily when available',
        'description': 'Purple-pink flowers, heart-shaped leaves. All parts edible.'
    },
    {
        'name': 'Sow Thistle',
        'scientific_name': 'Sonchus oleraceus',
        'safety_level': 'safe',
        'nutrition_notes': 'High calcium content, good for shell development.',
        'feeding_frequency': 'Daily - staple food',
        'description': 'Yellow flowers, dandelion-like leaves. Young leaves preferred.'
    },
    {
        'name': 'Sedum',
        'scientific_name': 'Sedum species',
        'safety_level': 'safe',
        'nutrition_notes': 'Succulent with good water content.',
        'feeding_frequency': '2-3 times weekly',
        'description': 'Various species of stonecrop. Thick, fleshy leaves.'
    },
    {
        'name': 'Rose Petals',
        'scientific_name': 'Rosa species',
        'safety_level': 'safe',
        'nutrition_notes': 'High vitamin C, natural antioxidants.',
        'feeding_frequency': 'Weekly treat',
        'description': 'Petals only - avoid stems with thorns. Remove stamens.'
    },
    {
        'name': 'Mulberry Leaves',
        'scientific_name': 'Morus species',
        'safety_level': 'safe',
        'nutrition_notes': 'Excellent calcium to phosphorus ratio.',
        'feeding_frequency': 'Daily when available',
        'description': 'Heart-shaped leaves from mulberry trees. Fresh or dried.'
    },
    {
        'name': 'Grape Leaves',
        'scientific_name': 'Vitis vinifera',
        'safety_level': 'safe',
        'nutrition_notes': 'Good fiber, moderate calcium content.',
        'feeding_frequency': '2-3 times weekly',
        'description': 'Young leaves preferred. Avoid pesticide-treated vines.'
    },
    {
        'name': 'Prickly Pear Cactus',
        'scientific_name': 'Opuntia species',
        'safety_level': 'safe',
        'nutrition_notes': 'High water content, good for hydration.',
        'feeding_frequency': 'Weekly',
        'description': 'Remove spines carefully. Both pads and fruits edible.'
    },
    {
        'name': 'Calendula',
        'scientific_name': 'Calendula officinalis',
        'safety_level': 'safe',
        'nutrition_notes': 'Anti-inflammatory properties, good vitamin content.',
        'feeding_frequency': '2-3 times weekly',
        'description': 'Orange marigold flowers. Petals and leaves edible.'
    },
    {
        'name': 'Lime Tree Leaves',
        'scientific_name': 'Tilia species',
        'safety_level': 'safe',
        'nutrition_notes': 'Good calcium source, digestible fiber.',
        'feeding_frequency': 'Daily when available',
        'description': 'Heart-shaped leaves from linden/lime trees.'
    },

    # CAUTION PLANTS - Feed sparingly or with care
    {
        'name': 'Spinach',
        'scientific_name': 'Spinacia oleracea',
        'safety_level': 'caution',
        'nutrition_notes': 'High oxalates can bind calcium. Use sparingly.',
        'feeding_frequency': 'Monthly treat only',
        'description': 'High in iron but oxalates prevent calcium absorption.'
    },
    {
        'name': 'Beet Greens',
        'scientific_name': 'Beta vulgaris',
        'safety_level': 'caution',
        'nutrition_notes': 'High oxalates, feed only occasionally.',
        'feeding_frequency': 'Monthly treat only',
        'description': 'Leaves from beetroot plants. High oxalate content.'
    },
    {
        'name': 'Swiss Chard',
        'scientific_name': 'Beta vulgaris cicla',
        'safety_level': 'caution',
        'nutrition_notes': 'Very high oxalates, use very sparingly.',
        'feeding_frequency': 'Rarely - special occasions only',
        'description': 'Colorful stalks and leaves. High oxalate vegetable.'
    },
    {
        'name': 'Rhubarb Leaves',
        'scientific_name': 'Rheum rhabarbarum',
        'safety_level': 'caution',
        'nutrition_notes': 'Contains oxalic acid, can be harmful in quantity.',
        'feeding_frequency': 'Avoid - use stalks only occasionally',
        'description': 'Leaves contain high oxalic acid. Stalks safer but still limit.'
    },
    {
        'name': 'Iceberg Lettuce',
        'scientific_name': 'Lactuca sativa',
        'safety_level': 'caution',
        'nutrition_notes': 'Low nutritional value, mostly water. Can cause diarrhea.',
        'feeding_frequency': 'Rarely - not recommended',
        'description': 'Poor nutritional choice. Use darker leafy greens instead.'
    },
    {
        'name': 'Cabbage',
        'scientific_name': 'Brassica oleracea',
        'safety_level': 'caution',
        'nutrition_notes': 'Goitrogens can affect thyroid function.',
        'feeding_frequency': 'Monthly treat only',
        'description': 'Cruciferous vegetable. Feed sparingly due to goitrogens.'
    },
    {
        'name': 'Kale',
        'scientific_name': 'Brassica oleracea acephala',
        'safety_level': 'caution',
        'nutrition_notes': 'High goitrogens, can interfere with thyroid.',
        'feeding_frequency': 'Monthly treat only',
        'description': 'Very nutritious but contains goitrogens. Use sparingly.'
    },

    # TOXIC PLANTS - NEVER feed these
    {
        'name': 'Buttercup',
        'scientific_name': 'Ranunculus species',
        'safety_level': 'toxic',
        'nutrition_notes': 'TOXIC - Contains ranunculin which causes severe irritation.',
        'feeding_frequency': 'NEVER',
        'description': 'Bright yellow flowers. All parts highly toxic to tortoises.'
    },
    {
        'name': 'Daffodil',
        'scientific_name': 'Narcissus species',
        'safety_level': 'toxic',
        'nutrition_notes': 'TOXIC - Contains lycorine and other alkaloids.',
        'feeding_frequency': 'NEVER',
        'description': 'Spring bulb flower. All parts extremely toxic.'
    },
    {
        'name': 'Foxglove',
        'scientific_name': 'Digitalis purpurea',
        'safety_level': 'toxic',
        'nutrition_notes': 'TOXIC - Contains cardiac glycosides, potentially fatal.',
        'feeding_frequency': 'NEVER',
        'description': 'Tall spikes of purple flowers. Extremely dangerous.'
    },
    {
        'name': 'Azalea',
        'scientific_name': 'Rhododendron species',
        'safety_level': 'toxic',
        'nutrition_notes': 'TOXIC - Contains grayanotoxins causing severe poisoning.',
        'feeding_frequency': 'NEVER',
        'description': 'Ornamental shrub with clusters of flowers. All parts toxic.'
    },
    {
        'name': 'Yew',
        'scientific_name': 'Taxus baccata',
        'safety_level': 'toxic',
        'nutrition_notes': 'TOXIC - Contains taxine alkaloids, extremely dangerous.',
        'feeding_frequency': 'NEVER',
        'description': 'Evergreen shrub/tree. Leaves and bark highly toxic.'
    },
    {
        'name': 'Ivy',
        'scientific_name': 'Hedera helix',
        'safety_level': 'toxic',
        'nutrition_notes': 'TOXIC - Contains saponins causing digestive issues.',
        'feeding_frequency': 'NEVER',
        'description': 'Climbing vine with lobed leaves. All parts toxic.'
    },
    {
        'name': 'Oleander',
        'scientific_name': 'Nerium oleander',
        'safety_level': 'toxic',
        'nutrition_notes': 'TOXIC - Contains cardiac glycosides, extremely dangerous.',
        'feeding_frequency': 'NEVER',
        'description': 'Evergreen shrub with pink/white flowers. Highly poisonous.'
    },
    {
        'name': 'Avocado',
        'scientific_name': 'Persea americana',
        'safety_level': 'toxic',
        'nutrition_notes': 'TOXIC - Contains persin, harmful to reptiles.',
        'feeding_frequency': 'NEVER',
        'description': 'All parts including fruit, leaves, and pit are toxic.'
    },
    {
        'name': 'Tomato Leaves',
        'scientific_name': 'Solanum lycopersicum',
        'safety_level': 'toxic',
        'nutrition_notes': 'TOXIC - Contains solanine and tomatine alkaloids.',
        'feeding_frequency': 'NEVER',
        'description': 'Leaves and stems of tomato plants. Fruit in moderation only.'
    },
    {
        'name': 'Potato Leaves',
        'scientific_name': 'Solanum tuberosum',
        'safety_level': 'toxic',
        'nutrition_notes': 'TOXIC - Contains solanine, especially in green parts.',
        'feeding_frequency': 'NEVER',
        'description': 'Leaves, stems, and green potatoes contain toxic solanine.'
    },
    {
        'name': 'Rhubarb Leaves',
        'scientific_name': 'Rheum rhabarbarum',
        'safety_level': 'toxic',
        'nutrition_notes': 'TOXIC - High oxalic acid content, can cause kidney damage.',
        'feeding_frequency': 'NEVER',
        'description': 'Leaves contain dangerous levels of oxalic acid.'
    },
    {
        'name': 'Apple Seeds',
        'scientific_name': 'Malus domestica',
        'safety_level': 'toxic',
        'nutrition_notes': 'TOXIC - Seeds contain cyanogenic compounds.',
        'feeding_frequency': 'NEVER',
        'description': 'Apple flesh is safe, but remove all seeds and core.'
    }
]

def populate_plant_database():
    """Populate the plant database with curated tortoise plant data"""
    
    print("Populating plant database with curated Tortoise Table data...")
    
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        # Insert each plant
        inserted_count = 0
        for plant in TORTOISE_PLANTS:
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
                plant.get('description')
            ))
            inserted_count += 1
            print(f"  Added: {plant['name']} ({plant['safety_level']})")
        
        # Commit changes
        conn.commit()
        
        print(f"\nSuccessfully populated database with {inserted_count} plants!")
        
        # Show statistics
        cursor.execute('SELECT safety_level, COUNT(*) FROM plants GROUP BY safety_level')
        stats = cursor.fetchall()
        
        print("\nPlant safety statistics:")
        for safety, count in stats:
            print(f"  {safety.title()}: {count} plants")
        
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"ERROR: Failed to populate database: {e}")
        return False
    
    finally:
        conn.close()

def verify_database():
    """Verify the populated database"""
    print("\nVerifying plant database...")
    
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT COUNT(*) FROM plants')
        total = cursor.fetchone()[0]
        print(f"Total plants in database: {total}")
        
        # Show sample plants from each category
        for safety in ['safe', 'caution', 'toxic']:
            cursor.execute('''
                SELECT name, scientific_name 
                FROM plants 
                WHERE safety_level = ? 
                ORDER BY name 
                LIMIT 3
            ''', (safety,))
            
            samples = cursor.fetchall()
            print(f"\nSample {safety} plants:")
            for name, sci_name in samples:
                sci_display = f" ({sci_name})" if sci_name else ""
                print(f"  - {name}{sci_display}")
                
    except Exception as e:
        print(f"ERROR during verification: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    print("Tortoise Plant Database Population Tool")
    print("=" * 45)
    print("Data source: The Tortoise Table (thetortoisetable.org.uk)")
    print()
    
    success = populate_plant_database()
    if success:
        verify_database()
        print("\nPlant database ready for use!")
    else:
        print("\nDatabase population failed.")