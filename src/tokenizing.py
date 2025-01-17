import pandas as pd

# Load the CSV file
csv_file = 'C:\\Users\\Aman\\Desktop\\kifyaw5\\data\\telegram_data_preprocessed_valid.csv'
df = pd.read_csv(csv_file)


from nltk.tokenize import word_tokenize

# Tokenize each message
df['Tokens'] = df['Message'].apply(word_tokenize)

# Save the tokenized data
df.to_csv('data/telegram_data_tokenized.csv', index=False)

print("Tokenized data saved to 'data/telegram_data_tokenized.csv'.")
