from dotenv import load_dotenv
load_dotenv()

from flaskr.scraper import scraper

scraper.scrape()