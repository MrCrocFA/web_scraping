import pandas as pd
import requests
from lxml import html
import time

start = time.time()
url = "https://www.investing.com/economic-calendar/"

while True:
    response = requests.get(url)

    tree = html.fromstring(response.content)

    rows = tree.xpath("//table[@id='economicCalendarData']//tbody//tr")
    row_40 = rows[1]  # Get the 6th row (index 5)
    tds_40 = row_40.xpath(".//td")
    actual_value_40 = tds_40[4].text_content().strip()

    rows = tree.xpath("//table[@id='economicCalendarData']//tbody//tr")
    row_43 = rows[2]  # Get the 6th row (index 5)
    tds_43 = row_43.xpath(".//td")
    actual_value_43 = tds_43[4].text_content().strip()

    rows = tree.xpath("//table[@id='economicCalendarData']//tbody//tr")
    row_44 = rows[3]  # Get the 6th row (index 5)
    tds_44 = row_44.xpath(".//td")
    actual_value_44 = tds_44[4].text_content().strip()
    if actual_value_40 and actual_value_43 and actual_value_44:
        data_40 = {
            "Row": 40,
            "Actual": actual_value_40,
            "Forecast": tds_40[5].text_content().strip(),
            "Previous": tds_40[6].text_content().strip(),
        }
        data_43 = {
            "Row": 43,
            "Actual": actual_value_43,
            "Forecast": tds_43[5].text_content().strip(),
            "Previous": tds_43[6].text_content().strip(),
        }
        data_44 = {
            "Row": 44,
            "Actual": actual_value_44,
            "Forecast": tds_44[5].text_content().strip(),
            "Previous": tds_44[6].text_content().strip(),
        }
        df = pd.DataFrame([data_40,data_43,data_44])
        print(df)
        break
    else:
        print("No data in the 'Actual' field. Retrying...")
        time.sleep(5)  # Wait for 5 seconds before retrying


end = time.time()
print(f"Elapsed time: {end - start} seconds")