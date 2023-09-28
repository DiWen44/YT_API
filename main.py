import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

chanName = input("ENTER CHANNEL NAME: ")

