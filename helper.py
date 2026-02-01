import numpy as np
import pandas as pd
from typing import Tuple


def fetch_medal_tally(df: pd.DataFrame, year: str, country: str) -> pd.DataFrame:
    """Return medal tally filtered by year and/or country.

    Args:
        df: Preprocessed DataFrame (must include 'Gold','Silver','Bronze','region','Year').
        year: Year as string or 'Overall'.
        country: Country name or 'Overall'.

    Returns:
        DataFrame with aggregated medal counts and a 'total' column.
    """
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if year == 'Overall' and country != 'Overall':
        x = (
            temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']]
            .sum()
            .reset_index()
            .sort_values('Year', ascending=True)
        )
    else:
        x = (
            temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']]
            .sum()
            .reset_index()
            .sort_values('Gold', ascending=False)
        )

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x


def medal_tally(df: pd.DataFrame) -> pd.DataFrame:
    """Return overall medal tally grouped by region."""
    medals_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medals_tally = (
        medals_tally.groupby('region')[['Gold', 'Silver', 'Bronze']]
        .sum()
        .reset_index()
        .sort_values('Gold', ascending=False)
    )
    medals_tally['total'] = medals_tally['Gold'] + medals_tally['Silver'] + medals_tally['Bronze']
    return medals_tally


def country_year_list(df: pd.DataFrame) -> Tuple[list, list]:
    years = sorted(df['Year'].dropna().unique().tolist())
    years.insert(0, 'Overall')

    country = sorted(pd.Series(df['region'].dropna().unique()).tolist())
    country.insert(0, 'Overall')

    return years, country


def data_over_time(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Return number of unique `col` values per Year.

    Returns a DataFrame with columns ['Edition','<col>'] where Edition==Year.
    """
    # Count unique values of `col` per year (e.g., unique regions per Year)
    nations_over_time = (
        df.drop_duplicates(['Year', col]).groupby('Year').agg({col: 'nunique'}).reset_index()
    )
    nations_over_time.rename(columns={'Year': 'Edition', col: col}, inplace=True)
    return nations_over_time


# noinspection SpellCheckingInspection
def mostsuccessful(df: pd.DataFrame, Sport: str) -> pd.DataFrame:
    temp_df = df.dropna(subset=['Medal'])

    if Sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == Sport]

    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medal Count']

    x = (
        medal_counts.merge(df, on='Name', how='left')
        [['Name', 'Medal Count', 'Sport', 'region']]
        .drop_duplicates(['Name'])
        .rename(columns={'Medal Count': 'Medals'})
    )
    return x


# noinspection SpellCheckingInspection
def yearwise_medal_tally(df: pd.DataFrame, country: str) -> pd.DataFrame:
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]
    new_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return new_df


def country_event_heatmap(df: pd.DataFrame, country: str) -> pd.DataFrame:
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


# noinspection SpellCheckingInspection
def mostsuccessful_countrywise(df: pd.DataFrame, country: str) -> pd.DataFrame:
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medal Count']

    x = (
        medal_counts.merge(df, on='Name', how='left')
        [['Name', 'Medal Count', 'Sport']]
        .drop_duplicates(['Name'])
        .rename(columns={'Medal Count': 'Medals'})
    )

    return x


def weight_vs_height(df: pd.DataFrame, sport: str) -> pd.DataFrame:
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        return athlete_df[athlete_df['Sport'] == sport]
    else:
        return athlete_df


def men_vs_women(df: pd.DataFrame) -> pd.DataFrame:
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)

    return final