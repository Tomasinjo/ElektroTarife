import os
import yaml
from datetime import datetime, timedelta
from workalendar.europe import Slovenia
from typing import Tuple
from collections import namedtuple
import pytz

class ElektroTarife():
    def __init__(self, dt: datetime = None):
        self.target_dt = dt
        if self.target_dt is None:
            self.target_dt = datetime.now()
        self.future_windows, self.current = self.hourly_windows()
    
    def next_cheapest(self):
        CheapestWindow = namedtuple('CheapestWindow', ['window', 'start', 'stop'])
        cheapest_window = max(self.future_windows.keys())
        cheapest_window = max(self.future_windows.keys())
        start = min(self.future_windows[cheapest_window])
        stop = max(self.future_windows[cheapest_window]) + timedelta(hours=1)
        return CheapestWindow(window=cheapest_window, start=start, stop=stop)
        
    def info(self) -> str:
        cheapest = self.next_cheapest()
        pretty_windows = '\n'.join([f'Window {w}: Start: {min(i)}, Stop: {max(i) + timedelta(hours=1)}' for w, i in self.future_windows.items()])
        return  f'Current time window is {self.current_window}\nNext cheapest window ({cheapest.window}) will start at {cheapest.start} and stop at {cheapest.stop}\n\nNext windows: \n{pretty_windows}'
    
    def hourly_windows(self) -> Tuple[dict, int]:
        '''windows_with_all_timestamps includes all timestamps for windows
           this is not ideal, since the same window can repeat in 24 hours, but
           we're only interested in timestamps of the most first window occurance.
           The while loop keeps only first timestamps that are 1 hour apart and removes others.
        '''
        start = self.target_dt
        stop = self.target_dt + timedelta(hours=24)
        hourly_datetimes = ElektroTarife.generate_hourly_datetimes(start, stop)
        
        windows_with_all_timestamps = {}
        for dt in hourly_datetimes:
            current_window = ElektroTarife.get_time_window(dt)
            if current_window in windows_with_all_timestamps.keys():
                windows_with_all_timestamps[current_window].append(dt)
            else:
                windows_with_all_timestamps[current_window] = [dt]

        out = {}
        for window, dt_list in windows_with_all_timestamps.items():
            i = 0
            new_dt_list = []
            while len(dt_list) > i:
                current_dt = dt_list[i]
                if i != 0:
                    if (current_dt - dt_list[i-1]).seconds != 3600:
                        break
                new_dt_list.append(current_dt)
                i += 1
            out[window] = new_dt_list
            
        return out, ElektroTarife.get_time_window(hourly_datetimes[0])

    @staticmethod
    def get_tw_config():
        config = os.path.join(os.path.dirname(__file__), 'config.yaml')
        with open(config, 'r') as f:
            contents = f.read()
        return yaml.safe_load(contents)
    
    @staticmethod
    def get_season(dt: datetime) -> str:
        if dt.month in [11, 12, 1, 2]:
            return 'high'
        return 'low'
    
    @staticmethod
    def get_time_window(target_dt):
        now_hour = target_dt.hour
        current_season = ElektroTarife.get_season(target_dt)
        is_workday = Slovenia().is_working_day(target_dt) # boolean
    
        for tw in ElektroTarife.get_tw_config():
            for cond in tw.get('conditions', []):
                if cond['season'] != current_season or cond['work_day'] != is_workday:
                    continue
                if cond['start_hour'] <= now_hour and cond['end_hour'] > now_hour:
                    return tw.get('tw')
        raise Exception('Time window was not found')
    
    @staticmethod
    def generate_hourly_datetimes(start: datetime, stop: datetime) -> list:
        timezone = pytz.timezone('Europe/Ljubljana')
        
        start = start.replace(minute=0, second=0, microsecond=0)
        start = timezone.localize(start)
        stop = stop.replace(minute=0, second=0, microsecond=0)
        stop = timezone.localize(stop)
        datetime_list = []

        while start < stop:
            datetime_list.append(start)
            start += timedelta(hours=1)
        return datetime_list