from apiget.animeapi import AnimeApp
#Instantiation class AnimeApp
rand_anime = AnimeApp()
#Change language to spanish
rand_anime.changeLanguage('es')
#Change option to random
rand_anime.getOption('randanime')
#print the data
print(rand_anime.getAnimeData())
#Instantiation class AnimeApp
source_anime = AnimeApp()
#Change language to japanese
source_anime.changeLanguage('ja')
#Give the name of anime. Input is available on english japanese and romaji without special characters.
source_anime.changeAnimeSource('らんま1/2')
#Change option to username input
source_anime.getOption('useranime')
#print the data 
print(source_anime.getAnimeData())
#Instantiation class AnimeApp
recomendation_gender = AnimeApp()
#Change language to spanish
recomendation_gender.changeLanguage('es')
#Search and print recomendation
print(recomendation_gender.getSuggestbyGenre('Ecchi'))