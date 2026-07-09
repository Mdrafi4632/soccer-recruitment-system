import pandas as pd

UP  = "/sessions/gallant-optimistic-gates/mnt/uploads"
OUT = "/sessions/gallant-optimistic-gates/mnt/outputs"

df = pd.read_csv(f"{UP}/fbref_transfermarkt_merged.csv")
print("Before:", df.shape)

# drop redundant duplicate metadata columns and join helpers
drop_exact = {"Rk", "norm_name", "name", "birth_year", "G+A-PK"}
cols_keep = [c for c in df.columns if "_stats_" not in c and c not in drop_exact]
df = df[cols_keep]

# logical order: identity -> features -> transfermarkt context -> target
identity = ["Player","Nation","Pos","Squad","Comp","Age","Born"]
tm_ctx   = ["player_id","position","sub_position","current_club_name",
            "country_of_citizenship","contract_expiration_date","foot","height_in_cm"]
target   = ["market_value_in_eur","value_millions_eur","highest_market_value_in_eur"]
features = [c for c in df.columns if c not in identity+tm_ctx+target]
df = df[identity + features + tm_ctx + target]

print("After:", df.shape)
print("\nColumns kept:")
for i,c in enumerate(df.columns,1): print(f"{i:>3} {c}")

df.to_csv(f"{OUT}/fbref_transfermarkt_clean.csv", index=False)
print("\nSaved fbref_transfermarkt_clean.csv")
print("Players with market value:", df['market_value_in_eur'].notna().sum(), "/", len(df))
