from urllib.request import urlopen
from urllib.parse import urlencode
import re
import json
import string

punctuations = string.punctuation

def extract_videos(search_keyword):
    search_keyword = search_keyword.strip().replace(' ','+')
    html = urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    VideoID = video_ids[0]
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % VideoID}
    url = "https://www.youtube.com/oembed"
    query_string = urlencode(params)
    url = url + "?" + query_string

    response = urlopen(url)
    response_text = response.read()
    data = json.loads(response_text.decode())

    return "https://www.youtube.com/watch?v=" + video_ids[0],data['thumbnail_url'],name_check(data['title'])

def name_check(string):
    char_list = [j for j in string if j.isalnum() or j in punctuations or j==" "]
    return ''.join(char_list)