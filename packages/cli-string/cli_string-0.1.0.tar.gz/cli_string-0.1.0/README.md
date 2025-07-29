# Unique Characters in a String

This CLI tool analyzes a string or a file containing strings and outputs **only the characters that appear exactly once** in each line (case-insensitive). Additionally, it measures the execution time of the function call.

---

## 🔍 Features

- ✅ Detects **unique characters only** (characters that appear exactly once).
- 🔠 **Case-insensitive** comparison (e.g., `'A'` and `'a'` are treated as the same).
- ♻️ **Result caching** with `functools.lru_cache` for optimized repeated calls.
- ⏱ **Execution time logging** using the custom `perf_counter_deco` decorator.

---

## 📦 Installation

1. Make sure you're using **Python 3.12** or later.
2. Install the package locally or from a distribution (if published):

```bash
pip install cli_string
```

⸻

🚀 Usage

Suppose your main script is named main.py.

Analyze a single string:

```python main.py --string "Example"```

Analyze lines from a file:

```python main.py --file path/to/file.txt```

⚠️ If both --string and --file are provided, the file input takes precedence.

Provide both string and file:

```python main.py --file path/to/file.txt --string "Example"```

If no arguments are provided:

Please provide a string or a file with lines to process.


⸻

📤 Example Output

String: 'Hello, World' => Unique characters: he, wrd


⸻

🧠 Function Breakdown

count_chars_in_string(s: str) -> str
	•	Validates input type and non-emptiness.
	•	Uses collections.Counter to identify characters that appear only once.
	•	Returns the resulting characters in lowercase.
	•	Output is cached using @lru_cache.
	•	Execution time is measured with the @perf_counter_deco.

main()
	•	Parses command-line arguments:
	•	--string: input string to analyze.
	•	--file: path to a file containing strings.
	•	Prioritizes file input if both are passed.
	•	Prints formatted results for each line.
	•	Handles missing arguments gracefully.

⸻

📁 Project Structure

cli_string/
├── __init__.py
├── main.py
├── utils.py
pyproject.toml
README.md


⸻

👨‍💻 Author

Daniel Kravchenko
📧 daniel.kravchenko@protonmail.com

⸻

📄 License

Distributed under the MIT License.

---
