import unittest
import time
import calendar

DAY_IN_SECONDS = 60 * 60 * 24

class TestRssChecker(unittest.TestCase):
    def test_find_inactive(self):
        from rss_checker import find_inactive
        feed_urls_by_companies = {}
        with self.subTest(feed_urls_by_companies=feed_urls_by_companies):
            self.assertEqual([], find_inactive(feed_urls_by_companies, 0))
            self.assertEqual([], find_inactive(feed_urls_by_companies, 1))
            self.assertEqual([], find_inactive(feed_urls_by_companies, 99))

        feed_urls_by_companies = {'apology_line': 'test_rss/apology_line.xml'}
        with self.subTest(feed_urls_by_companies=feed_urls_by_companies):
            # time stamp of the latest item
            apology_line_latest = calendar.timegm((2021, 2, 16, 8, 5, 0, 1, 47, 0))

            # time elapsed since the latest item
            time_elapsed_apology_line = time.time() - apology_line_latest

            days_elapsed_apology_line = time_elapsed_apology_line // DAY_IN_SECONDS
            self.assertEqual([], find_inactive(feed_urls_by_companies, days_elapsed_apology_line + 1))
            self.assertEqual(['apology_line'], find_inactive(feed_urls_by_companies, days_elapsed_apology_line - 1))

        feed_urls_by_companies = {'apology_line': 'test_rss/apology_line.xml',
                                  'lincoln_project': 'test_rss/lincoln_project.xml'}
        with self.subTest(feed_urls_by_companies=feed_urls_by_companies):
            # time stamps of the latest items
            apology_line_latest = calendar.timegm((2021, 2, 16, 8, 5, 0, 1, 47, 0))
            lincoln_project_latest = calendar.timegm((2021, 2, 17, 20, 49, 46, 2, 48, 0))

            # time elapsed since the latest items
            time_elapsed_apology_line= time.time() - apology_line_latest
            time_elapsed_lincoln_project = time.time() - lincoln_project_latest

            days_elapsed_apology_line= time_elapsed_apology_line // DAY_IN_SECONDS
            self.assertEqual([], find_inactive(feed_urls_by_companies, days_elapsed_apology_line + 1))

            days_elapsed_lincoln_project = time_elapsed_lincoln_project // DAY_IN_SECONDS
            self.assertEqual(['apology_line', 'lincoln_project'], find_inactive(feed_urls_by_companies, days_elapsed_lincoln_project - 1))

        feed_urls_by_companies = {'apology_line': 'test_rss/apology_line.xml',
                                  'lincoln_project': 'test_rss/lincoln_project.xml',
                                  'politico-news': 'test_rss/politico-news.xml'}
        with self.subTest(feed_urls_by_companies=feed_urls_by_companies):
            self.assertEqual(set(['apology_line', 'lincoln_project', 'politico-news']),
                             set(find_inactive(feed_urls_by_companies, 0)))             


if __name__ == '__main__':
    unittest.main()
