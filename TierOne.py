import http.client
import json
import csv
import os
import time


class TierOne:
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
            with open(filename, "w", newline="", encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                header = response_json[0].keys()
                csv_writer.writerow(header)
                for item in response_json:
                    csv_writer.writerow(item.values())

    def save_unique_tickers(self, response_json, filename):
        # Extract unique tickers from the list of dictionaries
        unique_tickers = set(item['Ticker'] for item in response_json)
        
        # Write the unique tickers to the specified file
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

    def process_data(self, endpoint, data_directory, file_prefix):
        response_json = self.fetch_data(endpoint)

        if response_json is not None:
            os.makedirs(data_directory, exist_ok=True)

            # json_filename = os.path.join(data_directory, file_prefix+".json")
            csv_filename = os.path.join(data_directory, file_prefix+".csv")
            tickers_filename = os.path.join(
                data_directory, file_prefix+"_unique_tickers.txt")

            # self.save_json_response(response_json, json_filename)
            self.save_csv_response(response_json, csv_filename)
            self.save_unique_tickers(response_json, tickers_filename)

            # print(f"\tJSON data saved to {json_filename}")
            print(f"\tCSV data saved to {csv_filename}")
            print(f"\tUnique Tickers saved to {tickers_filename}")

        else:
            print("No valid JSON data to process.")

    def get_all_unique_tickers(self, data_folder):
        # Check if the "data" directory exists
        if os.path.exists(data_folder) and os.path.isdir(data_folder):
            # Create an empty set to store unique tickers
            unique_tickers = set()

            # Loop through files in the data folder
            for filename in os.listdir(data_folder):
                if filename.endswith("_unique_tickers.txt"):
                    file_path = os.path.join(data_folder, filename)
                    with open(file_path, "r") as tickers_file:
                        # Read each line from the file and add it to the set
                        for line in tickers_file:
                            ticker = line.strip()
                            unique_tickers.add(ticker)

            # Define the path for the output file within the "data" directory
            output_file = os.path.join(data_folder, "tickers.txt")

            # Convert the set to a sorted list
            sorted_unique_tickers = sorted(unique_tickers)

            # Write the unique tickers to the output file
            with open(output_file, "w") as output:
                for ticker in sorted_unique_tickers:
                    output.write(ticker + "\n")

            print(f"\tUnique tickers saved to {output_file}")
        else:
            print(f"The '{data_folder}' directory does not exist.")


if __name__ == "__main__":
    token_file_path = "token.txt"
    data_directory = "data"
    endpoints_file = "tier_one_endpoints.txt"

    # Read endpoints from the file
    with open(endpoints_file, "r") as file:
        endpoints_data = file.readlines()

    print(f"Processing QuiverAPI endpoints\n")
    print(f"\n--------------------------------------------------------------")

    for line in endpoints_data:
        # Parse the endpoint details
        endpoint_parts = line.strip().split(",")
        if len(endpoint_parts) < 2:
            continue  # Skip invalid lines

        endpoint_url = endpoint_parts[0].strip()
        endpoint_name = endpoint_parts[1].strip().replace('"', '')
        query_parameters = []

        # Check if there are query parameters
        if len(endpoint_parts) > 2:
            query_parameters = [param.strip().replace(":", "=")
                                for param in endpoint_parts[2:]]

        # Merge query parameters into the endpoint URL
        if query_parameters:
            endpoint_url += "?" + "&".join(query_parameters)

        # Remove quotes
        endpoint_url = endpoint_url.replace('"', '')

        # # Create TierOne object and fetch data
        tier_one_obj = TierOne(token_file_path)
        tier_one_obj.process_data(endpoint_url, data_directory, endpoint_name)

        print(f"\n > {endpoint_name} data processed")
        print(f"\n**************************************************************")

        # Add a delay of 5 seconds between requests
        time.sleep(5)

    print("get all Unique tickers ")

    tier_one_obj.get_all_unique_tickers(data_directory)

    print(f"\nAll endpoints in {endpoints_file} completed")
    print(f"\n**************************************************************")
