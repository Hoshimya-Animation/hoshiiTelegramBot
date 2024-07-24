import logging  # Import the logging module for handling logs
from difflib import SequenceMatcher  # Import SequenceMatcher for string similarity comparison
from googletrans import Translator  # Import Translator from googletrans for text translation
from apiget.animeapi import AnimeApp  # Import AnimeApp from apiget.animeapi for anime-related data
from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup  # Import Telegram-related classes
from telegram.ext import (
    Application,  # Import Application for handling different types of interactions
    CommandHandler,  # Import CommandHandler for handling commands
    ContextTypes,  # Import ContextTypes for context management
    CallbackQueryHandler,  # Import CallbackQueryHandler for handling callback queries
    CallbackContext,  # Import CallbackContext for context in callback queries
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)  # Set up logging configuration

logging.getLogger("httpx").setLevel(logging.WARNING)  # Set log level for httpx module

# Create a logger for this module
logger = logging.getLogger(__name__)  # Initialize logger for this script/module


class telegramBot:
    def __init__(self) -> None:
        # Initialize a dictionary to map language names to their corresponding codes
        self.dict_languages = {
                "Español":"es",
                "English":"en",
                "Français":"fr",
                "Deutsch":"de",
                "Português":"pt",
                "Italiano":"it",
                "Русский":"ru",
                "عرب":"ar",
                "हिंदू":"hi",
                "Română":"ro",
                "日本語":"ja",
                "简体中文":"zh-tw",
                "한국인":"ko"
            }
        # Define a dictionary of bot commands and their descriptions
        self.commands_dictionary = {
            "start":"The bot starts ₍^ >ヮ<^₎ .ᐟ.ᐟ",
            "language":f"Change language of the Bot 🇪🇸➡️🇬🇧",
            "request": f"+'name'. Request a new anime from our database or if it's available on MyAnimeList list 🗄 (japanese or english)",
            "random": f"Random information about an anime 🎲",
            "hoshii": f"+'gender'. Anime suggestion by the gender 🌍🍱 (Action, Comedy, Horror, Sports, Adventure, Drama, Mystery, Supernatural, Avant Garde, Fantasy, Romance,Suspense, Award Winning, Girls Love, Sci-Fi, Boys Love,Gourmet, Slice of Life, Ecchi, Erotica, Hentai)",
            "help":f"Give you information about my functions 🆘❔"
        }
        # List of anime genres
        self.__genders = ['Action', 'Comedy', 'Horror', 'Sports', 'Adventure', 'Drama',
                        'Mystery', 'Supernatural', 'Avant Garde', 'Fantasy', 'Romance',
                        'Suspense', 'Award Winning', 'Girls Love', 'Sci-Fi', 'Boys Love',
                        'Gourmet', 'Slice of Life', 'Ecchi', 'Erotica', 'Hentai']
        # Initialize language-related attributes
        self.language = str
        self.translator = Translator()
        self.sourceLanguage = "en"
        # Placeholder for data 
        self.data = str
        # Initialize an empty dictionary to store information messages
        self.info_message = {
            f"🎥 {'Title'}": "",
            f"🎌 {'Japanese Title'}": "",
            f"📺 {'Type'}": "",
            f"🏷️ {'Genre'}":"",
            f"🗓️ {'Aired'}": "",
            f"🖥️ {'Episodes'}": "",
            f"⭐ {'Score'}": "",
            f"🔞 {'Rating'}": "",
            f"📜 {'Status'}": "",
            f"📝 {'Synopsis'}": ""
        }
    def getAbbreviation(self,lang):
        """
        Returns the abbreviation for the specified language
        Args:
            lang (str): Language code (e.g., 'en' for English)
        Returns:
            str: Language abbreviation
        """
        self.language = lang
        return self.language
    def showHelp(self):
        """
        Displays a help message with available commands
        Returns:
            dict: Dictionary of commands and their descriptions
        """
        if self.language == str:
            return self.commands_dictionary
        else:
            # Translate command descriptions if language is not English
            self.commands_dictionary = {x: self.translatedData(y) for x,y in self.commands_dictionary}
            return self.commands_dictionary
    def translatedData(self,data) -> str:
        """
        Translates data from the source language to the specified language
        Args:
            data (str): Text to be translated
        Returns:
            str: Translated text
        """
        self.data = self.translator.translate(data,src=self.sourceLanguage,dest=self.language).text
        self.data = self.data.replace('\u200b', '').replace('\n\n', '')
        return self.data
    def getSimilarity(self,gender):
        """
        Finds a gender match based on similarity
        Args:
            gender (str): Gender to compare
        Returns:
            str: Matching gender (if found)
        """
        gender_get  = next((i for i in self.__genders if SequenceMatcher(None, i.lower(), gender).ratio() > 0.5), '')
        return gender_get
