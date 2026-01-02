#!/usr/bin/env python3

import argparse
import json
import string
from nltk.stem import PorterStemmer
from logging.config import stopListening


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print("Searching for:", args.query)
            with open("./data/movies.json", "r") as f:
                data = json.load(f)
            movies = data["movies"]
            results = [movie for movie in movies if any(qt in tt for qt in retrieve_tokens(args.query) for tt in retrieve_tokens(movie["title"]))]
            for index in range(0,6):
                print(f"{index + 1}. {results[index]['title']}")
        case _:
            parser.print_help()


def retrieve_tokens(title):
    stemmer = PorterStemmer()
    with open("./data/stopwords.txt", "r") as f:
        data = f.read()
        lines = data.splitlines()
    translation_table = str.maketrans("", "", string.punctuation)
    return [stemmer.stem(token.lower()) for token in title.translate(translation_table).split() if token and token not in lines]

if __name__ == "__main__":
    main()

