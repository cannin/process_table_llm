# process_table_llm
Process rows in a CSV table with an LLM using aichat


# Install
Install uv. Uses uv and PEP 723 (see: https://thisdavej.com/share-python-scripts-like-a-pro-uv-and-pep-723-for-easy-deployment/)

```
chmod +x process_table_llm.py
```

# Run 

Example:

```
./process_table_llm.py --input_file="mtcars.csv" --prompt="a single letter followed by the sum of {row[\"carb\"]} and {row[\"gear\"]}; single line; no explanation" --verbose
```

Access columns with {row[\"COLUMN_NAME\"]}; this is done with Python f-strings. 