# Instances
telebot = telegramBot() # Create an instance of the TelegramBot class
animeApp = AnimeApp() # Create an instance of the AnimeApp class
#Functons
"""Start Command"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the start command for the bot
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    user = update.message.chat
    if telebot.language != str:
        # Send a translated welcome message if the language is not English
        await context.bot.send_message(chat_id=update.effective_chat.id, text= telebot.translatedData(f"Hi, {user.first_name}!!♡⸜(˃ ᵕ ˂ )⸝ I’m Hoshimya ✨, but you can call me ‘mya-chan’ if you prefer (ᵕ—ᴗ—). I’m at your service! 🌟\nWhat does this bot do? ❓ Well, when boredom strikes, I’ll whisk you away to the world of anime with a recommendation. Share your preferred genre, and I’ll conjure up a suggestion! I understand around 10 languages. 🌐\nWhile there are some things I can’t do, I’ll give my best shot.\nIf you’re a programmer itching to improve something new, go ahead! 👨‍💻👩‍💻 Check out the repository on GitHub. 🐈‍⬛ https://github.com/Hoshimya-Animation/hoshiTelegramBot \nAnd lastly, like the stars and constellations, I’ll be here for you until eternity. ( > 〰 < )♡✨🌃🌍"))
    else:
        # Send the default welcome message in English
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi, {user.first_name}!!♡⸜(˃ ᵕ ˂ )⸝ I’m Hoshimya ✨, but you can call me ‘mya-chan’ if you prefer (ᵕ—ᴗ—). I’m at your service! 🌟\nWhat does this bot do? ❓ Well, when boredom strikes, I’ll whisk you away to the world of anime with a recommendation. Share your preferred genre, and I’ll conjure up a suggestion! I understand around 10 languages. 🌐\nWhile there are some things I can’t do, I’ll give my best shot.\nIf you’re a programmer itching to improve something new, go ahead! 👨‍💻👩‍💻 Check out the repository on GitHub. 🐈‍⬛ https://github.com/Hoshimya-Animation/hoshiTelegramBot \nAnd lastly, like the stars and constellations, I’ll be here for you until eternity. ( > 〰 < )♡✨🌃🌍")
"""Change commands"""
async def changeCommands(application:Application) -> None:
    """
    Updates the bot's commands and chat menu button
    Args:
        application (Application): The application instance
    """
    command = [BotCommand((key),(value)) for key,value in telebot.commands_dictionary.items()]
    await application.bot.set_my_commands(command)
    await application.bot.set_chat_menu_button()

"""Start command menu"""
async def language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends a message with three inline buttons attached for language selection.
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    keyboard = [
        [
            InlineKeyboardButton(f"Español 🇲🇽", callback_data="Español"),
            InlineKeyboardButton(f"English 🇬🇧🇺🇸", callback_data="English"),
            InlineKeyboardButton(f"Français 🇫🇷", callback_data="Français"),
            
        ],
        [   InlineKeyboardButton(f"Deutsch 🇩🇪", callback_data="Deutsch"),
            InlineKeyboardButton(f"Português 🇵🇹🇧🇷", callback_data="Português"),
            InlineKeyboardButton(f"Italiano 🇮🇹", callback_data="Italiano"),
        ],
        [
            InlineKeyboardButton(f"Русский 🇷🇺", callback_data="Русский"),
            InlineKeyboardButton(f"عرب 🇸🇦", callback_data="عرب"),
            InlineKeyboardButton(f"हिंदू 🇮🇳", callback_data="हिंदू"),
        ],
        [
            InlineKeyboardButton(f"Română 🇷🇴", callback_data="Română"),
            InlineKeyboardButton(f"日本語 🇯🇵", callback_data="日本語"),
            InlineKeyboardButton(f"简体中文 🇨🇳", callback_data="简体中文"),
            InlineKeyboardButton(f"한국인 🇰🇷", callback_data="한국인"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if telebot.language == str:
        await update.message.reply_text("Please choose:", reply_markup=reply_markup)
    else:
        await update.message.reply_text(telebot.translatedData("Please choose:"), reply_markup=reply_markup)
"""Button query"""
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Parses the CallbackQuery and updates the message text.
    
    Args:
        update (Update): The update received from Telegram.
        context (ContextTypes.DEFAULT_TYPE): The context object.
    """
    query = update.callback_query
    await query.answer()
    if query.data in telebot.dict_languages:
        # Get the language from the query data
        language = telebot.dict_languages[query.data]
        telebot.getAbbreviation(lang=language)
        # Get the abbreviation for the language
        animeApp.changeLanguage(language)
        # Change the language in the animeApp
        await query.edit_message_text(text=f"{telebot.translatedData("Selected option")}: {query.data}")
