import discord
import requests
import asyncio
import os
from keep_alive import keep_alive
from datetime import date, datetime

#Change the below lines

#List of species to filter out (example list put in)
filtered_species = {
  #Canada Goose,
  #American Robin
  }

# Region Code for eBird API (Example in place)
IL_REGION_CODE = #'US-IL'

# Replace YOUR_DISCORD_CHANNEL_ID with the ID of the channel where you want to send messages
DISCORD_CHANNEL_ID = #Enter your id here

#----------------
#CAUTION CHANGING ANYTHING BELOW THIS LINE

# To access your bot token
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_SECRET']

# to access eBird api key
EBIRD_API_KEY = os.environ['EBIRD_SECRET']

# URL to check for new rare bird sightings in Illinois
EBIRD_API_URL = f'https://api.ebird.org/v2/data/obs/{IL_REGION_CODE}/recent/notable?back=1&detail=full'

# Global variable to keep track of the last sighting ID
last_sighting_id = None

# Function to create a message embed for the bird sighting
def create_sighting_embed(sighting):
    embed = discord.Embed(
        title=sighting['comName']+ " | " + sighting['subnational2Name'] + " County",
        color=0x00ff00,  # You can customize the color here
    )
    embed.add_field(name="Observer", value=sighting['userDisplayName'], inline=False)
    embed.add_field(name="Location", value=sighting['locName'], inline=False)
    embed.add_field(name="Date", value=sighting['obsDt'], inline=False)
    embed.add_field(name="Check it out on eBird", value="https://ebird.org/checklist/" + sighting['subId'], inline=False)
    return embed

# Global variable to keep track of old sightings
old_sightings = []

# Function to fetch and process new bird sightings
async def check_for_new_sightings():
    try:
        response = requests.get(EBIRD_API_URL, headers={'X-eBirdApiToken': EBIRD_API_KEY})
        response.raise_for_status()
        sightings = response.json()
        
        for new_sighting in sightings:
            # Create a unique ID for the sighting using species code, county, and observation date
            new_sighting_id = new_sighting['speciesCode'] + new_sighting['subnational2Code'] + new_sighting['obsDt'][:10]

            if new_sighting_id not in old_sightings:
                old_sightings.append(new_sighting_id)

                # If the list exceeds 1000000 records, remove the oldest record(s) to maintain the limit
                if len(old_sightings) > 1000000:
                    old_sightings.pop(0)

                # Check if the species is not in the filtered list
                if new_sighting['comName'] not in filtered_species:
                    # Create the message embed for the sighting
                    embed = create_sighting_embed(new_sighting)

                    # Send the embed message to Discord channel
                    channel = client.get_channel(int(DISCORD_CHANNEL_ID))
                    await channel.send(embed=embed)
    except Exception as e:
        print(f"Error: {e}")


# Initialize the Discord client
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Event to run when the bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    # Run the check_for_new_sightings function every 2 minutes
    while True:
        await check_for_new_sightings()
        await asyncio.sleep(120)  # 120 seconds = 2 minutes

# Run the bot with the provided token
keep_alive()
client.run(DISCORD_BOT_TOKEN)
