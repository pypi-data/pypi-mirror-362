# Keywordanalyz

This script analyzes language and keywords in a given text.

## How to use
After you cloned the repository and installed the needed packages with poetry (using `poetry install`), you can use the script like the following:
```python
import keywordanalyz
kw = keywordanalyz.TextAnalyser(maximum_keywords=10)
# You can also specify the length of the keywords using max_n_gram_size (defaults to 3)
text = "Global warming is a significant issue that has been a concern for many years."
print(kw.analyse(text))
# Output: {'language': 'en', 'keywords': [('Global warming', 0.015380821171891606), ('significant issue', 0.02570861714399338), ('Global', 0.09568045026443411), ('years', 0.09568045026443411), ('warming', 0.15831692877998726), ('significant', 0.15831692877998726), ('issue', 0.15831692877998726), ('concern', 0.15831692877998726)]}
# You can also set the language of the text:
print(kw.analyse(text, language="en"))
# Output is the same as before
```
