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

# Drop rows where 'Message' or 'Date' are missing
df.dropna(subset=['Message', 'Date'], inplace=True)

# Reset index after dropping rows
df.reset_index(drop=True, inplace=True)

# Create separate metadata dataframe
metadata_df = df[['Channel Title', 'Channel Username', 'ID', 'Date']].copy()

# Save metadata to a new CSV file
metadata_df.to_csv('data/telegram_metadata.csv', index=False)

# Save the preprocessed data into a new CSV file
df.to_csv('data/telegram_data_preprocessed.csv', index=False)



import os

def validate_media_paths(media_path):
    # Check if the media path is a valid string
    if isinstance(media_path, str) and media_path.strip():
        return os.path.isfile(media_path)  # Return True if the file exists
    return False  # Return False for invalid or missing paths


# Add a column to indicate if the media path is valid
df['Media Valid'] = df['Media Path'].apply(validate_media_paths)

# Filter out rows with invalid media paths
df = df[df['Media Valid']]

# Drop the validation column before saving
df.drop(columns=['Media Valid'], inplace=True)

# Save the updated dataset
df.to_csv('data/telegram_data_preprocessed_valid.csv', index=False)





