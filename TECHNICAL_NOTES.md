# Technical Notes

## Dependencies and Known Issues

### Adafruit.IO Library (adafruit-io v2.8.0)

**Issue**: The Adafruit.IO library currently uses `pkg_resources` which is deprecated in setuptools>=81.

**Warning Message**: 
```
pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. 
The pkg_resources package is slated for removal as early as 2025-11-30.
```

**Current Solution**: 
- Warning suppression implemented in `utils/adafruit_io_utils.py`
- This is a temporary solution until the upstream library is updated

**Monitoring**: 
- Check for updates to adafruit-io library regularly
- Monitor: https://github.com/adafruit/Adafruit_IO_Python/issues
- Remove warning suppression when library is updated

**Alternative Solutions Considered**:
1. Pin setuptools<81 (not recommended - blocks other updates)
2. Switch to different IoT platform (significant code changes required)
3. Fork and update the library (maintenance burden)

**Status**: Using warning suppression as least invasive approach while waiting for upstream fix.

## Database Schema

The application uses SQLite with the following main tables:
- `users` - User management
- `tortoises` - Tortoise profiles  
- `feeding_records` - Feeding history
- `feeding_items` - What was fed in each session
- `health_records` - Health tracking
- `growth_records` - Growth measurements
- `habitat_readings` - Environmental data
- `care_reminders` - Task management
- `settings` - Configuration storage
- `plants` - Plant database

## Plant Database

### Current Implementation
- 4400+ plants with safety classifications, scientific names, nutrition notes
- Search and filter functionality (by name, safety level)
- Pagination for performance with large datasets
- Data sourced from authoritative botanical databases

### Data Sources
- **The Tortoise Table** (thetortoisetable.org.uk) - Primary safety classifications
- **Atlas NBN** - UK biodiversity data
- **GBIF Backbone** - Global biodiversity database  
- **Plants of the World Online** - Kew Gardens botanical database

### Future Enhancements
- **Offline Plant Photos**: Would require harvesting/licensing thousands of plant images
  - Leaf photos for identification
  - Flower photos for seasonal identification  
  - Full plant photos for context
  - Estimated storage: 5-15GB for comprehensive image database
- **Visual Plant ID**: Machine learning-based plant identification from user photos
- **Seasonal Availability**: Geographic and seasonal availability data
- **Local Plant Maps**: Integration with geographic databases for local plant finding

## Development Environment

- Python 3.13+
- PySide6 for Qt GUI
- SQLite for data storage
- Adafruit.IO for IoT connectivity
- Flask for photo upload server