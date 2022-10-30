import datetime
import os
from dataclasses import dataclass

import pandas as pd

import warnings

warnings.filterwarnings('ignore')


class ProjectData:
    """
    Class for loading data in pandas.DataFrame.
    Classmethods return filtered by user_id data or validation is user exists
    """
    ### Написать код так, чтобы вместо файлов можно было легко переключиться на базу данных (использовать в логике скрипта агрегации данных не чтение из файла напрямую, а какую-то абстракцию, паттерн, имплементацию которой можно будет легко изменить, не меняя логику алгоритма агрегации данных)
    __users: pd.DataFrame = pd.read_csv(os.environ.get('USERS'))
    __hotspots: pd.DataFrame = pd.read_csv(os.environ.get('HOTSPOTS'))
    __conns: pd.DataFrame = pd.read_csv(os.environ.get('CONNS'))

    @classmethod
    def user_hotspots(cls, user_id: int) -> pd.DataFrame:
        return cls.__hotspots[cls.__hotspots['owner_id'] == user_id]

    @classmethod
    def user_conns(cls, user_id: int) -> pd.DataFrame:
        user_hotspots = cls.user_hotspots(user_id)
        user_hotspot_ids = tuple(user_hotspots['id'].values)
        return cls.__conns[cls.__conns['hotspot_id'].isin(user_hotspot_ids)]

    @classmethod
    def is_user(cls, user_id: int) -> bool:
        if user_id in cls.__users['id'].values:
            return True
        return False


@dataclass
class Day:
    today: datetime.date = pd.to_datetime(datetime.datetime.now()).date()
    year_ago: datetime.date = (today - pd.DateOffset(years=1)).date()
    month_ago: datetime.date = (today - pd.DateOffset(months=1)).date()
    week_ago: datetime.date = (today - pd.DateOffset(weeks=1)).date()


class UserProjectStats:
    """
    Class for getting stats by user_id
    Initialized with filtered by user_id dataframes from ProjectData
    """
    def __init__(self, user_id: int):
        self.__day = Day()
        self.__user_id = user_id
        self.__hotspots: pd.DataFrame = ProjectData.user_hotspots(user_id)
        self.__conns = pd.DataFrame = ProjectData.user_conns(user_id)

    @property
    def hotspots_quantity(self):
        """
        Сколько wifi точек (мы wifi записи еще называем hotpots) создал пользователь (не удаленных. Всего созданных можно получить в hotspots_dates['all_time'])
        :return: JSON
        """
        return {'quantity': self.__hotspots[self.__hotspots['deleted_at'].isnull()]['id'].nunique()}

    @property
    def hotspots_with_places_quantity(self):
        """
        Сколько hotpots у пользователя с привязкой к месту (not deleted hotspots)
        :return: JSON
        """
        df = self.__hotspots
        df = df[(~df['foursquare_id'].isnull()) | (~df['google_place_id'].isnull())]
        df = df[df['deleted_at'].isnull()]
        return {
            'quantity': len(df)
        }

    @property
    def hotspots_dates(self):
        """
        Сколько hotspots пользователь создал за все время, за последний месяц, неделю
        :return: JSON
        """
        df = self.__hotspots
        df['created_at'] = pd.to_datetime(df['created_at'])
        result = {
            'today_date': str(Day.today),
            'all_time': {'quantity': self.__hotspots['id'].nunique()},
        }
        for period in ['month_ago', 'week_ago']:
            result[period] = {'quantity': len(df[df['created_at'].apply(lambda x: x.date()) > getattr(self.__day, period)])}
        return result

    @property
    def hotspots_scored(self):
        """
        Сколько у пользователя хороших, средних и плохих hotspots (not deleted)
        :return: JSON
        """
        df = self.__hotspots[self.__hotspots['deleted_at'].isnull()]
        result = {
            'bad (Score < 0.3)': {'quantity': len(df[df['score_v4'] < 0.3])},
            'normal (0.3 <= Score < 0.6)': {'quantity': len(df[(df['score_v4'] >= 0.3) & (df['score_v4'] < 0.6)])},
            'good (Score >= 0.6)': {'quantity': len(df[df['score_v4'] >= 0.6])}
        }
        return result

    @property
    def hotspots_conns(self):
        """
        Cколько у пользователя hotspots к которым было больше 1, 5 и 10 уникальных подключений за все время, за последний год, за последний месяц, за последнюю неделю (not deleted hotspots).
        Каждый последующий (1, 5, 10) включает в себя предыдущий (не диапазонами, а больше 1, больше 5, больше 10)
        :return: JSON
        """
        not_deleted_hotspot_ids = self.__hotspots[self.__hotspots['deleted_at'].isnull()]['id'].values
        actual_conns = self.__conns[self.__conns['hotspot_id'].isin(not_deleted_hotspot_ids)]
        actual_conns['connected_at'] = pd.to_datetime(actual_conns['connected_at'])

        result = {'today_date': str(Day.today)}
        nums = [1, 5, 10]

        for period in ['year_ago', 'month_ago', 'week_ago']:
            if len(actual_conns):
                period_conns = actual_conns[actual_conns['connected_at'].apply(lambda x: x.date() > getattr(self.__day, period))]
                installations_quantities = period_conns.groupby(by='hotspot_id')['installation_id'].nunique().reset_index()
                period_result = {
                    f'>{num}': {
                        'quantity': len(installations_quantities[installations_quantities['installation_id'] > num])}
                    for num in nums
                }
            else:
                period_result = {
                    f'>{num}': {'quantity': 0}
                    for num in nums
                }
            result[period] = period_result
        return result