"""
Request Random Anime Function

This function handles a user's request for a random anime recommendation.
It interacts with an external anime application to retrieve data and sends
the information back to the user via a Telegram bot.
"""
async def requestRandom(update: Update, context: CallbackContext) -> None:
    """
    Stores the info about the user and ends the conversation.

    Parameters:
    update (Update): The update object that contains all the information about the incoming update.
    context (CallbackContext): The context object that contains the bot's data and helper functions.
    """
    # Check if the language setting in the telebot is set to a string (indicating English)
    if telebot.language == str:
        # Change the language of the anime application to English
        animeApp.changeLanguage('en')
        # Request a random anime from the anime application
        animeApp.getOption('randanime')
        # Get the anime data from the anime application
        animedata = animeApp.getAnimeData()
        # Create a help_info string with the anime data formatted as "key: value"
        help_info = '\n'.join(f'{k}: {v}'for k,v in zip(telebot.info_message.keys(),animedata))
        # If the help_info string is longer than 1000 characters, truncate it and add ellipses
        if len(help_info)>=1000:help_info = help_info[0:997]+"..."
        # Check if the anime is categorized as hentai or erotica
        if ('#Hentai' in animedata[3] or '#hentai' in animedata[3]) or ('#Erotica' in animedata[3] or '#erotica' in animedata[3]):
            try:
                # Notify the user that an anime suggestion is being sent
                await update.message.reply_text("Alright! Maybe you mean this anime.")
                # Send the anime image and information as a photo with a spoiler warning
                await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=True)
            except:
                # If an error occurs, notify the user
                await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
        else:
            try:
                # Notify the user that an anime suggestion is being sent
                await update.message.reply_text("Alright! Maybe you mean this anime.")
                # Send the anime image and information as a photo without a spoiler warning
                await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=False)
            except:
                # If an error occurs, notify the user
                await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
    elif telebot.language != str:
        # If the language setting in the telebot is not a string, use the set language
        animeApp.changeLanguage(telebot.language)
        # Request a random anime from the anime application
        animeApp.getOption('randanime')
        # Get the anime data from the anime application
        animedata = animeApp.getAnimeData()
        # Create a help_info string with the anime data formatted as "translated key: value"
        help_info = '\n'.join(f'{telebot.translatedData(k)}: {v}'for k,v in zip(telebot.info_message.keys(),animedata))
        # If the help_info string is longer than 1000 characters, truncate it and add ellipses
        if len(help_info)>=1000:help_info = help_info[0:997]+"..."
        # Check if the anime is categorized as hentai or erotica
        if ('#Hentai' in animedata[3] or '#hentai' in animedata[3]) or ('#Erotica' in animedata[3] or '#erotica' in animedata[3]):
            try:
                # Notify the user that an anime suggestion is being sent
                await update.message.reply_text(telebot.translatedData("Alright! Maybe you mean this anime."))
                # Send the anime image and information as a photo with a spoiler warning
                await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=True)
            except:
                # If an error occurs, notify the user
                await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
        else:
            try:
                # Notify the user that an anime suggestion is being sent
                await update.message.reply_text(telebot.translatedData("Alright! Maybe you mean this anime."))
                # Send the anime image and information as a photo without a spoiler warning
                await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=False)
            except:
                # If an error occurs, notify the user
                await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
