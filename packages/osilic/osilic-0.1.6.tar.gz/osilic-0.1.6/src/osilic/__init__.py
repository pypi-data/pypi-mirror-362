import sys
import requests
import argparse
from osilic.model import license_from_dict, print_licenses_table, print_license_details_table

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="osilic",
        description="OSI License CLI: List, search, and show license details."
    )
    parser.add_argument("spdx_id", nargs="?", help="SPDX ID of the license to show details for.")
    parser.add_argument("-s", "--search", metavar="SEARCH_KEY", help="Search licenses by name.")
    args = parser.parse_args()

    base_url = "https://opensource.org/api/license"

    if args.search:
        # Search licenses by name
        resp = requests.get(f"{base_url}?name={args.search}")
        if resp.status_code == 200:
            licenses = license_from_dict(resp.json())
            print_licenses_table(licenses)
        else:
            print("Error searching licenses:", resp.text)
    elif args.spdx_id:
        # Try to fetch license by SPDX ID
        spdx_id = args.spdx_id
        resp = requests.get(f"{base_url}/{spdx_id}")
        if resp.status_code == 404:
            data = resp.json()
            if "error" in data and data["error"] == "License not found.":
                print(f"License '{spdx_id}' not found.")
                print("Searching for similar licenses...")
                resp2 = requests.get(f"{base_url}?name={spdx_id}")
                if resp2.status_code == 200:
                    licenses = license_from_dict(resp2.json())
                    if licenses:
                        print("Are you looking for one of these licenses?")
                        print_licenses_table(licenses)
                    else:
                        print("No similar licenses found.")
                else:
                    print("Error searching licenses:", resp2.text)
            else:
                print(data)
        elif resp.status_code == 200:
            data = resp.json()
            # Print details for the found license
            licenses = license_from_dict([data])
            print_license_details_table(licenses[0])
        else:
            print("Error fetching license:", resp.text)
    else:
        # Print all licenses
        resp = requests.get(base_url)
        if resp.status_code == 200:
            licenses = license_from_dict(resp.json())
            print_licenses_table(licenses)
        else:
            print("Error fetching licenses:", resp.text)

if __name__ == "__main__":
    main()