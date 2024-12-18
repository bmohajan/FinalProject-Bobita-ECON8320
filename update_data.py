import requests
import json
import pandas as pd
from datetime import datetime

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

def get_latest_data(series_ids, start_year, end_year):
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": series_ids,"startyear": str(start_year), "endyear": str(end_year)})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    return json_data['Results']['series']

def update_data(data_file="data.csv"):
    # Load existing data
    all_data_df = pd.read_csv(data_file)

    # Get latest year and month from existing data
    latest_year = all_data_df['Year'].max()
    latest_month = all_data_df[all_data_df['Year'] == latest_year]['Month'].max()

    # Calculate start year and month for API call
    current_year = datetime.now().year
    current_month = datetime.now().month
    start_year = latest_year
    start_month = latest_month + 1
    #print(current_year, current_month, start_year, start_month)
    # If the latest data is from December, start from January of the next year
    if start_month > 12:
        start_month = 1
        start_year += 1

    # Only collect data if there is new data available
    if start_year <= current_year and (start_year < current_year or start_month <= current_month):
        series_ids = ['LNS14000000','CES0000000001','CES0500000002']
        series_list = get_latest_data(series_ids, start_year, current_year)
        #print(series_list)
        new_data_df = pd.DataFrame()
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

            new_data_df = pd.concat([new_data_df, df_series])

        new_data_df["Month"] = new_data_df["Month"].apply(month_name_to_number)
        #print(new_data_df)
        # Filter new data based on start year and month
        new_data_df['Year'] = pd.to_numeric(new_data_df['Year'], errors='coerce')
        new_data_df.dropna(subset=['Year'], inplace=True)
        new_data_df = new_data_df[
            (new_data_df['Year'] > latest_year) |
            ((new_data_df['Year'] == latest_year) & (new_data_df['Month'] >= start_month))
        ]
        #print(new_data_df)
        # Concatenate old and new data
        all_data_df = pd.concat([all_data_df, new_data_df])

        # Save updated data
        all_data_df.to_csv(data_file, index=False)
def main():
    update_data()

if __name__ == "__main__":
    main()