#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas", "tqdm"]
# ///

import pandas as pd
import subprocess
import argparse
import time
from tqdm import tqdm


def process_table_llm(input_file, prompt, sleep_time=1, out_file="out.csv", model="ollama:gpt-oss:20b", new_col="new", verbose=False):
    # Load the data
    org_dat = pd.read_csv(input_file)
    dat = org_dat.copy()
    dat[new_col] = None

    for i, row in tqdm(dat.iterrows(), total=dat.shape[0], desc="Processing"):
        # Construct the prompt
        final_prompt = eval(f"f'{prompt}'")
        cmd = f"aichat --role %functions% --model {model} '{final_prompt}'"

        # Print the command being executed
        if verbose:
            print(f"I: {i + 1}, CMD: {cmd}, CMD: {cmd}")

        # Execute the command and capture the result
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)
        dat.at[i, new_col] = result.stdout.strip()

        time.sleep(sleep_time)

    # Save the updated DataFrame to the output file
    dat.to_csv(out_file, index=False)

    # Print the command being executed
    if verbose:
        print(dat.head())

    print(f"Data saved to {out_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a table with an LLM")
    parser.add_argument("-i", "--input_file", type=str, required=True, help="Path to input CSV file")
    parser.add_argument("-p", "--prompt", type=str, required=True, help="Prompt")
    parser.add_argument("-o", "--out_file", type=str, nargs="?", default="out.csv", help="Path to output CSV file")
    parser.add_argument("-n", "--new_col", type=str, nargs="?", default="new", help="Name of the new column")
    parser.add_argument("-m", "--model", type=str, nargs="?", default="ollama:gemma2:27b", help="LLM model")
    parser.add_argument("-s", "--sleep", type=float, default=1, help="Sleep time between iterations")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show debugging info")
    args = parser.parse_args()

    process_table_llm(
        input_file=args.input_file,
        prompt=args.prompt,
        sleep_time=args.sleep,
        out_file=args.out_file,
        model=args.model,
        new_col=args.new_col,
        verbose=args.verbose
    )
