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
    row = rows[58]  # Get the 6th row (index 5)
    tds = row.xpath(".//td")
    actual_value = tds[4].text_content().strip()
    if actual_value:
        data = {
            "Actual": actual_value,
            "Forecast": tds[5].text_content().strip(),
            "Previous": tds[6].text_content().strip(),
        }
        df = pd.DataFrame([data])
        print(df)
        break
    else:
        print("No data in the 'Actual' field. Retrying...")
        time.sleep(1)


end = time.time()
print(f"Elapsed time: {end - start} seconds")
print(time.ctime())