import http.client
import json
import csv
import os

class LiveLobbying:
    def __init__(self, token_file_path):
        self.token_file_path = token_file_path
        self.base_url = "api.quiverquant.com"
        self.headers = {
            'Accept': "application/json",
            'Authorization': self.read_api_token()
        }

    def read_api_token(self):
        try:
            with open(self.token_file_path, "r") as token_file:
                return "Bearer " + token_file.read().strip()
        except FileNotFoundError:
            raise Exception("Token file not found.")

    def make_request(self, endpoint):
        conn = http.client.HTTPSConnection(self.base_url)
        conn.request("GET", endpoint, headers=self.headers)
        res = conn.getresponse()
        data = res.read()
        return data

    def save_json_response(self, response_json, filename):
        with open(filename, "w") as json_file:
            json.dump(response_json, json_file, indent=4)

    def save_csv_response(self, response_json, filename):
        if isinstance(response_json, list) and len(response_json) > 0:
            with open(filename, "w", newline="", encoding="utf-8") as csv_file:  # Specify encoding here
                csv_writer = csv.writer(csv_file)
                header = response_json[0].keys()
                csv_writer.writerow(header)
                for item in response_json:
                    csv_writer.writerow(item.values())


    def save_unique_tickers(self, response_json, filename):
        unique_tickers = set(item['Ticker'] for item in response_json)
        with open(filename, "w") as tickers_file:
            for ticker in unique_tickers:
                tickers_file.write(ticker + "\n")

    def fetch_data(self, endpoint):
        data = self.make_request(endpoint)
        if data:
            try:
                response_json = json.loads(data.decode("utf-8"))
                return response_json
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        else:
            print("Empty response from the API.")
        return None

    def process_data(self, endpoint, data_directory):
        response_json = self.fetch_data(endpoint)

        if response_json is not None:
            os.makedirs(data_directory, exist_ok=True)

            json_filename = os.path.join(data_directory, "live_lobbying.json")
            csv_filename = os.path.join(data_directory, "live_lobbying.csv")
            tickers_filename = os.path.join(data_directory, "live_lobbying__unique_tickers.txt")
            

            self.save_json_response(response_json, json_filename)
            self.save_csv_response(response_json, csv_filename)
            self.save_unique_tickers(response_json, tickers_filename)


            print(f"JSON data saved to {json_filename}")
            print(f"CSV data saved to {csv_filename}")
            print(f"Unique Tickers saved to {tickers_filename}")

        else:
            print("No valid JSON data to process.")


# Example usage:
if __name__ == "__main__":
    token_file_path = "token.txt"
    live_lobbying_endpoint = "/beta/live/lobbying"
    data_directory = "data"

    live_lobbying = LiveLobbying(token_file_path)
    live_lobbying.process_data(live_lobbying_endpoint, data_directory)
