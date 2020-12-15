from pytrends.request import TrendReq

class Trends:
    def __init__(self):
        self.pytrends = TrendReq()

    def get_results(self,keyword):
        trends = []
        try:
            suggs = self.pytrends.suggestions(keyword)
            kw_list = [suggs[0]['mid']]

            self.pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
            df = self.pytrends.related_topics()

            for i in df[suggs[0]['mid']]['top']['topic_title'][:3]:
                if i.lower() != keyword.lower():
                    trends.append(i.lower())
        except:pass
        return trends
