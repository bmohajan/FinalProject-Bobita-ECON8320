import requests
import json
import prettytable
import pandas as pd
series_ids = ['LNS14000000','CES0000000001','CES0500000002']
headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": series_ids,"startyear":"2015", "endyear":"2024"})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)
series_list = json_data['Results']['series']

def month_name_to_number(month_name):
  month_dict = {
      "January": 1,
      "February": 2,
      "March": 3,
      "April": 4,
      "May": 5,
      "June": 6,
      "July": 7,
      "August": 8,
      "September": 9,
      "October": 10,
      "November": 11,
      "December": 12
  }
  return month_dict.get(month_name)


all_data_df = pd.DataFrame()
for i, series in enumerate(series_list):
    df_series = pd.DataFrame(series["data"])
    df_series["series_id"] = series_ids[i]

    df_series = df_series[["year", "periodName", "value", "series_id"]]
    df_series.rename(columns={
        "series_id": "series_id",
        "year": "Year",
        "periodName": "Month",
        "value": "Value"
    }, inplace=True)
    all_data_df = pd.concat([all_data_df, df_series])
all_data_df["Month"] = all_data_df["Month"].apply(month_name_to_number)
all_data_df.to_csv("data.csv", index=False)