"""
Request Anime by User Function

This function handles a user's request for a specific anime recommendation.
It interacts with an external anime application to retrieve data based on the user's input and sends
the information back to the user via a Telegram bot.
"""
async def requestAnime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the user's request for an anime by name.

    Parameters:
    update (Update): The update object that contains all the information about the incoming update.
    context (ContextTypes.DEFAULT_TYPE): The context object that contains the bot's data and helper functions.
    """
    # Get the user's input text and split it into command and anime name
    user_input = update.message.text.split(maxsplit=1)
    # Check if the user provided an anime name
    if len(user_input) > 1:
        name = user_input[1]
        # Check if the language setting in the telebot is set to a string (indicating English)
        if telebot.language == str:
            # Change the language of the anime application to English
            animeApp.changeLanguage('en')
            # Change the anime source in the anime application to the user's input
            animeApp.changeAnimeSource(str(name))
            try:
                # Request the user-specified anime from the anime application
                animeApp.getOption('useranime')
                # Get the anime data from the anime application
                animedata = animeApp.getAnimeData()
                # Create a help_info string with the anime data formatted as "key: value"
                help_info = '\n'.join(f'{k}: {v}'for k,v in zip(telebot.info_message.keys(),animedata))
                # If the help_info string is longer than 1000 characters, truncate it and add ellipses
                if len(help_info)>=1000:help_info = help_info[0:997]+"..."
                # Check if the anime is categorized as hentai or erotica
                if ('#Hentai' in animedata[3] or '#hentai' in animedata[3]) or ('#Erotica' in animedata[3] or '#erotica' in animedata[3]):
                    try:
                        # Notify the user that an anime suggestion is being sent
                        await update.message.reply_text("Alright! Maybe you mean this anime.")
                        # Send the anime image and information as a photo with a spoiler warning
                        await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=True)
                    except:
                        # If an error occurs, notify the user
                        await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
                else:
                    try:
                        # Notify the user that an anime suggestion is being sent
                        await update.message.reply_text("Alright! Maybe you mean this anime.")
                        # Send the anime image and information as a photo without a spoiler warning
                        await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=False)
                    except:
                        # If an error occurs, notify the user
                        await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
            except:
                # If an error occurs, notify the user
                await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
        elif telebot.language != str:
            # If the language setting in the telebot is not a string, use the set language
            animeApp.changeLanguage(telebot.language)
            # Change the anime source in the anime application to the user's input
            animeApp.getOption('useranime')
            try:
                # Request the user-specified anime from the anime application
                animeApp.changeAnimeSource(name)
                # Get the anime data from the anime application
                animedata = animeApp.getAnimeData()
                # Create a help_info string with the anime data formatted as "translated key: value"
                help_info = '\n'.join(f'{telebot.translatedData(k)}: {v}'for k,v in zip(telebot.info_message.keys(),animedata))
                # If the help_info string is longer than 1000 characters, truncate it and add ellipses
                if len(help_info)>=1000:help_info = help_info[0:997]+"..."
                # Check if the anime is categorized as hentai or erotica
                if ('#Hentai' in animedata[3] or '#hentai' in animedata[3]) or ('#Erotica' in animedata[3] or '#erotica' in animedata[3]):
                    try:
                        # Notify the user that an anime suggestion is being sent
                        await update.message.reply_text(telebot.translatedData("Alright! Maybe you mean this anime."))
                        # Send the anime image and information as a photo with a spoiler warning
                        await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=True)
                    except:
                        # If an error occurs, notify the user
                        await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
                else:
                    try:
                        # Notify the user that an anime suggestion is being sent
                        await update.message.reply_text(telebot.translatedData("Alright! Maybe you mean this anime."))
                        # Send the anime image and information as a photo without a spoiler warning
                        await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=False)
                    except:
                        # If an error occurs, notify the user
                        await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
            except:
                # If an error occurs, notify the user
                await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
    else:
        # If the user did not provide an anime name, prompt them to type an anime name
        if telebot.language == str:
            response = "Type your anime (ෆ˙ᵕ˙ෆ)♡"
            await update.message.reply_text(response)
        else:
            response = telebot.translatedData("Type your anime (ෆ˙ᵕ˙ෆ)♡")
            await update.message.reply_text(response)

"""
Request Anime by Gender Function

