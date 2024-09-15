import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
start = time.time()
url = "https://www.investing.com/economic-calendar/"

while True:
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    table = soup.select_one("#economicCalendarData")

    rows = table.select("tbody tr")
    if len(rows) < 6:
        print("The table does not contain enough rows.")
        break
    else:
        row = rows[5]  # Get the 6th row (index 5)
        tds = row.select("td")
        if len(tds) == 8:
            actual_value = tds[4].get_text(strip=True)
            if actual_value:
                data = {
                    "Actual": actual_value,
                    "Forecast": tds[5].get_text(strip=True),
                    "Previous": tds[6].get_text(strip=True),
                }
                df = pd.DataFrame([data])

                # df.head()
                #
                # df.to_csv('economic_calendar.csv', index=False)
                print(df)
                break
            else:
                print("No data in the 'Actual' field. Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
        else:
            print("The 6th row does not have the expected 8 columns.")
            break
end = time.time()
print(end-start)