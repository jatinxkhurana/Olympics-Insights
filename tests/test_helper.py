import pandas as pd
from helper import data_over_time, country_year_list, fetch_medal_tally


def make_sample_df():
    data = [
        {'Year': 2000, 'region': 'A', 'Team': 'T1', 'NOC': 'X', 'Games': '2000 Summer', 'City': 'C', 'Sport': 'S1', 'Event': 'E1', 'Medal': 'Gold', 'Gold': 1, 'Silver': 0, 'Bronze': 0},
        {'Year': 2000, 'region': 'B', 'Team': 'T2', 'NOC': 'Y', 'Games': '2000 Summer', 'City': 'C', 'Sport': 'S2', 'Event': 'E2', 'Medal': None, 'Gold': 0, 'Silver': 0, 'Bronze': 0},
        {'Year': 2004, 'region': 'A', 'Team': 'T1', 'NOC': 'X', 'Games': '2004 Summer', 'City': 'D', 'Sport': 'S1', 'Event': 'E1', 'Medal': 'Silver', 'Gold': 0, 'Silver': 1, 'Bronze': 0},
    ]
    return pd.DataFrame(data)


def test_country_year_list():
    df = make_sample_df()
    years, countries = country_year_list(df)
    assert years[0] == 'Overall'
    assert 2000 in years
    assert 'A' in countries and 'B' in countries


def test_data_over_time_counts():
    df = make_sample_df()
    res = data_over_time(df, 'region')
    # Editions correspond to years
    editions = sorted(res['Edition'].tolist())
    assert editions == [2000, 2004]
    # check counts (unique regions per year)
    counts = dict(zip(res['Edition'].tolist(), res['region'].tolist()))
    assert counts[2000] == 2
    assert counts[2004] == 1


def test_fetch_medal_tally_overall_country():
    df = make_sample_df()
    # Overall all
    res = fetch_medal_tally(df, 'Overall', 'Overall')
    assert 'total' in res.columns
    # By country
    res_country = fetch_medal_tally(df, 'Overall', 'A')
    # Should return Year rows
    assert 'Year' in res_country.columns