This function handles a user's request for an anime recommendation by genre.
It interacts with an external anime application to retrieve data based on the user's input and sends
the information back to the user via a Telegram bot.
"""
async def requestgender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the user's request for an anime by genre.

    Parameters:
    update (Update): The update object that contains all the information about the incoming update.
    context (ContextTypes.DEFAULT_TYPE): The context object that contains the bot's data and helper functions.
    """
    # Get the user's input text and split it into command and genre name
    user_input = update.message.text.split(maxsplit=1)
    # Check if the user provided a genre name
    if len(user_input) > 1:
        name = user_input[1]
        # Check if the language setting in the telebot is set to a string (indicating English)
        if telebot.language == str:
            # Change the language of the anime application to English
            animeApp.changeLanguage('en')
            # Get the genre that closely matches the user's input
            gender_ = telebot.getSimilarity(name)
            # If a matching genre is found
            if gender_!='':
                try:
                    # Request anime suggestions by genre from the anime application
                    animedata = animeApp.getSuggestbyGenre(str(gender_))
                    # Create a help_info string with the anime data formatted as "key: value"
                    help_info = '\n'.join(f'{k}: {v}'for k,v in zip(telebot.info_message.keys(),animedata))
                    # If the help_info string is longer than 1000 characters, truncate it and add ellipses
                    if len(help_info)>=1000:help_info = help_info[0:997]+"..."
                    # Check if the anime is categorized as hentai or erotica
                    if ('#Hentai' in animedata[3] or '#hentai' in animedata[3]) or ('#Erotica' in animedata[3] or '#erotica' in animedata[3]):
                        try:
                            # Notify the user that an anime suggestion is being sent
                            await update.message.reply_text("Alright! Maybe you mean this anime.")
                            # Send the anime image and information as a photo with a spoiler warning
                            await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=True)
                        except:
                            # If an error occurs, notify the user
                            await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
                    else:
                        try:
                            # Notify the user that an anime suggestion is being sent
                            await update.message.reply_text("Alright! Maybe you mean this anime.")
                            # Send the anime image and information as a photo without a spoiler warning
                            await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=False)
                        except:
                            # If an error occurs, notify the user
                            await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
                except:
                    # If an error occurs, notify the user
                    await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
            else:
                # If no matching genre is found, notify the user
                await update.message.reply_text("Error! Maybe your gender is not into the list. ( ˶°ㅁ°) !!\nPlease use the command /help to show the genders are available. (˶ᵔ ᵕ ᵔ˶)")
        elif telebot.language != str:
            # If the language setting in the telebot is not a string, use the set language
            animeApp.changeLanguage(telebot.language)
            # Get the genre that closely matches the user's input
            gender_ = telebot.getSimilarity(name)
            # If a matching genre is found
            if gender_!='':
                try:
                    # Request anime suggestions by genre from the anime application
                    animedata = animeApp.getSuggestbyGenre(str(gender_))
                    # Create a help_info string with the anime data formatted as "translated key: value"
                    help_info = '\n'.join(f'{k}: {v}'for k,v in zip(telebot.info_message.keys(),animedata))
                    # If the help_info string is longer than 1000 characters, truncate it and add ellipses
                    if len(help_info)>=1000:help_info = help_info[0:997]+"..."
                    # Check if the anime is categorized as hentai or erotica
                    if ('#Hentai' in animedata[3] or '#hentai' in animedata[3]) or ('#Erotica' in animedata[3] or '#erotica' in animedata[3]):
                        try:
                            # Notify the user that an anime suggestion is being sent
                            await update.message.reply_text(telebot.translatedData("Alright! Maybe you mean this anime."))
                            # Send the anime image and information as a photo with a spoiler warning
                            await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=True)
                        except:
                            # If an error occurs, notify the user
                            await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
                    else:
                        try:
                            # Notify the user that an anime suggestion is being sent
                            await update.message.reply_text(telebot.translatedData("Alright! Maybe you mean this anime."))
                            # Send the anime image and information as a photo without a spoiler warning
                            await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=False)
                        except:
                            # If an error occurs, notify the user
                            await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
                except:
                    # If an error occurs, notify the user
                    await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
            else:
                # If no matching genre is found, notify the user
                await update.message.reply_text(telebot.translatedData("Error! Maybe your gender is not into the list. ( ˶°ㅁ°) !!\nPlease use the command /help to show the genders are available. (˶ᵔ ᵕ ᵔ˶)"))
    else:
        # If the user did not provide a genre name, prompt them to type a genre name
        if telebot.language == str:
            response = "Type your anime (ෆ˙ᵕ˙ෆ)♡"
            await update.message.reply_text(response)
        else:
            response = telebot.translatedData("Type the gender please (ෆ˙ᵕ˙ෆ)♡")
            await update.message.reply_text(response)
