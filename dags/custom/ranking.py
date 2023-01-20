import pandas as pd

def rank_odds_by_rating(ratings : pd.DataFrame) -> pd.DataFrame :
    ranking = (
        ratings.groupby("meet")
               .agg(
                   avg_rating=pd.NamedAgg(column="odds",aggfunc="mean"),
               )
               .sort_values(["avg_rating"],ascending=False)
    )
    return ranking