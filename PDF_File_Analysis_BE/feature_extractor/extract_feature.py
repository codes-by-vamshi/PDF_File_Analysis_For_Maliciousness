#!/usr/bin/env python3

import hashlib
import json
import os
import argparse
import sys
from feature_extractor.feature_specs.pdf_property_spec import PdfFeatureSpec
from feature_extractor.property_collector import PdfPropertyCollector

def save_json(output_path: str, obj):
    """Save to json"""
    args = {}
    args.update({'sort_keys': True, 'indent': 4})
    with open(output_path, 'w') as fp:
        json.dump(obj, fp, **args)
        fp.close()


def to_dict(obj):
    result = {}
    for att in dir(obj):
        if not att.startswith("__"):
            attr_obj = getattr(obj, att)
            if callable(attr_obj):
                continue
            if hasattr(attr_obj, "__dict__"):
                result[att] = to_dict(attr_obj)
            else:
                try:
                    # Attempt to serialize the attribute; skip if not serializable
                    json.dumps(attr_obj)
                    result[att] = attr_obj
                except TypeError:
                    # Handle non-serializable attribute (customize as needed)
                    result[att] = str(attr_obj)
    return result

def get_features(file_path: str=None,  properties_dir: str = None, return_properties = False, category=None):
    
    properties = PdfPropertyCollector(file_path).collect_properties()

    # Save properties
    if properties_dir:
        if category == 'malicious':
            path = os.path.join(properties_dir, 'malicious')
        else:
            path = os.path.join(properties_dir, 'benign')
        if not os.path.isdir(path):
            os.makedirs(path)
        name_ = hashlib.sha256(file_path.encode()).hexdigest()
        output_path = os.path.join(path, f"{name_}.properties.json")
        save_json(output_path, to_dict(properties))
        print(f'Saved properties to {output_path}')

    # extract features
    try:
        features = PdfFeatureSpec().dump(properties)
    except Exception as exc:
        print(f'{file_path} Failed to process {exc}')
        raise

    if return_properties:
        return features, properties

    return features


def save_features(file_name: str, output_dir: str = None, category = None):
    """
    save feature files to output dir
    :param file_name: path to file
    :param output_dir: output dir
    :return: features
    """
    # get features
    print(f'Extracting properties and features for {file_name}')
    features = get_features(file_name, output_dir, category=category)
    
    if output_dir:
        if category:
            if category == 'malicious':
                path = os.path.join(output_dir, 'malicious')
            else:
                path = os.path.join(output_dir, 'benign')
            if not os.path.isdir(path):
                os.makedirs(path)
            name_ = hashlib.sha256(file_name.encode()).hexdigest()
            output_path = os.path.join(path, f"{name_}.features.json")
        #save_json(output_path, features) # save example feature engineered data
        #print(f'Saved features to {output_path}')

    return features

def process_files(category, file_folder_path, output_folder_path, properties_dir):
    file_folder_path = os.path.join(os.getcwd(), file_folder_path)
    for filename in os.listdir(file_folder_path):
        input_file_path = os.path.join(file_folder_path, filename)
        features = save_features(file_name=input_file_path,output_dir= output_folder_path, properties_dir=properties_dir, category=category)

    print("File processing complete.")


def process_files(category, file_folder_path, output_folder_path):
    if not os.path.exists(file_folder_path):
        print(f"Error:Input Folder not found - {file_folder_path}")
        return

    if not os.path.exists(output_folder_path):
        os.mkdir(output_folder_path)

    file_folder_path = os.path.join(os.getcwd(), file_folder_path)
    print(f"Processing files in: {file_folder_path}")

    for filename in os.listdir(file_folder_path):
        input_file_path = os.path.join(file_folder_path, filename)
        save_features(file_name=input_file_path, output_dir=output_folder_path, category=category)

    print("File processing complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process files and save features.")
    parser.add_argument("--cat", dest="category", choices=["malicious", "benign"], required=True, help="Category of the files (malicious or benign)")
    parser.add_argument("--in", dest="input_folder_path", required=True, help="Path to the folder containing files")
    parser.add_argument("--out", dest="output_folder_path", required=True, help="Path to the folder to save features")

    args = parser.parse_args()

    if not all([args.category, args.input_folder_path, args.output_folder_path]):
        print("Error: All required arguments must be provided.")
        sys.exit(1)

    try:
        process_files(args.category, args.input_folder_path, args.output_folder_path)
    except Exception as e:
        print(f"Error: {e}")
