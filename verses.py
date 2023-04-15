#!/usr/bin/env python3


####################################
# verses.py is a program designed  #
# to query verses of the quran in  #
# various languages                #
#                                  #
# Designed by Anas Lecaillon       #
####################################

# import system libraries to open and fetch files
import re
import sys
import os.path
import wget

#languages
languages = {
        "en" : "https://tanzil.net/trans/en.sahih",
        "tr" : "https://tanzil.net/trans/en.transliteration",
        "fr" : "https://tanzil.net/trans/fr.hamidullah",
        "ar" : "https://tanzil.net/trans/ar.muyassar",
        "de" : "https://tanzil.net/trans/de.aburida",
        "it" : "https://tanzil.net/trans/it.piccardo",
        "es" : "https://tanzil.net/trans/es.bornez"
}

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# default values
args = sys.argv
language = "ar"
query = ""
searching = False
colored = False
transliteration = False
verses_selected = False
help_requested = False

#cache folders
homedir = os.environ["HOME"]
qurandir = homedir + "/.cache/quran"


#### MAIN ####

def main(args):
    
    global language
    global transliteration
    global query
    global searching
    global colored
    global verses_selected

    # make sure the path exists
    if not os.path.exists(qurandir):
        os.makedirs(qurandir)

    for i in range(len(args)):
        arg = args[i]
    

        # help menu
        if arg == "-h":
            help_menu()
            exit()

        # search
        elif arg == "-s":
            searching = True
            colored = False
            try:
                query = args[i+1]
            except:
                print("Missing query")
                exit(1)
        # search with color
        elif arg == "-sc":
            searching = True
            colored = True
            try:
                query = args[i+1]
            except:
                print("Missing query")
                exit(1)

        # language selection
        elif arg == "-l":
            try:
                language = args[i+1]
            except:
                print("Invalid arguments")
                exit(1)

        # transliteration
        elif arg == "-t":
            transliteration = True
            try:
                language = "tr"
            except:
                print("Invalid arguments")
                exit(1)

        elif arg == "-v":
            verses_selected = True
    
    run(searching, colored, query, verses_selected, transliteration, language)


#### MAIN RUN BLOCK ####

def run(searching, colored, query, verses_selected, transliteration, language):
    handle_language(language, transliteration)
    quran_open(language)
    if verses_selected:
        requested_verses = handle_verses()
        if searching:
            query_results = search(query, colored, requested_verses)
            for i in query_results:
                print(i)
        else:
            for i in requested_verses:
                print(i)
    else:
        requested_verses = quran
        if searching:
            query_results = search(query, colored, requested_verses)
            for i in query_results:
                print(i)
        else:
            print("Error: no verses specified")
            exit(1)
    quran.close()



#### VERSE HANDLING ####


# method to handle verses in cli arguments and print out the requested verses to screen
def handle_verses():

    # requested verses is the returned list of verse strings
    requested_verses = []

    #generate array of verses from cli arguments
    verses = []
    for i in range(len(args)):
        arg = args[i]
        # print("finding verse at arg num: ", arg)
        if arg == "-v":
            for j in range(i+1, len(args)):
                verses.append(args[j])

    if verses == ['all']:
        verses = quran.readlines()
        quran.seek(0)
        requested_verses = []
        for verse in verses:
            if verse[0] != "#":
                formatted_verse = re.sub(r"([0-9]*)\|([0-9]*)\|", r"(\1:\2)", verse).strip()
                requested_verses.append(formatted_verse)
        return requested_verses
                # print("appended verse: ", args[j])
        
    # get and open the required quran file
    # print("opened quran file")

    # parse verses into tuples
    parsed_verses = []
    for verse in verses:
        parsed_verse = parse(verse)
        if type(parsed_verse) == type((0,1)):
            parsed_verses.append(parse(verse))
        elif type(parsed_verse) == type([0,1]):
            parsed_verses.extend(parsed_verse)
        else:
            print("Type error: ", type(parsed_verse))
        # print("verses parsed")
            

    # search quran for selected verses
    verses = quran.readlines()
    quran.seek(0)
    for selected_verse in parsed_verses:
        for verse in verses:
            if re.match("^" + selected_verse[0] + "\|" + selected_verse[1] + "\|" + ".*", verse):
                formatted_verse = re.sub("[0-9]*\|[0-9]*\|", "(" + selected_verse[0] + ":" + selected_verse[1] + ") ", verse).strip()
                requested_verses.append(formatted_verse)
    return requested_verses


