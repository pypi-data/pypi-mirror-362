import sys
import requests
import argparse
from osilic.model import license_from_dict, print_licenses_table, print_license_details_table, print_licenses_table_with_steward

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="osilic",
        description="OSI License CLI: List, search, and show license details."
    )
    parser.add_argument("spdx_id", nargs="?", help="SPDX ID of the license to show details for.")
    parser.add_argument("-s", "--search", metavar="SEARCH_KEY", help="Search licenses by name.")
    parser.add_argument("-w", "--steward", metavar="STEWARD_KEY", help="Search licenses by steward.")
    parser.add_argument("-k", "--keyword", metavar="FILTER_KEY", help="Filter licenses by keyword.")
    args = parser.parse_args()

    base_url = "https://opensource.org/api/license"

    if args.keyword:
        # Search licenses by steward
        resp = requests.get(f"{base_url}?keyword={args.keyword}")
        if resp.status_code == 200:
            licenses = license_from_dict(resp.json())
            if len(licenses)>0:
                print_licenses_table(licenses)
            else:
                print("No licenses found for keyword:", args.keyword)
                # Get all licenses and then stewards for display
                resp = requests.get(base_url)
                unique_keywords = set()
                if resp.status_code == 200:
                    licenses = license_from_dict(resp.json())
                    for license in licenses:
                        keywords=license.keywords
                        #print(f"Debug: {keywords}")
                        if len(keywords) > 0:
                            for keyword in keywords:
                                unique_keywords.add(str(keyword.value))
                    print("Please choose a keyword key from this list:",unique_keywords)
                else:
                    print("Error fetching licenses while listing all keywords:", resp.text)
        else:
            print("Error {resp.text} while searching licenses for keyword: {args.keyword}")

    elif args.steward:
        # Search licenses by steward
        resp = requests.get(f"{base_url}?steward={args.steward}")
        if resp.status_code == 200:
            licenses = license_from_dict(resp.json())
            if len(licenses)>0:
                print_licenses_table_with_steward(licenses)
            else:
                print("No licenses found for steward:", args.steward)
                # Get all licenses and then stewards for display
                resp = requests.get(base_url)
                unique_stewards = set()
                if resp.status_code == 200:
                    licenses = license_from_dict(resp.json())
                    for license in licenses:
                        if len(license.stewards) > 0:
                            unique_stewards.update(license.stewards)
                    print("Please choose a steward key from this list:",unique_stewards)
                else:
                    print("Error fetching licenses while listing all stewards:", resp.text)
        else:
            print("Error {resp.text} while searching licenses for steward:{args.steward}")

    elif args.search:
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