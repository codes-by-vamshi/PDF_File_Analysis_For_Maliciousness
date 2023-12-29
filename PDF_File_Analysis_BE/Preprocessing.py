import os
import json
import pandas as pd
from urllib.parse import urlparse
from collections import defaultdict

requiredDomains = []
f = open('requiredDomains.txt', 'r')
while True:
    domain = f.readline()
    if(domain):
        requiredDomains.append(domain.rstrip())
    else:
        break
print(requiredDomains)

class PdfFilePreprocessing:
  def __init__(self, folderPath):
    self.files_path = self.getFilePaths(folderPath)
    self.files = {}
    self.topNUrls = 10
    self.kForCrossValidation = 10

    # Start Preprocessing
    self.preprocessing()

  def getFilePaths(self, folderPath):
    # Retrieve paths of all files in the specified folder
    files = os.listdir(folderPath)
    file_paths = []
    for file_name in files:
      file_paths.append(os.path.join(folderPath, file_name))
    return file_paths

  def preprocessing(self):
    # Extracting Yara Signatures
    yara_signatures = self.extractYaraSignatures()
    # Extracting Static Properties
    static_properties = self.extractStaticProperties()

    # Converting Yara Signatures to DataFrames
    yara_df = pd.DataFrame(yara_signatures)

    # Converting Static Properties to DataFrames
    static_properties_df = pd.DataFrame(static_properties).T
    
    urx_dicts = self.check_if_exists(requiredDomains)
    rows_dict = {}
    for outer_key, inner_dict in urx_dicts.items():
      rows_dict[outer_key] = inner_dict

    # Convert Urxs dictionary to DataFrame
    urx_df = pd.DataFrame(rows_dict).T

    # Combining all features to form benign and malicious dataframe
    self.df = pd.concat([yara_df, static_properties_df, urx_df], axis = 1)

  def extractYaraSignatures(self):
    # Initialize dictionaries to store YARA signatures
    yara_signatures = {}
    
    numOfFiles = len(self.files_path)
    
    # Extract YARA signatures
    for ind, file_path in enumerate(self.files_path):
      with open(file_path, 'r') as file:
        # Load JSON data from file and get YARA signatures
        yara_signatures = json.load(file)['yara_signatures']
        # Process each YARA signature in the file
        for yara_sign in yara_signatures:
          # Check if the signature already exists in the dictionaries
          if(yara_sign in yara_signatures):
            yara_signatures[yara_sign][ind] = 1
          else:
            # Initialize lists for all files with zeros
            yara_signatures[yara_sign] = [0 for i in range(numOfFiles)]
            yara_signatures[yara_sign][ind] = 1

    return yara_signatures

  def extractStaticProperties(self):
    # Initialize dictionaries to store static properties
    props = {}

    # Extract static properties
    for ind, file_path in enumerate(self.files_path):
      with open(file_path, 'r') as file:
        # Load JSON data from file and get static properties
        props[ind] = json.load(file)['static_properties']

    return props

  # Method to convert list of URLs to domain list
  def list_to_check(self, file_list):
      domain_list = []
      for url in file_list:
          domain_list.append(self.extract_domain(url))
      return domain_list

  # Method to extract domain from URL
  def extract_domain(self, url):
      parsed_url = urlparse(url)
      if parsed_url.netloc != '':
          return parsed_url.netloc
      else:
          path_parts = parsed_url.path.split('/')
          return path_parts[0] if path_parts[0] != '' else None

  # Method to count frequency of elements
  def frequency_counter(self, elements, frequency):
      for element in elements:
          if element in frequency:
              frequency[element] += 1
          else:
              frequency[element] = 1
      return frequency

  # Method to calculate ratio of dictionary values
  def calculate_ratio(self, dictionary):
      total_sum = sum(dictionary.values())
      for key, value in dictionary.items():
          ratio = value / total_sum
          dictionary[key] = (value, ratio)
      return dictionary

  def check_if_exists(self, requiredDomains):
    check_in = defaultdict(dict)

    for domain in requiredDomains:
      for ind, file_path in enumerate(self.files_path):
        regex_urls = []
        regex_uris = []
        pypdf_urls = []
        with open(file_path, 'r') as file:
          # Load JSON data from file and get Urx's(Url's,Uri's)
          loaded_file = json.load(file)
          for i in loaded_file['regex_urls']:
            regex_urls.append(self.extract_domain(i))
          for i in loaded_file['regex_uris']:
            regex_uris.append(self.extract_domain(i))
          for i in loaded_file['pypdf_uris']:
            pypdf_urls.append(self.extract_domain(i))
          regex_urls = list(set(regex_urls))
          regex_uris = list(set(regex_uris))
          pypdf_urls = list(set(pypdf_urls))
          if (domain in(regex_urls) or domain in(regex_uris) or domain in(pypdf_urls)):
            check_in[ind][domain] = 1
            continue
          check_in[ind][domain] = 0

    return check_in