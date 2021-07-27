# Spotify_to_Youtube
Here is a project I have been working on to scrape info from Spotify playlists and produce a Youtube playlist.

Here are the issues that I ran into, and the reason I decided to discontinue this project:
 - So for the general idea of scraping content from Spotify, querying Youtube's search engine, and then capturing the ID from the returned page, that was done, and worked very well. However, the issue that I ran into was that YT rendered it's data/page using json. that in in ot itself was no problem at all, I could just capture thejson using beautiful soup and parse it using python's json library however, there seemed to be errors in the json when I captured it. I am not sure if it was the way I captured the page using beautiful soup, or if YT legitimately had issues inside of their json. Either for dissuading individuals from scraping their site, or just errors... Regardless, the python json library cannot parse json if there is a single error in it... 
 - That being said, there are several ways to fix this:
        1) use regular expressions to filter and grab only the parts of the json that are needed
        2) make a script that filters through json and "debugs" by iterating through each character
        3) find a way to parse the json on the YT page so that it does not throw errors
