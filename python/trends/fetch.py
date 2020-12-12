from pytrends.request import TrendReq

class trends:
    def __init__(self):
        self.pytrends = TrendReq()

    def get_results(self,keyword):
        kw_list = [keyword]
        self.pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
        df = self.pytrends.related_topics()
        trends = []

        for (i,j) in zip(df['algebra']['top']['topic_title'],df['algebra']['top']['topic_type']):
            if i.lower() not in kw_list and j=="Field of study":
                trends.append(i.lower())

        return trends

