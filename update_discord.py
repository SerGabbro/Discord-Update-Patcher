#!/usr/bin/env python3
import requests
import json

def search_for_latest_version(branch):
    if branch not in ["canary", "ptb", "stable"]:
        raise ValueError("Invalid branch")
    url = f"https://discord.com/api/updates/{branch}?platform=linux"
    print(f"Getting current version from {url}")
    resp = requests.get(url)
    if resp.status_code != 200:
        raise ValueError(f"Could not get current version: {resp.status_code}")
    data = resp.json()
    return data["name"]

def update_discord_version(file_path, new_version):
    try:
        with open(file_path, 'r') as file:
            build_info = json.load(file)

        current_version = build_info['version']
        print(f"Current Discord version: {current_version}")

        # Skip update if the version is the same
        if current_version == new_version:
            print(f"Version is already up-to-date: {new_version}. Skipping update.")
            return

        # Update version in the JSON file
        build_info['version'] = new_version

        # Save the changes
        with open(file_path, 'w') as file:
            json.dump(build_info, file, indent=4)

        print(f"Discord version updated to: {new_version}")
    
    except Exception as e:
        print(f"Error while updating the file: {e}")

# Get the latest stable version using the renamed function
latest_version = search_for_latest_version("stable")

# Update the version in the build_info.json file
update_discord_version("/usr/share/discord/resources/build_info.json", latest_version)
