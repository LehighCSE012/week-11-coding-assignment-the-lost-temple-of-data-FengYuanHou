"""
Adventure parser module for processing data files from the Lost Temple of Azmar.
Includes functions to load artifact data from Excel, location notes from TSV,
and extract dates and secret codes from journal text.
"""

import datetime
import re

import pandas as pd

def load_artifact_data(excel_filepath):
    """
    Reads artifact data from a specific sheet ('Main Chamber') in an Excel file,
    skipping the first 3 rows.

    Args:
        excel_filepath (str): The path to the artifacts Excel file.

    Returns:
        pandas.DataFrame: DataFrame containing the artifact data.
    """
    df = pd.read_excel(excel_filepath, sheet_name="Main Chamber", skiprows=3)
    return df

def load_location_notes(tsv_filepath):
    """
    Reads location data from a Tab-Separated Value (TSV) file.

    Args:
        tsv_filepath (str): The path to the locations TSV file.

    Returns:
        pandas.DataFrame: DataFrame containing the location data.
    """
    df = pd.read_csv(tsv_filepath, sep='\t')
    return df

def extract_journal_dates(journal_text):
    """
    Extracts all valid dates in MM/DD/YYYY format from the journal text.
    Only dates that pass datetime.strptime() validation are returned.

    Args:
        journal_text (str): The full text content of the journal.

    Returns:
        list[str]: A list of valid date strings found in the text.
    """
    found_dates = re.findall(r"\d{2}/\d{2}/\d{4}", journal_text)
    valid_dates = []
    for d in found_dates:
        try:
            datetime.datetime.strptime(d, "%m/%d/%Y")
            valid_dates.append(d)
        except ValueError:
            pass
    return valid_dates

def extract_secret_codes(journal_text):
    """
    Extracts all secret codes in AZMAR-XXX format (where XXX are digits)
    from the journal text.

    Args:
        journal_text (str): The full text content of the journal.

    Returns:
        list[str]: A list of secret code strings found in the text.
    """
    found_codes = re.findall(r"AZMAR-\d{3}", journal_text)
    return found_codes

def main():
    """
    Simulates processing the artifact and location data, and extracting information
    from the journal.
    """
    excel_file = 'artifacts.xlsx'
    tsv_file = 'locations.tsv'
    journal_file = 'journal.txt'

    print(f"--- Loading Artifact Data from {excel_file} ---")
    try:
        artifacts_df = load_artifact_data(excel_file)
        print("Successfully loaded DataFrame. First 5 rows:")
        print(artifacts_df.head())
        print("\nDataFrame Info:")
        artifacts_df.info()
    except FileNotFoundError:
        print(f"Error: File not found at {excel_file}")

    print(f"\n--- Loading Location Notes from {tsv_file} ---")
    try:
        locations_df = load_location_notes(tsv_file)
        print("Successfully loaded DataFrame. First 5 rows:")
        print(locations_df.head())
        print("\nDataFrame Info:")
        locations_df.info()
    except FileNotFoundError:
        print(f"Error: File not found at {tsv_file}")

    print(f"\n--- Processing Journal from {journal_file} ---")
    try:
        with open(journal_file, 'r', encoding='utf-8') as f:
            journal_content = f.read()

        print("\nExtracting Dates...")
        dates_list = extract_journal_dates(journal_content)
        print(f"Found dates: {dates_list}")

        print("\nExtracting Secret Codes...")
        codes_list = extract_secret_codes(journal_content)
        print(f"Found codes: {codes_list}")

    except FileNotFoundError:
        print(f"Error: File not found at {journal_file}")

if __name__ == '__main__':
    main()