"""
Show Help Function

This function provides help information to the user, displaying the available commands and their descriptions.
"""
async def help(update: Update, context:CallbackContext)->None:
    """
    Provides help information to the user.

    Parameters:
    update (Update): The update object that contains all the information about the incoming update.
    context (CallbackContext): The context object that contains the bot's data and helper functions.
    """
    # Check if the language setting in the telebot is not a string (indicating a specific language setting)
    if telebot.language!=str:
        # Create a help_info string with the translated commands and their descriptions
        help_info = '\n'.join(f'/{x}: {telebot.translatedData(y)}'for x,y in telebot.commands_dictionary.items())
        await update.message.reply_text(help_info)
    else:
        # Create a help_info string with the commands and their descriptions in English
        help_info = '\n'.join(f'/{x}: {y}'for x,y in telebot.commands_dictionary.items())
        await update.message.reply_text(help_info)
def main(TELEGRAM_TOKEN):
    """
    Main function to initialize and run the Telegram bot.

    Parameters:
    TELEGRAM_TOKEN (str): The token for the Telegram bot.
    """
    # Create an application instance with the provided Telegram token
    
    """
    application = Application.builder() 
        .token(str(TELEGRAM_TOKEN))   # Set the bot token
        .post_init(changeCommands)   # Set the post initialization hook to change commands
        .read_timeout(7)   # Set the read timeout to 7 seconds
        .get_updates_connect_timeout(42)   # Set the connect timeout for getting updates to 42 seconds
        .build()  # Build the application instance
    """
    application = Application.builder().token(str(TELEGRAM_TOKEN)).post_init(changeCommands).read_timeout(7).get_updates_connect_timeout(42).build()
    # Add command handlers to the application
    application.add_handler(CommandHandler("start",start))# Handle the /start command
    application.add_handler(CommandHandler("language", language))# Handle the /language command
    application.add_handler(CallbackQueryHandler(button))# Handle callback queries
    application.add_handler(CommandHandler("request",requestAnime))# Handle the /request command
    application.add_handler(CommandHandler("random",requestRandom))# Handle the /random command
    application.add_handler(CommandHandler("hoshii",requestgender))# Handle the /hoshii command
    application.add_handler(CommandHandler("help", help))# Handle the /help command
    #Run the bot until the user presses Ctrl-C
    application.run_polling()