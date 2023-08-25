# Sentiment Analysis for Turkish Book Comments

This project aims to analyze the sentiment of book comments written in Turkish, collected from [idefix.com](https://www.idefix.com/). The sentiment analysis considers the complexity of the Turkish language structure, including word roots, to provide accurate results.

## Project Overview

The primary goal of this project is to perform sentiment analysis on Turkish book comments. The challenge lies in the Turkish language's intricacies where a word's positive/negative meaning can change based on its root. For instance, "beğenmedim" has a negative meaning, while the root "beğenme" has a positive meaning. Therefore, the sentiment analysis considers both the rooted and non-rooted versions of the comments.

The project involves the following steps:

- **Data Collection**: The script collects book comments from multiple pages on [idefix.com](https://www.idefix.com/). Each comment is associated with the respective book.

- **Preprocessing**: Comments undergo preprocessing, including removing special characters, numbers, emojis, and stopwords. Words in comments are rooted using the TurkishStemmer library to account for variations.

- **Sentiment Analysis**: The sentiment of comments is analyzed using a BERT-based Turkish-supporting sentiment analysis model from the Transformers library. Both original and rooted comments are scored.

- **Results Storage**: Sentiment analysis results are saved in an Excel file named `Idefix_Comments.xlsx`. Columns include Book Name, Original Comment, Cleaned Comment, Sentiment Score (original), Rooted Comment, and Sentiment Score (rooted).

## Used Libraries

The project relies on the following Python libraries:

- [Transformers](https://huggingface.co/transformers): A state-of-the-art natural language processing library that provides easy-to-use interfaces for various pre-trained language models, including BERT.

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): A library used for web scraping and extracting data from HTML and XML files.

- [Pandas](https://pandas.pydata.org/): A data manipulation and analysis library, used here to create dataframes and store the sentiment analysis results.

- [Requests](https://docs.python-requests.org/en/latest/): A library for making HTTP requests to web servers.

- [NLTK](https://www.nltk.org/): The Natural Language Toolkit, used for various natural language processing tasks such as tokenization and stopwords removal.

- [TurkishStemmer](https://pypi.org/project/TurkishStemmer/): A Turkish stemming library used to find the roots of words in Turkish text.

