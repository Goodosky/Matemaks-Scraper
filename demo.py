from matemaks_scraper import MatemaksScraper
from export_functions import *

"""
Import needed things:
from matemaks_scraper_class import MatemaksScraper
from export_functions import *

Init scrapper:
scraper = MatemaksScraper()

Use medthods:
- scraper.get_basic_matura_course()
- scraper.get_extended_matura_course()
- scraper.get_all_matura_course()
- scraper.get_all_matura_questions()
- scraper.get_lessons_data(url)
- scraper.get_questions(url)
- scraper.generate_data_for_matemaks_extension()

Close browser:
- scraper.close_browser()

Export data:
- export_to_json(data)
"""

# EXAMPLE:

# Init MatemaksScraper class, open browser and login to matemaks
scraper = MatemaksScraper()

scraper.generate_data_for_matemaks_extension()

# Close the browser
scraper.close_browser()
