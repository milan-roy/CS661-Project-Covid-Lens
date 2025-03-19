import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

cases_deaths_df = pd.read_csv(config.CASES_DEATHS_FILE_PATH)

cases_deaths_df['country'] = cases_deaths_df['country'].replace('World excl. China, South Korea, Japan and Singapore',
                                                  'World excl. China South Korea Japan and Singapore')

cases_deaths_df['date'] = pd.to_datetime(cases_deaths_df['date'])
cases_deaths_df = cases_deaths_df[cases_deaths_df['date'] <= pd.to_datetime('2024-01-01')]
cases_deaths_df['new_cases'] = cases_deaths_df['new_cases'].fillna(0)
cases_deaths_df['new_deaths'] = cases_deaths_df['new_deaths'].fillna(0)
cases_deaths_df['new_cases_per_million'] = cases_deaths_df['new_cases_per_million'].fillna(0)
cases_deaths_df['new_deaths_per_million'] = cases_deaths_df['new_deaths_per_million'].fillna(0)

cases_deaths_df['total_cases'] = cases_deaths_df['total_cases'].ffill()
cases_deaths_df['total_deaths'] = cases_deaths_df['total_deaths'].ffill()
cases_deaths_df['total_cases_per_million'] = cases_deaths_df['total_cases_per_million'].ffill()
cases_deaths_df['total_deaths_per_million'] = cases_deaths_df['total_deaths_per_million'].ffill()

countries_df = pd.read_csv(config.COUNTRIES_FILE_PATH)
spread_df = cases_deaths_df[['country','date', 'new_cases','total_cases', 'new_deaths', 'total_deaths',
                             'new_cases_per_million', 'total_cases_per_million',
                             'new_deaths_per_million', 'total_deaths_per_million']]

def get_values(row):
    lat = countries_df[countries_df['country']==row.iloc[0]]['latitude'].values[0]
    long = countries_df[countries_df['country']==row.iloc[0]]['longitude'].values[0]
    isocode = countries_df[countries_df['country']==row.iloc[0]]['isocode'].values[0]

    return pd.Series([lat, long, isocode])

spread_df[['latititude', 'longitude', 'isocode']] = spread_df.apply(get_values, axis=1)
spread_df['date'] = spread_df['date'].astype('str').str.split().str[0]

spread_df.to_csv(config.SPREAD_FILE_PATH, index=False)
    







