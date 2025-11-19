"""create_splits.py

Creates train/validation/test CSV files required by `train_model.py`.

Usage:
  python create_splits.py --input american_bankruptcy.csv

If no input is given, the script will look for `american_bankruptcy.csv` in the
project root and will print instructions for downloading the dataset if it's
not present.
"""
import argparse
import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split


def make_splits(df, out_dir='.', seed=42):
    # first take 10% as test
    train_val, test = train_test_split(df, test_size=0.1, random_state=seed)
    # then split remaining into train (~80%) and validation (~10% of original)
    # 10% of total is 0.1111 of remaining 90%
    train, val = train_test_split(train_val, test_size=0.1111, random_state=seed)

    train.to_csv(os.path.join(out_dir, 'train.csv'), index=False)
    val.to_csv(os.path.join(out_dir, 'validation.csv'), index=False)
    test.to_csv(os.path.join(out_dir, 'test.csv'), index=False)

    print(f"Saved train.csv ({len(train)} rows), validation.csv ({len(val)} rows), test.csv ({len(test)} rows)")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', help='Path to raw dataset CSV (american_bankruptcy.csv)')
    args = parser.parse_args()

    input_path = args.input or 'american_bankruptcy.csv'

    if not os.path.exists(input_path):
        print(f"Dataset file not found at '{input_path}'.")
        print("Options to obtain the dataset:")
        print("  1) Download from Kaggle: https://www.kaggle.com/datasets/utkarshx27/american-companies-bankruptcy-prediction-dataset")
        print("     - Install kaggle CLI and place your kaggle.json in ~/.kaggle or set KAGGLE_CONFIG_DIR on Windows.")
        print("     - Example (PowerShell):")
        print("         pip install kaggle")
        print("         kaggle datasets download -d utkarshx27/american-companies-bankruptcy-prediction-dataset")
        print("         unzip american-companies-bankruptcy-prediction-dataset.zip")
        print("         move american_bankruptcy.csv .\")
        print("")
        print("  2) If you already have the dataset CSV, provide its path to this script:")
        print("         python create_splits.py --input path/to/american_bankruptcy.csv")
        sys.exit(1)

    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        sys.exit(1)

    # Basic sanity checks
    if df.shape[0] < 10:
        print(f"Dataset looks too small ({df.shape[0]} rows). Aborting.")
        sys.exit(1)

    make_splits(df)
