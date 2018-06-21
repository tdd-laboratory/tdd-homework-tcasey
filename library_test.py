import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # Fourth unit test; test date with format 2015-07-25
    def test_dates(self):
        self.assert_extract('I was born on 2015-07-25.', library.dates_iso8601, '2015-07-25')

    # Fifth unit test; test date with invalid months/days
    def test_incorrect_date(self):
        self.assert_extract("2015-13-48", library.dates_iso8601)

    # Sixth unit test; test date with format 25 Jan 2017
    def dates_fmt2(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_fmt2, '25 Jan 2017')

    # Bunch-o-tests

    # test iso8601 timeStamp with format 2018-06-22T18:22:19.123
    def test_time_stamp(self):
       self.assert_extract('Current timeStamp is 2018-06-22T18:22:19.123', library.dates_iso8601, '2018-06-22T18:22:19.123')

    # test iso8601 timeStamp with format 2018-06-22T18:22:19.123MDT
    def test_time_stamp2(self):
        self.assert_extract('Current timeStamp is 2018-06-22T18:22:19.123MDT', library.dates_iso8601, '2018-06-22T18:22:19.123MDT')

    # test iso8601 timeStamp with format 2018-06-22T18:22:19.123MST
    def test_time_stamp3(self):
        self.assert_extract('Current timeStamp is 2018-06-22T18:22:19.123MST', library.dates_iso8601, '2018-06-22T18:22:19.123MST')

    # test  iso8601 timeStamp with format 2018-06-22T18:22:19.123Z
    def test_time_stamp4(self):
        self.assert_extract('Current timeStamp is 2018-06-22T18:22:19.123Z', library.dates_iso8601, '2018-06-22T18:22:19.123Z')

    # test iso8601 timeStamp with format 2018-06-22T18:22:19.123-800
    def test_time_stamp5(self):
        self.assert_extract('Current timeStamp is 2018-06-22T18:22:19.123-800', library.dates_iso8601, '2018-06-22T18:22:19.123-800')

    # test iso8601 timeStamp with wrong format
    def test_time_stamp6(self):
        self.assert_extract('Current timeStamp is 2018-06-22T18:22:19.12', library.dates_iso8601, '2018-06-22T18:22:19.12')

    # test date format 2 with format 25 Jan, 2017
    def test_date_fmt2_comma(self):
        self.assert_extract('Current date is 25 Jan, 2017', library.dates_fmt2, '25 Jan, 2017')

    # test date format 2 with format 25 Jan. 2017
    def test_date_fmt2_comma2(self):
        self.assert_extract('Current date is 25 Jan. 2017', library.dates_fmt2)

    # test number & letters with comma separated groupings
    def test_invalid_integers_comma(self):
        self.assert_extract('I have 123a,456b,789c', library.integers, '123a,456b,789c')

    # test number with comma separated groupings
    def test_invalid_integers_comma2(self):
        self.assert_extract('I have 123,456,789', library.integers)

if __name__ == '__main__':
    unittest.main()
