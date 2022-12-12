import json
import requests

def search_rcsb(ligand):
  # create a dictionary with the search parameters
  search_params = {
  "query": {
    "type": "group",
    "logical_operator": "and",
    "nodes": [
      {
        "type": "terminal",
        "service": "text",
        "parameters": {
          "attribute": "rcsb_nonpolymer_entity_annotation.comp_id",
          "operator": "exact_match",
          "negation": False,
          "value": ligand
        }
      },
      {
        "type": "terminal",
        "service": "text",
        "parameters": {
          "attribute": "rcsb_nonpolymer_entity_annotation.type",
          "operator": "exact_match",
          "value": "SUBJECT_OF_INVESTIGATION",
          "negation": False
        }
      }
    ],
    "label": "nested-attribute"
  },
  "return_type": "entry",
  "request_options": {
    "paginate": {
      "start": 0,
      "rows": 9999
    },
    "results_content_type": [
      "experimental"
    ],
    "sort": [
      {
        "sort_by": "score",
        "direction": "desc"
      }
    ],
    "scoring_strategy": "combined"
  }
}

  # convert the dictionary to JSON format
  search_request = json.dumps(search_params)

  # send the search request to the RCSB search API
  response = requests.get(f"https://search.rcsb.org/rcsbsearch/v2/query?json={search_request}")
  # return the response from the request
  # example usage: search for entries with "K" in their sequence
  data = json.loads(response.text)

  # Get a list of all the dictionaries in the "result_set" key
  result_set = data['result_set']

  # Create an empty list to store the identifiers
  identifiers = []

  # Loop through each dictionary in the result_set and add the
  # "identifier" value to the list of identifiers
  for entry in result_set:
      identifiers.append(entry['identifier'])
  
  return identifiers

response = search_rcsb("K")
print(response)