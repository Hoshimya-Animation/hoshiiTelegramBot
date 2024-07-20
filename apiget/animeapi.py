import re  # Importing the 're' module for regular expression operations
import random  # Importing the 'random' module for generating random numbers
import json  # Importing the 'json' module for working with JSON data
from jikanpy import Jikan  # Importing the 'Jikan' class from the 'jikanpy' module for interacting with the Jikan API (an unofficial MyAnimeList API)
from googletrans import Translator  # Importing the 'Translator' class from the 'googletrans' module for translating text using Google Translate
import os #Importing the 'os' module for working with Operating System
class AnimeApp:
    """
    A class to represent an Anime application.

    Attributes
    ----------
    languague_app : str
        The language of the app.
    request_api : Jikan
        An instance of the Jikan API initialized with the specified base URL.
    option : str
        User options.
    animeSource : str
        The source of the anime.
    translator : Translator
        An instance of the Google Translator.
    translated : str
        Translated text.
    __animeTitle : str
        The title of the anime (private).
    __animeTitle_Japanese : str
        The title of the anime in Japanese (private).
    __genderAnime : str
        The genre of the anime (private).
    __aired : str
        The airing date of the anime (private).
    __episodes : str
        The number of episodes (private).
    __score : str
        The score of the anime (private).
    __ratingData : str
        The rating data (private).
    __animeId : int
        The ID of the anime (private).
    __synopsis : str
        The synopsis of the anime (private).
    __status : str
        The status of the anime (private).
    __types : str
        The type of the anime (private).
    __urlPicture : str
        The URL of the anime picture (private).
    animeData : list
        A list to store anime data.
    animeSuggest : list
        A list to store suggested anime.
    idDBGender : int
        The ID of the gender in the database.

    Methods
    -------
    __init__():
        Initializes the AnimeApp with default values.
    """

    def __init__(self):
        """
        Initializes the AnimeApp with default values.
        """
        self.languague_app = str  # Variable to store the language of the app
        self.request_api = Jikan(selected_base='https://api.jikan.moe/v4/')  # Initialize Jikan API with the specified base URL
        self.option = str  # Variable to store user options
        self.animeSource = ''  # Variable to store the source of the anime
        self.translator = Translator()  # Initialize the Google Translator
        self.translated = str  # Variable to store translated text
        self.__animeTitle = str  # Private variable to store the anime title
        self.__animeTitle_Japanese = str  # Private variable to store the anime title in Japanese
        self.__genderAnime = str  # Private variable to store the genre of the anime
        self.__aired = str  # Private variable to store the airing date of the anime
        self.__episodes = str  # Private variable to store the number of episodes
        self.__score = str  # Private variable to store the score of the anime
        self.__ratingData = str  # Private variable to store the rating data
        self.__animeId = int  # Private variable to store the anime ID
        self.__synopsis = str  # Private variable to store the synopsis of the anime
        self.__status = str  # Private variable to store the status of the anime
        self.__types = str  # Private variable to store the type of the anime
        self.__urlPicture = str  # Private variable to store the URL of the anime picture
        self.animeData = []  # List to store anime data
        self.animeSuggest = []  # List to store suggested anime
        self.idDBGender = int  # Variable to store the ID of the gender in the database

    def changeLanguage(self, language):
        """
        Change the language of the app.

        Parameters
        ----------
        language : str
            The new language to set for the app.

        Returns
        -------
        str
            The updated language of the app.
        """
        self.languague_app = language.lower()
        return self.languague_app

    def changeAnimeSource(self, animeNameSource):
        """
        Change the source of the anime.

        Parameters
        ----------
        animeNameSource : str
            The new source name for the anime.

        Returns
        -------
        str
            The updated anime source.
        """
        self.animeSource = animeNameSource
        return self.animeSource

    def getOption(self, option):
        """
        Set an option for the app.

        Parameters
        ----------
        option : str
            The option to set for the app.

        Returns
        -------
        str
            The updated option.
        """
        self.option = option.lower()
        return self.option

    def __dataTranslated(self, sourceData, srcLanguage) -> str:
        """
        Translate the source data from the source language to the app's language.

        Parameters
        ----------
        sourceData : str
            The data to be translated.
        srcLanguage : str
            The source language of the data.

        Returns
        -------
        str
            The translated and cleaned data.
        """
        sourceData = self.translator.translate(sourceData, src=srcLanguage, dest=self.languague_app).text
        new_sourceData = sourceData.replace('\u200b', '').replace('\n\n', '')
        return str(new_sourceData)


    def __dataRating(self) -> str:
        # Process the rating data.
        # Search for specific rating keywords in '__ratingData'.
        wordsFine = re.search(r'G|PG-13|PG|pg-13|pg|Rx - Hentai|R - 17+|R+|R', self.__ratingData, re.IGNORECASE)
        matched = wordsFine.group()  # Get the matched rating keyword
        self.__ratingData = str(matched).capitalize()  # Capitalize the matched rating keyword
        # Check if the rating is 'Rx - Hentai' and translate a warning message if true.
        if self.__ratingData == 'Rx - Hentai' or self.__ratingData == 'Rx - hentai':
            self.__ratingData = self.__dataTranslated('The genre Hentai is not strongly recommended for audiences under 18 years.', 'en')
            return self.__ratingData  # Return the translated warning message
        else:
            return self.__ratingData  # Return the processed rating data
    def __fillAnimeData(self, rand) -> list:
        """
        Fills the anime data based on the source and random flag.
        
        Parameters:
        rand (bool): A flag to determine if the data should be fetched randomly or based on the source.
        
        Returns:
        list: A list containing the anime data.
        """
        if self.animeSource != '' and rand == False:  # Check if the anime source is not empty and rand is False
            search = self.request_api.search('anime', self.animeSource)  # Search for the anime using the Jikan API
            self.__animeId = search['data'][0]['mal_id']  # Get the anime ID from the search results
            dataAnime = self.request_api.anime(self.__animeId)  # Fetch detailed anime data using the anime ID
            self.__animeTitle = self.__dataTranslated(dataAnime['data']['title_japanese'], 'ja')  # Translate the anime title to Japanese
            self.__animeTitle_Japanese = dataAnime['data']['title_japanese']  # Store the original Japanese title
            listGenders = [gen['name'] for gen in dataAnime['data']['genres']]  # Extract the genres of the anime
            self.translated_gender = [self.__dataTranslated(g, 'en') for g in listGenders]  # Translate the genres to English
            self.__genderAnime = "#" + "#".join(map(str, self.translated_gender))  # Format the genres as a string
            self.__aired = self.__dataTranslated(str(dataAnime['data']['aired']['string']), 'en')  # Translate the airing date
            self.__episodes = str(dataAnime['data']['episodes'])  # Store the number of episodes
            self.__score = str(dataAnime['data']['score'])  # Store the score of the anime
            self.__ratingData = str(dataAnime['data']['rating'])  # Store the rating data
            self.__dataRating()  # Process the rating data
            self.__status = self.__dataTranslated(dataAnime['data']['status'], 'en')  # Translate the status of the anime
            self.__types = dataAnime['data']['type']  # Store the type of the anime
            self.__synopsis = self.__dataTranslated(dataAnime['data']['synopsis'], 'en')  # Translate the synopsis
            self.__urlPicture = str(dataAnime['data']['images']['jpg']['image_url'])  # Store the URL of the anime picture
            self.animeData.extend([
                self.__animeTitle, self.__animeTitle_Japanese, self.__types,
                self.__genderAnime, self.__aired, self.__episodes,
                self.__score, self.__ratingData, self.__status,
                self.__synopsis, self.__urlPicture
            ])  # Add all the collected data to the animeData list
            return self.animeData  # Return the list containing the anime data
        elif self.animeSource == '' and rand == True:  # Check if the anime source is empty and rand is True
            id_anime_rand = self.request_api.random('anime')  # Fetch a random anime using the Jikan API
            try:
                self.__animeId = id_anime_rand['data']['mal_id']  # Get the anime ID from the random anime data
                dataAnime = self.request_api.anime(self.__animeId)  # Fetch detailed anime data using the anime ID
                self.__animeTitle = self.__dataTranslated(dataAnime['data']['title_japanese'], 'ja')  # Translate the anime title to Japanese
                self.__animeTitle_Japanese = dataAnime['data']['title_japanese']  # Store the original Japanese title
                listGenders = [gen['name'] for gen in dataAnime['data']['genres']]  # Extract the genres of the anime
                self.translated_gender = [self.__dataTranslated(g, 'en') for g in listGenders]  # Translate the genres to English
                self.__genderAnime = "#" + "#".join(map(str, self.translated_gender))  # Format the genres as a string
                self.__aired = self.__dataTranslated(str(dataAnime['data']['aired']['string']), 'en')  # Translate the airing date
                self.__episodes = str(dataAnime['data']['episodes'])  # Store the number of episodes
                self.__score = str(dataAnime['data']['score'])  # Store the score of the anime
                self.__ratingData = str(dataAnime['data']['rating'])  # Store the rating data
                self.__dataRating()  # Process the rating data
                self.__status = self.__dataTranslated(dataAnime['data']['status'], 'en')  # Translate the status of the anime
                self.__types = dataAnime['data']['type']  # Store the type of the anime
                self.__synopsis = self.__dataTranslated(dataAnime['data']['synopsis'], 'en')  # Translate the synopsis
                self.__urlPicture = str(dataAnime['data']['images']['jpg']['image_url'])  # Store the URL of the anime picture
                self.animeData.extend([
                    self.__animeTitle, self.__animeTitle_Japanese, self.__types,
                    self.__genderAnime, self.__aired, self.__episodes,
                    self.__score, self.__ratingData, self.__status,
                    self.__synopsis, self.__urlPicture
                ])  # Add all the collected data to the animeData list
            except:
                pass  # Handle any exceptions that occur
            return self.animeData  # Return the list containing the anime data

    def __getAnimeByIDGender(self, gender) -> int:
        """
        Retrieves an anime ID based on the provided gender.

        Args:
            gender (str): The gender for which to retrieve an anime ID.

        Returns:
            int: The ID of the anime corresponding to the provided gender.
        """
        js_file = os.path.join(os.getcwd(),'idgenders/idsgen.json') # Change directory and find the file
        file = open(js_file)  # Open the JSON file containing gender IDs
        idsGen = json.load(file)  # Load the JSON data into a dictionary
        self.idDBGender = random.choice(idsGen[str(gender)])  # Select a random ID from the list corresponding to the provided gender
        return self.idDBGender  # Return the selected anime ID
    def __getSuggestions(self, gender) -> list:
        """
        Retrieves a list of suggested anime details based on the provided gender.

        Args:
            gender (str): The gender for which to retrieve anime suggestions.

        Returns:
            list: A list containing details of the suggested anime.
        """
        self.__getAnimeByIDGender(gender=gender)  # Retrieve an anime ID based on the provided gender
        try:
            setAnimeID = self.request_api.anime(self.idDBGender)  # Fetch anime details using the retrieved anime ID
            self.__animeId = setAnimeID['data']['mal_id']  # Extract the anime ID from the fetched data
            dataAnime = self.request_api.anime(self.__animeId)  # Fetch detailed anime data using the anime ID
            self.__animeTitle = self.__dataTranslated(dataAnime['data']['title_japanese'], 'ja')  # Translate the Japanese title of the anime
            self.__animeTitle_Japanese = dataAnime['data']['title_japanese']  # Store the Japanese title of the anime
            listGenders = [gen['name'] for gen in dataAnime['data']['genres']]  # Extract the list of genres from the anime data
            self.translated_gender = [self.__dataTranslated(g, 'en') for g in listGenders]  # Translate each genre to English
            self.__genderAnime = "#" + "#".join(map(str, self.translated_gender))  # Format the translated genres as a string
            self.__aired = self.__dataTranslated(str(dataAnime['data']['aired']['string']), 'en')  # Translate the airing date of the anime
            self.__episodes = str(dataAnime['data']['episodes'])  # Store the number of episodes as a string
            self.__score = str(dataAnime['data']['score'])  # Store the score of the anime as a string
            self.__ratingData = str(dataAnime['data']['rating'])  # Store the rating data of the anime as a string
            self.__dataRating()  # Process the rating data
            self.__status = self.__dataTranslated(dataAnime['data']['status'], 'en')  # Translate the status of the anime
            self.__types = dataAnime['data']['type']  # Store the type of the anime
            self.__synopsis = self.__dataTranslated(dataAnime['data']['synopsis'], 'en')  # Translate the synopsis of the anime
            self.__urlPicture = str(dataAnime['data']['images']['jpg']['image_url'])  # Store the URL of the anime picture
            self.animeSuggest.extend([
                self.__animeTitle, self.__animeTitle_Japanese, self.__types,
                self.__genderAnime, self.__aired, self.__episodes,
                self.__score, self.__ratingData, self.__status,
                self.__synopsis, self.__urlPicture
            ])  # Add all the extracted and translated details to the anime suggestions list
        except:
            pass  # Handle any exceptions that occur during the process
        return self.animeSuggest  # Return the list of suggested anime details
    def getSuggestbyGenre(self, genderChoose) -> list:
        """
        Get a list of anime suggestions based on the chosen genre.

        Parameters
        ----------
        genderChoose : str
            The genre chosen by the user.

        Returns
        -------
        list
            A list of suggested anime.
        """
        while self.__getSuggestions(genderChoose) == []:
            continue  # Keep trying until suggestions are found
        return self.animeSuggest

    def getAnimeData(self) -> list:
        """
        Get anime data based on the source and user option.
    
        Returns
        -------
        list
            A list of anime data.
        """
        if self.animeSource != '' and self.option == 'useranime':  # Check if the anime source is specified and the option is 'useranime'
            try:
                self.__fillAnimeData(False)  # Fill anime data without random selection
                return self.animeData  # Return the filled anime data
            except:
                return []  # Return an empty list if an exception occurs
        elif self.animeSource == '' and self.option == 'randanime':  # Check if the anime source is not specified and the option is 'randanime'
            while self.__fillAnimeData(True) == []:  # Keep trying to fill data with random selection until successful
                continue  # Continue the loop until data is filled
            return self.animeData  # Return the filled anime data
