import re
import emoji

import pandas as pd

# Load the CSV file
csv_file = 'data/telegram_data.csv'
df = pd.read_csv(csv_file)

# Display basic information
print(df.head())  # Preview the first few rows


def preprocess_text(text):
    if isinstance(text, str):  # Only process text if it's a string
        # Replace emojis with their descriptions (e.g., 😊 → ":slightly_smiling_face:")
        text = emoji.demojize(text)
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        # Remove unwanted characters (retain Amharic and basic punctuation)
        text = re.sub(r'[^\w\s፡።፤፥፦፧]', '', text)
        # Normalize spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    return ""  # Return an empty string for non-string inputs


# Apply text preprocessing
df['Message'] = df['Message'].apply(preprocess_text)

# Verify changes
print(df[['Message']].head())

import os
import sys

# Specify the desired file path
directory = "C:\\Users\\Aman\\Desktop\\kifyaw5\\data"
filename = "pre_processed.csv"
file_path = os.path.join(directory, filename)

# Ensure the directory exists
if not os.path.exists(directory):
    print(f"Directory {directory} does not exist. Creating it...")
    os.makedirs(directory)

# Write data to the file
with open(file_path, 'w') as file:
    file.write("Hello, this is an example file.")

print(f"File saved at: {file_path}") 

