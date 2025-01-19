import pandas as pd
import re
# Load the dataset
csv_file = 'data/telegram_data_preprocessed_valid.csv'
df = pd.read_csv(csv_file)

# Select a subset of messages for labeling
subset = df['Message'].dropna().sample(50, random_state=42)  # Adjust sample size as needed
def tokenize_amharic(text):
    # Simple whitespace-based tokenizer; improve if needed
    return re.findall(r'\S+', text)

def annotate_message(message):
    tokens = tokenize_amharic(message)
    labeled_tokens = []
    
    for token in tokens:
        # Replace with manual or semi-automated labeling logic
        if re.match(r'^\d+', token):  # Example for price
            labeled_tokens.append((token, 'B-PRICE' if len(labeled_tokens) == 0 or labeled_tokens[-1][1] != 'B-PRICE' else 'I-PRICE'))
        elif "አዲስ" in token or "ቦሌ" in token:  # Example for location
            labeled_tokens.append((token, 'B-LOC'))
        elif "ምርት" in token:  # Example for product
            labeled_tokens.append((token, 'B-Product'))
        else:
            labeled_tokens.append((token, 'O'))
    return labeled_tokens

# Save the annotated data to a CoNLL-formatted text file
output_file = 'data/labeled_data.conll'

with open(output_file, 'w', encoding='utf-8') as f:
    for message in subset:
        annotated_tokens = annotate_message(message)
        for token, label in annotated_tokens:
            f.write(f"{token}\t{label}\n")
        f.write("\n")  # Separate messages with a blank line

# print(f"Labeled data saved to {output_file}.")

