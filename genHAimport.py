import pandas as pd

src_path = "oscar_export.csv"
df = pd.read_csv(src_path, encoding="latin1", sep=None, engine="python")

# Parse Start as datetime and floor to full hour
start_dt = pd.to_datetime(df["Start"], errors="coerce")
start_dt_truncated = start_dt.dt.floor("H")
start_strings = start_dt_truncated.dt.strftime("%d.%m.%Y %H:%M")

# Parse duration and round to 2 decimals (hours)
durations = pd.to_timedelta(df["Gesamte Zeit"], errors="coerce")
sleep_hours = (durations / pd.Timedelta(hours=1)).round(2)

# AHI values
ahi_values = pd.to_numeric(df["AHI"], errors="coerce")

records = []

for start_str, hours_val, ahi_val in zip(start_strings, sleep_hours, ahi_values):
    if pd.isna(hours_val) or pd.isna(ahi_val) or start_str == "NaT":
        continue

    # Sleep duration entry
    records.append({
        "statistic_id": "sensor.sleep_total_time",
        "unit": "h",
        "start": start_str,
        "min": hours_val,
        "max": hours_val,
        "mean": hours_val,
    })

    # AHI entry
    records.append({
        "statistic_id": "sensor.sleep_ahi",
        "unit": "events/h",
        "start": start_str,
        "min": ahi_val,
        "max": ahi_val,
        "mean": ahi_val,
    })

out_df = pd.DataFrame(records, columns=["statistic_id","unit","start","min","max","mean"])

out_path = "./oscar_import_sleep_ahi_6m.tsv"
out_df.to_csv(out_path, sep="\t", index=False, encoding="utf-8")

out_path, out_df.head(), len(out_df)

