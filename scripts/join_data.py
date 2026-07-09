import pandas as pd, unicodedata, re, os

UP = "/sessions/gallant-optimistic-gates/mnt/uploads"
OUT = "/sessions/gallant-optimistic-gates/mnt/outputs"

def norm(s):
    if pd.isna(s): return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

# ---- FBref features ----
fb = pd.read_csv(f"{UP}/players_data-2025_2026-d235ae2b.csv")
fb = fb.loc[:, ~fb.columns.duplicated()]          # drop duplicated col names
fb["norm_name"] = fb["Player"].map(norm)
fb["birth_year"] = pd.to_numeric(fb["Born"], errors="coerce")
print("FBref players:", len(fb))

# ---- Transfermarkt target ----
tm = pd.read_csv(f"{UP}/players.csv")
tm["norm_name"] = tm["name"].map(norm)
tm["birth_year"] = pd.to_datetime(tm["date_of_birth"], errors="coerce").dt.year
# keep only rows with a market value; prefer most recent / most valuable per (name, year)
tmv = tm.dropna(subset=["market_value_in_eur"]).copy()
tmv = tmv.sort_values(["last_season", "market_value_in_eur"], ascending=False)
tm_key = tmv.drop_duplicates(subset=["norm_name", "birth_year"], keep="first")
print("Transfermarkt players (with value, deduped):", len(tm_key))

tm_cols = ["player_id","name","norm_name","birth_year","market_value_in_eur",
           "highest_market_value_in_eur","position","sub_position",
           "current_club_name","country_of_citizenship","contract_expiration_date","foot","height_in_cm"]

# ---- primary join: name + birth year ----
merged = fb.merge(tm_key[tm_cols], on=["norm_name","birth_year"], how="left",
                  suffixes=("_fbref","_tm"))
matched = merged["market_value_in_eur"].notna()
print(f"\nPrimary match (name+birth year): {matched.sum()}/{len(merged)} = {matched.mean()*100:.1f}%")

# ---- fallback for unmatched: name-only (unique names) ----
unm = merged[~matched].copy()
name_counts = tm_key["norm_name"].value_counts()
uniq_names = set(name_counts[name_counts == 1].index)
tm_nameonly = tm_key[tm_key["norm_name"].isin(uniq_names)].set_index("norm_name")
fill_idx = []
for i, r in unm.iterrows():
    nm = r["norm_name"]
    if nm in tm_nameonly.index:
        for c in tm_cols:
            if c in ("norm_name","birth_year"): continue
            merged.at[i, c] = tm_nameonly.at[nm, c]
        fill_idx.append(i)
print(f"Fallback name-only fills: {len(fill_idx)}")

final_matched = merged["market_value_in_eur"].notna()
print(f"TOTAL matched: {final_matched.sum()}/{len(merged)} = {final_matched.mean()*100:.1f}%")

merged["value_millions_eur"] = merged["market_value_in_eur"]/1e6
os.makedirs(OUT, exist_ok=True)
merged.to_csv(f"{OUT}/fbref_transfermarkt_merged.csv", index=False)
print("\nSaved: fbref_transfermarkt_merged.csv  shape:", merged.shape)

# spot check
print("\n--- sample matched players ---")
cols = ["Player","Squad","Comp","birth_year","Gls","Ast","value_millions_eur","current_club_name"]
print(merged[final_matched][cols].head(12).to_string(index=False))
print("\n--- sample UNMATCHED (need review) ---")
print(merged[~final_matched][["Player","Squad","birth_year"]].head(10).to_string(index=False))
