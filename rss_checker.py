import feedparser
import time
import calendar

DAY_IN_SECONDS = 60 * 60 * 24

def find_inactive(rss_feed_urls, days_of_inactive):
    """
    Return a list of companies that have no activity for a given number of days.
    Input:  
        rss_feed_urls (string): a dictionary with key of company name and value of RSS feed url
        days_of_inactive (int): a number of days
    """
    cutoff_time = time.time() - (days_of_inactive * DAY_IN_SECONDS)
    latest_publishing_times = {}

    # obtain the publishing time of the latest published item of each feed
    for company in rss_feed_urls:
        # check if value is array (multiple feeds)
        urls = rss_feed_urls[company]
        if isinstance(urls, list) is False:
            urls =[urls]

        for url in urls:
            rss_feed = feedparser.parse(url)
            latest_publishing_time = None

            for entry in rss_feed.entries:
                publishing_time = entry.get('published_parsed', None)
                
                if publishing_time is not None:
                    publishing_time = calendar.timegm(publishing_time)  # specify publishing time as a timestamp

                    if latest_publishing_time is None:
                        latest_publishing_time = publishing_time
                    elif publishing_time > latest_publishing_time:
                        latest_publishing_time = publishing_time

            # update latest_publishing_time if it is alreay in the Dictionaries
            publishing_time = latest_publishing_times.get(company)
            if publishing_time is None:
                latest_publishing_times[company] = latest_publishing_time
            elif latest_publishing_time >  publishing_time:
                latest_publishing_times[company] = latest_publishing_time

    # obtain the list of inactive companies within days_of_inactive days
    inactive_companies = []
    for company in latest_publishing_times:
        latest_publishing_time = latest_publishing_times[company]

        if latest_publishing_time is None or latest_publishing_time < cutoff_time:
            inactive_companies.append(company)

    return inactive_companies
