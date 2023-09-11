# QuiverAnalyzerAPI

## Overview

The QuiverAnalyzerAPI is a Python-based client for the QuiverQuant API, allowing you to fetch financial and trading data from various endpoints. This readme provides instructions on how to deploy and use the QuiverAnalyzerAPI.

## Prerequisites

Before deploying the API client, ensure you have the following prerequisites:

- Python 3.x installed on your machine.
- An API token obtained from QuiverQuant. Save the token in a file named `token.txt` in the root directory of the project.

## Deployment

Follow these steps to deploy the QuiverAnalyzerAPI:

### 1. Clone the Repository

Clone this repository to your local machine using Git:

```bash
git clone https://github.com/EmmanuelMPaul/QuiverAnalyzerAPI.git
```

### 2. Run the Script

To fetch data from the specified endpoint, run the script using Python:

```bash
python LiveLobbying.py
```
Replace LiveLobbying.py with the name of the script corresponding to your chosen endpoint.

### 3. Data Directory

The fetched data will be saved in JSON and CSV formats in the data directory within the project root. Additionally, unique tickers (if available) will be saved in a text file with a name like <endpoint name>_unique_tickers.txt.

### Usage

The API client script makes a request to the QuiverQuant API using your API token and fetches data from the specified endpoint.

Fetched data is saved in the data directory and can be accessed for analysis or other applications.

### Example

For example, if you want to fetch data from the "Live Lobbying" endpoint, modify the live_lobbying_endpoint variable in LiveLobbying.py, then run the script:

```bash
python LiveLobbying.py
```

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgments

[QuiverQuant](https://api.quiverquant.com/docs/#/) for providing the API.
Happy data analysis!