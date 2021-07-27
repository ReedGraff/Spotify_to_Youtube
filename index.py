import urllib.request
import pandas as pd
import regex as re
import html5lib
import requests
import demjson
import os

from urllib.parse import urlparse, urljoin
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from time import sleep


class Converter:
    def __init__(self, URL, Yes_No):
        ua = UserAgent()
        #self.header = {"User-Agent":str(ua.chrome)}
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
        
        self.URL = URL
        
        while Yes_No != "YES" and Yes_No != "NO":
            if "Y" in Yes_No or "y" in Yes_No and "N" not in Yes_No and "n" not in Yes_No:
                Yes_No = "YES"
            elif "N" in Yes_No or "n" in Yes_No and "Y" not in Yes_No and "y" not in Yes_No:
                Yes_No = "NO"
            else:
                Yes_No = input("Please enter yes or no: ")

        self.Yes_No = Yes_No
    
    def MainInnerHTML(self):
        req = requests.get(self.URL)
        soup = BeautifulSoup(req.content, 'html.parser')

        """
        soup = soup.prettify()
        with open("out.txt","w") as out:
            for i in range(0, len(soup)):
                try:
                    out.write(soup[i])
                except:
                    1+1
        """
        
        for tag in soup.findAll("ol"):
            if str(tag["class"][0]) == "tracklist":
                print("Found")
                return tag.encode_contents()
            else:
                print("Not Found")
      
    def Convert_Layman(self):
        if self.Yes_No == "YES":
            soup = BeautifulSoup(self.MainInnerHTML(), 'html.parser')
            Songs = []
            Artists = []
            id_list = []
            playlist_string = "http://www.youtube.com/watch_videos?video_ids="

            # For Chrome Setting turned off:
            # Song Names
            for tag in soup.findAll("div"):
                for sub_tag in tag.findAll("div"):
                    if "dir" in sub_tag.attrs:
                        if sub_tag.attrs["class"][0] == "auto":
                            if "as" in sub_tag.attrs:
                                if sub_tag.attrs["as"][0] == "div":
                                    print(sub_tag.encode_contents())
                                    Songs.append(sub_tag.encode_contents())

            # Song Artists
            for tag in soup.findAll("span"):
                for sub_tag in tag.findAll("a"):
                    if "dir" in sub_tag.attrs:
                        if sub_tag.attrs["dir"][0] == "auto":
                            if "href" in sub_tag.attrs:
                                if "artist" in sub_tag.attrs["href"][0]:
                                    print(sub_tag.encode_contents())
                                    Artists.append(sub_tag.encode_contents())

            # Songs and Artist should be the same length...

            # Finding youtube IDs
            for i in range(0,len(Songs)): # Do I subtract 1?
                search_query = (str(Songs[i]) + " song by " + str(Artists[i]))
                search_query.replace(" ", "+")

                req = requests.get("https://www.youtube.com/results?search_query=" + search_query, headers = self.header)
                soup = BeautifulSoup(req.content, 'html.parser')

                tag = soup.find(id="thumbnail")
                id = tag.attrs["href"][0]
                pattern = "(?:watch\?v=|watch\?.+&v=|embed\/|v\/|.+\?v=)?([^&=\n%\?]{11})"
                id = re.findall(pattern, id)
                id_list.append(id)

            for j in id_list:
                playlist_string = playlist_string + "," + j

            print(playlist_string) 
        else:
            # Only 30
            soup = BeautifulSoup(self.MainInnerHTML(), 'html.parser')
            Songs = []
            Artists = []
            id_list = []
            playlist_string = "http://www.youtube.com/watch_videos?video_ids="

            # For Chrome Setting turned off:
            # Song Names
            for tag in soup.findAll("span"):
                if "class" in tag.attrs:
                    if tag.attrs["class"][0] == "track-name":
                        print(tag.encode_contents())
                        Songs.append(tag.encode_contents())

            # Song Artists
            for tag in soup.findAll("a"):
                tag = BeautifulSoup(tag.encode_contents(), 'html.parser')
                for sub_tag in tag.findAll("span"):
                    if len(Artists) != len(Songs):
                        print(sub_tag.encode_contents())
                        Artists.append(sub_tag.encode_contents())

            # Songs and Artist should be the same length...

            # Finding youtube IDs
            print(str(len(Songs)))
            print(str(len(Artists)))

            # YouTube

            for i in range(0,len(Songs)): # Do I subtract 1?
                search_query = ("Official" + str(Songs[i]) + " song by " + str(Artists[i]))
                search_query = search_query.replace(" ", "+")
                search_query = search_query.replace("b'", "+")
                search_query = search_query.replace("'", "")
                search_query = search_query.replace("-", "")

                Found = "False"

                req = requests.get("https://www.youtube.com/results?search_query=" + str(search_query) + "&sp=CAM%253D")
                soup = BeautifulSoup(req.content, 'html.parser')

                print("https://www.youtube.com/results?search_query=" + str(search_query) + "&sp=CAM%253D")

                for tag in soup.findAll("script"):
                    if "nonce" in tag.attrs:
                        if "var ytInitialData" in str(tag.encode_contents()):
                            if Found == "False":
                                pattern = "(?:watch\?v=|watch\?.+&v=|embed\/|v\/|.+\?v=)?([^&=\n%\?]{11})"
                                id = re.findall(pattern, str(tag.encode_contents()))
                                print(str(len(id)))
                                for j in id:
                                    if "var" in j:
                                        id.remove(str(j))
                                for j in id:
                                    if "response" in j:
                                        id.remove(str(j))
                                for j in id:
                                    if '"' in j:
                                        id.remove(str(j))
                                for j in id:
                                    if '{' in j:
                                        id.remove(str(j))
                                for j in id:
                                    if '}' in j:
                                        id.remove(str(j))
                                for j in id:
                                    if 'service' in j:
                                        id.remove(str(j))
                                for j in id:
                                    if 'param' in j:
                                        id.remove(str(j))
                                for j in id:
                                    if ',' in j:
                                        id.remove(str(j))
                                for j in id:
                                    if 'web' in j:
                                        id.remove(str(j))
                                for j in id:
                                    if 'search' in j:
                                        id.remove(str(j))
                                for j in id:
                                    if 'has' in j:
                                        id.remove(str(j))
                                for j in id:
                                    if 'limit' in j:
                                        id.remove(str(j))
                                for j in id:
                                    if 'entitle' in j:
                                        id.remove(str(j))
                                for j in id:
                                    if 'premium' in j:
                                        id.remove(str(j))
                                for j in id:
                                    if 'key' in j:
                                        id.remove(str(j))
                                print(str(len(id)))
                                id_list.append(id[0])
                                Found = "True"
            for j in id_list:

                playlist_string = playlist_string + str(j) + ","

            print(playlist_string)
            print(""*2)
            #print(pd.DataFrame({"Songs":Songs, "Artists":Artists}))
    
    def Convert_Complex(self):
        import json
        if self.Yes_No == "YES":
            1+1
        else: # Old Sspotify.. Only 30 results
            # Only 30
            soup = BeautifulSoup(self.MainInnerHTML(), 'html.parser')
            Songs = []
            Artists = []
            id_list = []
            playlist_string = "http://www.youtube.com/watch_videos?video_ids="

            # For Chrome Setting turned off:
            # Song Names
            for tag in soup.findAll("span"):
                if "class" in tag.attrs:
                    if tag.attrs["class"][0] == "track-name":
                        print(tag.encode_contents())
                        Songs.append(tag.encode_contents())

            # Song Artists
            for tag in soup.findAll("a"):
                tag = BeautifulSoup(tag.encode_contents(), 'html.parser')
                for sub_tag in tag.findAll("span"):
                    if len(Artists) != len(Songs):
                        print(sub_tag.encode_contents())
                        Artists.append(sub_tag.encode_contents())

            # Songs and Artist should be the same length...

            # Finding youtube IDs
            print(str(len(Songs)))
            print(str(len(Artists)))

            # YouTube

            for i in range(0,len(Songs)): # Do I subtract 1?
                search_query = ("Official" + str(Songs[i]) + " song by " + str(Artists[i]))
                search_query = search_query.replace(" ", "+")
                search_query = search_query.replace("b'", "+")
                search_query = search_query.replace("'", "")
                search_query = search_query.replace("-", "")

                Found = "False"

                req = requests.get("https://www.youtube.com/results?search_query=" + str(search_query) + "&sp=CAM%253D")
                soup = BeautifulSoup(req.content, 'html.parser')

                print("https://www.youtube.com/results?search_query=" + str(search_query) + "&sp=CAM%253D")


                """
                tries = 0

                while tries < 3:
                    try:
                        for tag in soup.findAll("script"):
                            if "nonce" in tag.attrs:
                                if "var ytInitialData" in str(tag.encode_contents()):
                                    if Found == "False":                              
                                        json_data = str(tag.encode_contents())
                                        json_data = json_data.replace("b'var ytInitialData = ", "")
                                        json_data = json_data.replace("}}}}}}};'", "}}}}}}}")
                                        json_data = json_data.replace("/", "")

                                        cut = []

                                        for j in range(0, json_data.count('""')):
                                            for i in range(0, (len(json_data) - len(cut))):
                                                try:
                                                    if json_data[i] == '"':
                                                        if json_data[i-1] == '"':
                                                            replacement = r"\*"
                                                            replacement = replacement.replace('*', '')
                                                            json_data = json_data.replace(replacement, "")
                                                            if json_data[i+1] != '}' and json_data[i+1] != ',':
                                                                json_data = list(json_data)
                                                                del(json_data[i])
                                                                json_data = "".join(json_data)
                                                                cut.append(i)
                                                                print("cutting" + str(i) + " with 1")
                                                        if json_data[i-1] == '"':
                                                            if json_data[i-2] != ":":
                                                                json_data = list(json_data)
                                                                del(json_data[i])
                                                                json_data = "".join(json_data)
                                                                cut.append(i)
                                                                print("cutting" + str(i) + " with 2")
                                                        if json_data[i-1] == ":":
                                                            inside = re.search(''-'d', s)
                                                except:
                                                    1+1
                                        
                                        '''

                                        # Replace with "" instead of "'"
                                            Replace all "'" or '"' inside of the two main with an empty string...

                                        for j in range(0, json_data.count('"')):
                                            inside = []
                                            for j in range(0, len(json_data)):
                                                if json_data[j] == '"':
                                                    while state == "True":
                                                        j += 1
                                                        if json_data[j] == '"':
                                                            if json_data[j+1] != "}" and json_data[j+1] != ",":
                                                                state = "False"
                                                        else:
                                                            inside.append(j)
                                        '''
                                                    





                                        # Escape issue..."
                                        '''
                                        letter_list = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","'",'"']
                                        for letter in letter_list:
                                            replacement = r"\*" + letter
                                            replacement = replacement.replace('*', '')
                                            to_replace = r"\\"
                                            print(replacement)
                                            json_data = json_data.replace(replacement, to_replace)
                                        '''

                                        replacement = r"\*"
                                        replacement = replacement.replace('*', '')
                                        json_data = json_data.replace(replacement, "")
                                        
                                        json_file = open("data.json", "w")
                                        json_file.write(json_data)
                                        json_file.close()
                                        
                                        json_data = json.loads(json_data)
                                        '''
                                        "contents": {
                                            "twoColumnSearchResultsRenderer": {
                                                "primaryContents": {
                                                    "sectionListRenderer": {
                                                        "contents": [
                                                            {"itemSectionRenderer": {
                                                                "contents": [
                                                                    {"videoRenderer": {
                                                                        "videoId": "sMmTkKz60W8",
                                                                        "viewCountText": {
                                                                            "simpleText": "247,705,544 views"
                                                                    {"videoRenderer": {
                                                                        "videoId": "sMmTkKz60W8",
                                                                        "viewCountText": {
                                                                            "simpleText": "247,705,544 views"
                                        '''
                                        #print(json_data.keys())
                                        #print(json_data["contents"])
                                        #print(json_data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0])
                                        
                                        '''
                                        for i in range(0, len(json_data"contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"[0]]["itemSectionRenderer"]["contents"])):
                                            json_data[0]["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"[0]]["itemSectionRenderer"]["contents"[i]]
                                        '''
                    except:
                        print("Failed json capture for " + Songs[i] + "... for the " + str(tries) + " time retrying...")
                        tries += 1
                """

                for tag in soup.findAll("script"):
                    if "nonce" in tag.attrs:
                        if "var ytInitialData" in str(tag.encode_contents()):
                            if Found == "False":                              
                                json_data = str(tag.encode_contents())
                                json_data = json_data.replace("b'var ytInitialData = ", "")
                                json_data = json_data.replace("}}}}}}};'", "}}}}}}}")
                                json_data = json_data.replace("/", "")

                                cut = []

                                for j in range(0, json_data.count('""')):
                                    for i in range(0, (len(json_data) - len(cut))):
                                        try:
                                            if json_data[i] == '"':
                                                if json_data[i-1] == '"':
                                                    replacement = r"\*"
                                                    replacement = replacement.replace('*', '')
                                                    json_data = json_data.replace(replacement, "")
                                                    if json_data[i+1] != '}' and json_data[i+1] != ',':
                                                        json_data = list(json_data)
                                                        del(json_data[i])
                                                        json_data = "".join(json_data)
                                                        cut.append(i)
                                                        print("cutting" + str(i) + " with 1")
                                                if json_data[i-1] == '"':
                                                    if json_data[i-2] != ":":
                                                        json_data = list(json_data)
                                                        del(json_data[i])
                                                        json_data = "".join(json_data)
                                                        cut.append(i)
                                                        print("cutting" + str(i) + " with 2")
                                                if json_data[i-1] == ":":
                                                    inside = re.search(''-'d', s)
                                        except:
                                            1+1
                                
                                """

                                # Replace with "" instead of "'"
                                    Replace all "'" or '"' inside of the two main with an empty string...

                                for j in range(0, json_data.count('"')):
                                    inside = []
                                    for j in range(0, len(json_data)):
                                        if json_data[j] == '"':
                                            while state == "True":
                                                j += 1
                                                if json_data[j] == '"':
                                                    if json_data[j+1] != "}" and json_data[j+1] != ",":
                                                        state = "False"
                                                else:
                                                    inside.append(j)
                                """
                                            





                                # Escape issue..."
                                """
                                letter_list = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","'",'"']
                                for letter in letter_list:
                                    replacement = r"\*" + letter
                                    replacement = replacement.replace('*', '')
                                    to_replace = r"\\"
                                    print(replacement)
                                    json_data = json_data.replace(replacement, to_replace)
                                """

                                replacement = r"\*"
                                replacement = replacement.replace('*', '')
                                json_data = json_data.replace(replacement, "")
                                
                                json_file = open("data.json", "w")
                                json_file.write(json_data)
                                json_file.close()
                                
                                json_data = json.loads(json_data)
                                """
                                "contents": {
                                    "twoColumnSearchResultsRenderer": {
                                        "primaryContents": {
                                            "sectionListRenderer": {
                                                "contents": [
                                                    {"itemSectionRenderer": {
                                                        "contents": [
                                                            {"videoRenderer": {
                                                                "videoId": "sMmTkKz60W8",
                                                                "viewCountText": {
                                                                    "simpleText": "247,705,544 views"
                                                            {"videoRenderer": {
                                                                "videoId": "sMmTkKz60W8",
                                                                "viewCountText": {
                                                                    "simpleText": "247,705,544 views"
                                """
                                #print(json_data.keys())
                                #print(json_data["contents"])
                                #print(json_data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0])
                                
                                """
                                for i in range(0, len(json_data"contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"[0]]["itemSectionRenderer"]["contents"])):
                                    json_data[0]["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"[0]]["itemSectionRenderer"]["contents"[i]]
                                """

                                

            for j in id_list:
                playlist_string = playlist_string + str(j) + ","

            print(playlist_string)
            print(""*2)
            print(pd.DataFrame({"Songs":Songs, "Artists":Art}))
    
















Converter = Converter(input("Give me the URL for the Spotify playlist here: "), input("Would you like all of the songs [YES]? Would you like the first 30 songs [NO]?: "))
Converter.Convert_Complex()
