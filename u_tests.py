import datetime
import sys

import pandas as pd

from dotenv import load_dotenv
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

import unittest

import warnings

warnings.filterwarnings('ignore')

from app.api.user_project_stats import UserProjectStats


class UserProjectStatsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.user_stats = UserProjectStats
        self.today = pd.to_datetime(datetime.datetime.now()).date()


class HotspotsQuantityTest(UserProjectStatsTests):

    def test1(self):
        user_id = 1118
        res = self.user_stats(user_id).hotspots_quantity
        self.assertEqual(res, {'quantity': 39})

    def test2(self):
        user_id = 15505
        res = self.user_stats(user_id).hotspots_quantity
        self.assertEqual(res, {'quantity': 973})


class HotspotsWithPlacesQuantity(UserProjectStatsTests):

    def test1(self):
        user_id = 1118
        res = self.user_stats(user_id).hotspots_with_places_quantity
        self.assertEqual(res, {'quantity': 34})

    def test2(self):
        user_id = 15505
        res = self.user_stats(user_id).hotspots_with_places_quantity
        self.assertEqual(res, {'quantity': 826})


class HotspotsDates(UserProjectStatsTests):

    def test1(self):
        user_id = 1118
        res = self.user_stats(user_id).hotspots_dates
        self.assertEqual(res,
                         {
                             "today_date": str(self.today),
                             "all_time": {"quantity": 42},
                             "month_ago": {"quantity": 0},
                             "week_ago": {"quantity": 0}
                         })

    def test2(self):
        user_id = 15505
        res = self.user_stats(user_id).hotspots_dates
        self.assertEqual(res,
                         {
                             'all_time': {'quantity': 1392},
                             'month_ago': {'quantity': 3},
                             'today_date': str(self.today),
                             'week_ago': {'quantity': 0}
                         })


class HotspotsScored(UserProjectStatsTests):
    def test1(self):
        user_id = 1118
        res = self.user_stats(user_id).hotspots_scored
        self.assertEqual(res,
                         {'bad (Score < 0.3)': {'quantity': 6},
                          'good (Score >= 0.6)': {'quantity': 32},
                          'normal (0.3 <= Score < 0.6)': {'quantity': 1}})

    def test2(self):
        user_id = 15505
        res = self.user_stats(user_id).hotspots_scored
        self.assertEqual(res,
                         {'bad (Score < 0.3)': {'quantity': 470},
                          'good (Score >= 0.6)': {'quantity': 468},
                          'normal (0.3 <= Score < 0.6)': {'quantity': 35}})


class HotspotsConns(UserProjectStatsTests):
    def test1(self):
        user_id = 1118
        res = self.user_stats(user_id).hotspots_conns
        self.assertEqual(res,
                         {"today_date": str(self.today),
                          "year_ago": {
                              ">1": {"quantity": 12},
                              ">5": {"quantity": 3},
                              ">10": {"quantity": 2}
                          },
                          "month_ago": {
                              ">1": {"quantity": 2},
                              ">5": {"quantity": 0},
                              ">10": {"quantity": 0}
                          },
                          "week_ago": {
                              ">1": {"quantity": 0},
                              ">5": {"quantity": 0},
                              ">10": {"quantity": 0}
                          }})

    def test2(self):
        user_id = 15505
        res = self.user_stats(user_id).hotspots_conns
        self.assertEqual(res,
                         {'month_ago': {'>1': {'quantity': 23},
                                        '>5': {'quantity': 0},
                                        '>10': {'quantity': 0}},
                          'today_date': str(self.today),
                          'week_ago': {'>1': {'quantity': 0},
                                       '>5': {'quantity': 0},
                                       '>10': {'quantity': 0}},
                          'year_ago': {'>1': {'quantity': 235},
                                       '>5': {'quantity': 79},
                                       '>10': {'quantity': 41}}})


if __name__ == '__main__':
    unittest.main(verbosity=2).runTests()
