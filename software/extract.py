import urllib.request
import re
import json
import urllib
import pprint

def extract_videos(search_keyword):
    search_keyword = search_keyword.strip().replace(' ','+')
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v=" + video_ids[0],video_ids[0]


def extract_img(VideoID):
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % VideoID}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    response = urllib.request.urlopen(url)
    response_text = response.read()
    data = json.loads(response_text.decode())
    #pprint.pprint(data)
    return data['thumbnail_url']

