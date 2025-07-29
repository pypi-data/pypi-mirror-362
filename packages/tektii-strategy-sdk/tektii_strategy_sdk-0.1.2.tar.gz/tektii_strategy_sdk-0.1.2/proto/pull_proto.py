"""Fetch the strategy.proto file from GitHub and save it locally.

This script retrieves the strategy.proto file from the specified GitHub repository
and saves it in the local `./proto` directory. It handles errors related to network issues and file system operations.
"""

import os

import requests  # type: ignore


def fetch_proto_file() -> None:
    """Fetch the backtest.proto file from GitHub and save it locally."""
    print("Fetching proto file from GitHub...")

    try:
        # Repo info
        owner = "Tektii"
        repo = "tektii-strategy-proto"
        path = "strategy.proto"
        branch = "main"

        # GitHub API endpoint for raw file content
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"

        # Headers with authentication
        headers = {
            "Accept": "application/vnd.github.v3.raw",
        }

        # Make the request
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Save the file
        os.makedirs("./proto", exist_ok=True)
        with open("./proto/strategy.proto", "wb") as f:
            f.write(response.content)
    except requests.RequestException as e:
        print(f"Error fetching proto file: {e}")
        raise e
    except EnvironmentError as e:
        print(f"EnvironmentError: {e}")
        raise e
    else:
        print("Proto file fetched and saved successfully.")


if __name__ == "__main__":
    fetch_proto_file()
