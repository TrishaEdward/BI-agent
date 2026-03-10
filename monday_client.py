import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MONDAY_API_KEY")
DEALS_BOARD_ID = os.getenv("DEALS_BOARD_ID")
WORK_BOARD_ID = os.getenv("WORK_BOARD_ID")

URL = "https://api.monday.com/v2"

HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}


def fetch_board_data(board_id):

    query = f"""
    query {{
      boards(ids: {board_id}) {{
        items_page {{
          items {{
            name
            column_values {{
              column {{
                title
              }}
              text
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(URL, json={"query": query}, headers=HEADERS)

    data = response.json()

    if "data" not in data:
        print("API Error:", data)
        return []

    items = data["data"]["boards"][0]["items_page"]["items"]

    results = []

    for item in items:

        row = {"Deal Name": item["name"]}

        for col in item["column_values"]:
            column_name = col["column"]["title"]
            column_value = col["text"]

            row[column_name] = column_value

        results.append(row)

    return results


def fetch_deals():
    return fetch_board_data(DEALS_BOARD_ID)


def fetch_work_orders():
    return fetch_board_data(WORK_BOARD_ID)


if __name__ == "__main__":

    print("\nFETCHING DEALS DATA...\n")
    deals = fetch_deals()

    for d in deals:
        print(d)

    print("\nFETCHING WORK ORDERS DATA...\n")
    work_orders = fetch_work_orders()

    for w in work_orders:
        print(w)