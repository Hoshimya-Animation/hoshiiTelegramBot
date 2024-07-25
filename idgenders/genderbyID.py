# Import the Jikan class from the jikanpy library, which is used to interact with the MyAnimeList API
from jikanpy import Jikan
# Import the getIDAnime function from the mal_dbid module, which is presumably used to get the ID of an anime
from mal_dbid import getIDAnime
# Import the json module, which is used for working with JSON data
import json
# Import the os module, which provides a way of using operating system dependent functionality
import os
# Import the time module, which provides various time-related functions
import time

# Define a class named gendersIDs
class gendersIDs:
    # Define the constructor method for the class
    def __init__(self, animeIDS) -> None:
        # Initialize the animeID attribute with the provided animeIDS parameter
        self.animeID = animeIDS
        # Initialize an empty dictionary to store genders
        self.get_genders = {}
        # Initialize an empty string for gender
        self.gender = ''
        # Create an instance of the Jikan class with a specified base URL for the API
        self.contact = Jikan(selected_base='https://api.jikan.moe/v4/')
        # Initialize a list of anime genres
        self.list_genders = ['Action', 'Comedy', 'Horror', 'Sports', 'Adventure', 'Drama',
                             'Mystery', 'Supernatural', 'Avant Garde', 'Fantasy', 'Romance',
                             'Suspense', 'Award Winning', 'Girls Love', 'Sci-Fi', 'Boys Love',
                             'Gourmet', 'Slice of Life', 'Ecchi', 'Erotica', 'Hentai']
        # Initialize empty lists for each genre
        self.Action = []
        self.Comedy = []
        self.Horror = []
        self.Sports = []
        self.Adventure = []
        self.Drama = []
        self.Mystery = []
        self.Avant = []
        self.Fantasy = []
        self.Romance = []
        self.Supernatural = []
        self.Suspense = []
        self.Award = []
        self.Girls = []
        self.Sci = []
        self.Boys = []
        self.Gourmet = []
        self.Slice = []
        self.Erotica = []
        self.Ecchi = []
        self.Hentai = []
        # Initialize an empty list to store values of IDs
        self.values_ids = []
        # Initialize an empty dictionary for additional data
        self.dicm = {}

    # Define a method named commonList within the gendersIDs class
    def commonList(self, listg, id_g):
        # Create a dictionary that maps genre names to their corresponding lists
        genre_map = {
            'Action': self.Action,
            'Comedy': self.Comedy,
            'Horror': self.Horror,
            'Adventure': self.Adventure,
            'Sports': self.Sports,
            'Drama': self.Drama,
            'Mystery': self.Mystery,
            'Supernatural': self.Supernatural,
            'Avant Garde': self.Avant,
            'Fantasy': self.Fantasy,
            'Romance': self.Romance,
            'Suspense': self.Suspense,
            'Award Winning': self.Award,
            'Girls Love': self.Girls,
            'Sci-Fi': self.Sci,
            'Boys Love': self.Boys,
            'Gourmet': self.Gourmet,
            'Slice of Life': self.Slice,
            'Ecchi': self.Ecchi,
            'Erotica': self.Erotica,
            'Hentai': self.Hentai
        }
        # Iterate over each genre in the list of genres
        for g in self.list_genders:
            # If the genre is in the provided list and also in the genre_map dictionary
            if g in listg and g in genre_map:
                # Append the given ID to the corresponding genre list
                genre_map[g].append(id_g)
        # Extend the values_ids list with all values from the genre_map dictionary
        self.values_ids.extend(genre_map.values())
        # Return the updated values_ids list
        return self.values_ids
    # Define a method named listDic within the gendersIDs class
    def listDic(self):
        # Create a dictionary where each genre is mapped to its index in the list_genders
        self.dicm = {item: index for index, item, in enumerate(self.list_genders)}
        # Return the created dictionary
        return self.dicm
    
    # Define a method named uploadDict within the gendersIDs class
    def uploadDict(self):
        # Call the listDic method to populate the dicm dictionary
        self.listDic()
        # Create a dictionary mapping genres to their corresponding lists of IDs
        self.get_genders = {key: value for key, value in zip(self.dicm.keys(), self.values_ids)}
        # Return the created dictionary
        return self.get_genders
    
    # Define a method named returnJsonDict within the gendersIDs class
    def returnJsonDict(self):
        # Define the path to the JSON file
        path = './idsgen.json'
        # Check if the file already exists
        if os.path.isfile(path):
            # If the file exists, open it in write mode and dump the get_genders dictionary into it
            with open('idsgen.json', 'w') as file:
                json.dump(self.get_genders, file, indent=4)
        else:
            # If the file does not exist, create it and dump the get_genders dictionary into it
            with open('idsgen.json', 'a') as file:
                json.dump(self.get_genders, file, indent=4)
    
    # Define a method named runList within the gendersIDs class
    def runList(self):
        # Initialize counters i and r to 0
        i, r = 0, 0
        # Iterate over each anime ID in the animeID list
        for num in self.animeID:
            # If r is not equal to 3
            if r != 3:
                try:
                    # Fetch anime details using the Jikan API
                    ids = self.contact.anime(num)
                    # Extract the list of genre names from the fetched data
                    ll = [genre['name'] for genre in ids['data']['genres']]
                    # Call the commonList method to update genre lists with the current anime ID
                    self.commonList(ll, num)
                except:pass
                # Print the current registration number
                print("Registo: ", i + 1, flush=True)
                # Increment the counters i and r
                i += 1
                r += 1
            # If r is equal to 3
            elif r == 3:
                # Sleep for 3 seconds
                time.sleep(3)
                # Reset the counter r to 0
                r = 0
        # Call the uploadDict method to update the get_genders dictionary
        self.uploadDict()
        # Call the returnJsonDict method to save the dictionary to a JSON file
        self.returnJsonDict()

# Create an instance of the gendersIDs class with anime IDs obtained from the getIDAnime function
update_json = gendersIDs(getIDAnime())
# Call the runList method to process the anime IDs and update the JSON file
update_json.runList()
