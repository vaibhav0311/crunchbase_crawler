# System imports
import os, sys, httplib, urllib, csv, json

# External imports
import unicodecsv

# Be sure api key is passed in aas argument
if len(sys.argv) != 2:
    print "USAGE: python crawler USER_KEY"
    exit(1)

# Initialize constants
USER_KEY = sys.argv[1]
CRUNCH_BASE_ENDPOINT = "api.crunchbase.com"
API_ENDPOINT = "/v/2"

# Look at most recently created 10000 companies
# Each page returns 1,000 records
PAGES = 10

# Read in timestamp file to keep track of previously collected data
TIMESTAMP_FILE = "last_timestamp.txt"
TIMESTAMP = None

if os.path.isfile(TIMESTAMP_FILE):
    TIMESTAMP = open(TIMESTAMP_FILE, 'r').readline().strip()

# Set up ssl connection to Crunchbase API
conn = httplib.HTTPSConnection(CRUNCH_BASE_ENDPOINT)

# Grab organization json for all ten pages
organizations = []
organizations_endpoint = "/organizations"
query_string_parameters = {
        "user_key": USER_KEY,
        "order": "created_at desc",
        }

for page in range(1, PAGES+1): # pages 1 to 10, range is exclusive
    query_string_parameters['page'] = page
    query_string = "?" + urllib.urlencode(query_string_parameters)
    url = API_ENDPOINT + organizations_endpoint + query_string

    conn.request("GET", url)
    resp = conn.getresponse().read()

    for organization in json.loads(resp)['data']['items']:
        # Check against created_at timestamp
        organizations.append(organization)


#@TODO: Collect data per company

keys = organizations[0].keys()
with open("output.csv", "w") as output_file:
    writer = unicodecsv.DictWriter(output_file, keys)
    writer.writeheader()
    writer.writerows(organizations)

#@TODO: write timestamp file

