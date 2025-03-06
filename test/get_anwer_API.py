import requests

from dotenv import load_dotenv
import os
from pathlib import Path

dotenv_path = Path('/home/nileshp/projects/dataFiller/app/.env')

# Load environment variables from the .env file (if present)
load_dotenv(dotenv_path=dotenv_path)

# Access environment variables as if they came from the actual environment
API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

headers = {"Authorization": f"Bearer {API_KEY}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": {
	"question": "How much funding raised by airbnb?",
	"context": "After moving to San Francisco in October 2007, roommates and former schoolmates Brian Chesky and Joe Gebbia came up with an idea of putting an air mattress in their living room and turning it into a bed and breakfast.[8] In February 2008, Nathan Blecharczyk, Chesky's former roommate, joined as the chief technology officer and the third co-founder of the new venture, which they named AirBed & Breakfast.[8][9] They put together a website that offered short-term living quarters and breakfast for those who were unable to book a hotel in the saturated market.[8] The site Airbedandbreakfast.com was launched on August 11, 2008.[10][11] The founders had their first customers in the summer of 2008, during the Industrial Design Conference held by Industrial Designers Society of America, where travelers had a hard time finding lodging in the city.[12] After the founders raised $30,000 by selling cereal named after the two candidates of the 2008 United States presidential election, Barack Obama and John McCain, mostly at the 2008 Democratic National Convention,[13][14][15] computer programmer Paul Graham invited the founders to the January 2009 winter training session of his startup incubator, Y Combinator, which provided them with training and $20,000 in funding in exchange for a 6% interest in the company.[8][16][17] With the website already built, they used the Y Combinator investment to fly to New York to meet users and promote the site.[15] They returned to San Francisco with a profitable business model to present to West Coast investors. By March 2009, the site had 10,000 users and 2,500 listings.[18] In March 2009, the name of the company was shortened to Airbnb.com to eliminate confusion over air mattresses; by then listings included entire rooms and properties.[8] By November 2010, out of 700,000 nights booked, 80% had occurred in the previous six months.[19] At the March 2011 South by Southwest conference, Airbnb won the 'app' award.[20] In November 2012, Airbnb launched 'Neighborhoods', a travel guide of 23 cities that helps travelers choose a neighborhood in which to stay based on certain criteria and personal preferences.[21]"
},
})

print(output)