# method to parse text verse index into a tuple of (chapter, verse) or a list of such tuples
def parse(versetext):
    index = versetext.split(":")
    verses = []
    #print("parsed verse: ", index)
    if "," in index[1]:
        verseparts = []
        versepart_list = index[1].split(",")
        for versepart in versepart_list:
            verseparts.append(str(versepart))

        for part in verseparts:
            if "-" in part:
                verse_range = part.split("-")
                for verse in range(int(verse_range[0]), int(verse_range[1])+1):
                    verses.append((index[0], str(verse)))
            else:
                verses.append((index[0], str(part)))
            
        return verses
 
    # if the verse part contains a range (i.e 4:3-56)
    elif "-" in index[1]:
        verses = []
        verse_range = index[1].split("-")
        for verse in range(int(verse_range[0]), int(verse_range[1])+1):
            verses.append((index[0], str(verse)))
        return verses
    # if the verse part contains a list (i.e 4:3,7,82)
    elif "," in index[1]:
        verses = []
        verse_list = index[1].split(",")
        for verse in verse_list:
            verses.append((index[0], str(verse)))
        return verses
        
        
    else:
        return (index[0], index[1])


#### HELP ####

def help_menu():
    print("Welcome to verses")
    print("-h                  help menu")
    print("-l [language code]  language selection (ex: 'verses -l en')")
    print("-t                  english transliteration")
    print("-v   [verses]       verse list (ex: 'verses -v 1:23 6:24 5:4-7') or 'all' to have entire corpus")
    print("-s [query]          search for query (can be regex)")
    print("-sc [query]         search for query (can be regex)" + color.GREEN + " (colored)" + color.END)
    print("\n")
    print("Note: the '-v' option must be last")
    print("Current languages: en, fr, ar, it, es, de")
    print("About transliteration:")
    print("\n")
    print("Bold letters are not pronounced, underlined consonants are hard consonants, \n and underlined vowels are long vowels")
    print("like in: a" + color.BOLD + "l" + color.END + "rra" + color.UNDERLINE + "h" + color.END + "m" + color.UNDERLINE + "a" + color.END + "n")

    exit()

#### SEARCH ####

def search(query, colored, verses):
    query_matches = 0
    query_results = []

    for verse in verses:
        verse_text = re.sub("^([0-9]+\:[0-9]+)\s", "", verse)
        if re.match(query, verse_text):
            query_matches += 1
            if colored:
                verse = re.sub(query, color.GREEN + query + color.END, verse)
            query_results.append(str(query_matches) + ": " + verse)
        
    if len(query_results) == 0:
        for verse in verses:    
            verse_text = re.sub("^([0-9]+\:[0-9]+)\s", "", verse)
            if re.match(".*" + query + ".*", verse_text):
                query_matches += 1
                if colored:
                    verse = re.sub(query, color.GREEN + query + color.END, verse)
                query_results.append(str(query_matches) + ": " + verse)
    return query_results


#### LANGUAGE ####


# language handler
def handle_language(language, transliteration):
    #check if language is downloaded
    if not check_language_available(language):
        print("downloading new language", language)
        try:
            download_language(language)
            if transliteration:
                path = qurandir + "/" + language
                translit_text = open(path, "r" )
                lines = []
                for line in translit_text:
                    lines.append(line)

                newlines = []
                for line in lines:
                    # UNDERLINE
                    newline = re.sub("<u>", color.UNDERLINE, line)
                    newline = re.sub("</U>", color.END, newline)
                    newline = re.sub("</u>", color.END, newline)

                    # BOLD
                    newline = re.sub("<b>", color.BOLD, newline)
                    newline = re.sub("</B>", color.END, newline)
                    newline = re.sub("</b>", color.END, newline)
                    newlines.append(newline)

                translit_text.close()
                translit_text = open(path, "w")
                for line in newlines:
                    translit_text.write(line)



        except Exception as e:
            print("Could not download language: ", language)
            print(e)
            exit(1)

# checks if language is available
def check_language_available(language):
    path = qurandir + "/" + language
    return os.path.isfile(path)

# downloads language
def download_language(language):
    path = qurandir + "/" + language
    wget.download(languages[language], path)
    print("\n")


#### FILE OPS ####

def quran_open(language):
    global path
    path = qurandir + "/" + language
    global quran
    quran = open(path, mode="r", encoding="utf-8")



######## Main execution

if len(args) >= 2:
    main(args)
else:
    help_menu()
    exit(1)



