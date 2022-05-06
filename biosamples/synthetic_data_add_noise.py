import random
import string

import pandas as pd

DATA_FILE_NAME = "../resources/ukb_synthetic_data_tofu.csv"
OUTPUT_FILE_NAME = "../resources/ukb_synthetic_data_tofu_noise.csv"
NOISE_COLUMNS = [
    "Ethnic background-0.0",
    "Type of cancer: ICD10-0.0",
    "Histology of cancer tumour-0.0",
    "Type of cancer: ICD9-0.0",
    "Behaviour of cancer tumour-0.0",
    "Histology of cancer tumour-0.0",
    "Type of cancer: ICD9-0.0",
    "Behaviour of cancer tumour-0.0",
    "Cancer report format-0.0",
    "Cancer record origin-0.0",
    "Past tobacco smoking-0.0",
    "Source of report of K85 (acute pancreatitis)-0.0",
    "Source of report of K86 (other diseases of pancreas)-0.0",
    "Qualifications-0.0",
    "C-reactive protein reportability-0.0",
    "Country of birth (UK/elsewhere)-0.0",
    "Operative procedures - OPCS4-0.0",
    "Blood, blood-forming organs and certain immune disorders",
    "Endocrine, nutritional and metabolic diseases",
    "Mental and behavioural disorders",
    "Nervous system disorders",
    "Digestive system disorders",
    "Respiratory system disorders",
    "Circulatory system disorders"
]


def main():
    edit_distance = 2
    percentage = 5
    add_noise_to_dataset(edit_distance, percentage)


def add_noise_to_dataset(edit_distance, percentage):
    syn_data = read_synthetic_data(DATA_FILE_NAME)

    for column in NOISE_COLUMNS:
        add_noise_to_column(syn_data, column, edit_distance, percentage)

    syn_data.to_csv(OUTPUT_FILE_NAME, sep=',', index=False)


def add_noise_to_column(df, column, edit_distance, percentage):
    total_records = df.shape[0]
    edit_records = int(total_records * percentage / 100)
    for n in range(edit_records):
        random_row = random.randrange(0, total_records)
        value = df[column][random_row]
        df[column][random_row] = edit_value(str(value), edit_distance)
        print(df[column][random_row])


def edit_value(value, edit_distance):
    if not isinstance(value, str) or len(value) == 0:
        return value

    val_len = len(value)
    for i in range(edit_distance):
        rand_char = random.choice(string.ascii_letters).lower()
        pos = random.randrange(0, val_len)
        value = value[0:pos] + rand_char + value[pos + 1:val_len]

    return value


def read_synthetic_data(file_name):
    synthetic_data = pd.read_csv(file_name)
    return synthetic_data


if __name__ == '__main__':
    main()
