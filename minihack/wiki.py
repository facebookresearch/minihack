# Copyright (c) Facebook, Inc. and its affiliates.

import json
import os
import re
from collections import defaultdict
from functools import lru_cache
from typing import List
from urllib.parse import unquote

import pkg_resources

try:
    import inflect
    import stanza

    PREPROCESSING_ALLOWED = True
    import_error = None
except ImportError as error:  # noqa
    PREPROCESSING_ALLOWED = False
    import_error = error

DATA_DIR_PATH = pkg_resources.resource_filename("nle", "minihack/dat")

EXCEPTIONS = (
    "floor of a room",
    "agent",
    "staircase up",
)


class TextProcessor:
    """Base class for modeling relations between an object and subject."""

    def __init__(self):
        # Will only do it the first time
        stanza.download("en")
        self.nlp = stanza.Pipeline(lang="en", processors="tokenize,mwt,pos")
        self.inflect = inflect.engine()

    @lru_cache(maxsize=None)
    def preprocess(self, input_str: str) -> str:
        # Removes the brackets and non-letter charachters
        text = re.sub(r"\([^)]*\)", "", input_str)
        pattern = re.compile(r"[^a-zA-Z]+")
        text = pattern.sub(" ", text)
        # Remove trailing whitespaces
        text = re.sub(r"\w[ ]{2,}\w", " ", text)
        return text.strip()

    @lru_cache(maxsize=None)
    def process(self, input_str: str) -> str:
        input_str = self.preprocess(input_str)

        # First find nouns in phrase
        result = self.nlp(input_str)
        nouns = [
            word.text
            for sent in result.sentences
            for word in sent.words
            if word.upos in {"NOUN", "PROPN"}
        ]
        if not nouns:
            return input_str
        # Pick last noun in input
        noun = nouns[-1]

        # Singularise the noun - returns False if the word is alread singular
        singular = self.inflect.singular_noun(noun.lower())
        if not singular:
            return nouns[-1].lower()
        else:
            return singular


class NetHackWiki:
    """A class representing Nethack Wiki Data - pages and links between them.

    Args:
        raw_wiki_file_name (str):
            The path to the raw file of NetHack wiki. The raw file can be
            downloaded using the `get_nhwiki_data.sh` script located in
            `minihack/scripts`.
        processed_wiki_file_name (str):
            The path to the processed file of NetHack wiki. The processing
            is performed in the `__init__` function of this classed.
        save_processed_json (bool):
            Whether to save the processed json file of the wiki. Only
            considered when a raw wiki file is passed. Defaults to True.
        ignore_inpage_anchors (bool):
            Whether to ingnore in-page anchors. Defaults to True.
        preprocess_input (bool):
            Whether to perform a preprocessing on wiki data. Defaults to True.
        exceptions (Tuple[str] or None):
            Name of entities in screen descriptions that are ingored. If None,
            there are no exceptions. Defaults to None.
    """

    def __init__(
        self,
        raw_wiki_file_name: str,
        processed_wiki_file_name: str,
        save_processed_json: bool = True,
        ignore_inpage_anchors: bool = True,
        preprocess_input: bool = True,
        exceptions: tuple = None,
    ) -> None:
        if os.path.isfile(processed_wiki_file_name):
            with open(processed_wiki_file_name, "r") as json_file:
                self.wiki = json.load(json_file)
        elif os.path.isfile(raw_wiki_file_name):
            raw_json = load_json(raw_wiki_file_name)
            self.wiki = process_json(
                raw_json, ignore_inpage_anchors=ignore_inpage_anchors
            )
            if save_processed_json:
                with open(processed_wiki_file_name, "w+") as json_file:
                    json.dump(self.wiki, json_file)
        else:
            raise ValueError(
                """One of `raw_wiki_file_name` or `processed_wiki_file_name`
                must be supplied as argument and be a file. Try using
                `nle/minihack/scripts/get_nhwiki_data.sh` to download the
                data."""
            )

        self.exceptions = exceptions if exceptions is not None else EXCEPTIONS
        self.preprocess_input = preprocess_input
        if preprocess_input:
            if PREPROCESSING_ALLOWED:
                self.text_processor = TextProcessor()
            else:
                print(
                    "To perform text preprocessing, `inflect` and `stanza`"
                    f"must be installed. See {import_error} for more information"
                )
                self.preprocess_input = False

    def get_page_text(self, page: str) -> str:
        """Get the text of a page.

        Args:
            page (str): The page name.
        Returns:
            str: The text of the page.
        """
        if page in self.exceptions:
            return ""
        if self.preprocess_input:
            page = self.text_processor.process(page)
        return self.wiki.get(page, {}).get("text", "")

    def get_page_data(self, page: str) -> dict:
        """Get the data of a page.

        Args:
            page (str): The page name.
        Returns:
            dict: The page data as a dict.
        """
        if page in self.exceptions:
            return {}
        if self.preprocess_input:
            page = self.text_processor.process(input)
        return self.wiki.get(page, {})


def load_json(file_name: str) -> list:
    """Load a file containing a json object per line into a list of dicts."""
    with open(file_name, "r") as json_file:
        input_json = []
        for line in json_file:
            input_json.append(json.loads(line))
    return input_json


def process_json(wiki_json: List[dict], ignore_inpage_anchors) -> dict:
    """Process a list of json pages of the wiki into one dict of all pages."""
    result: dict = {}
    redirects = {}
    result["_global_counts"] = defaultdict(int)

    def href_normalise(x: str):
        result = unquote(x.lower())
        if ignore_inpage_anchors:
            result = result.split("#")[0]
        return result.replace("_", " ")

    for page in wiki_json:
        relevant_page_info = dict(
            title=page["wikipedia_title"].lower(),
            length=len("".join(page["text"])),
            categories=page["categories"].split(","),
            raw_text="".join(page["text"]),
            text=clean_page_text(page["page_data"]),
        )
        # noqa: E731
        relevant_page_info["anchors"] = [
            dict(
                text=anchor["text"].lower(),
                page=href_normalise(anchor.get("title", anchor.get("href"))),
                start=anchor["start"],
            )
            for anchor in page["anchors"]
        ]
        redirect_anchors = [
            anchor
            for anchor in page["anchors"]
            if anchor.get("title")
            and href_normalise(anchor["href"])
            != href_normalise(anchor["title"])
        ]
        redirects.update(
            {
                href_normalise(anchor["href"]): href_normalise(anchor["title"])
                for anchor in redirect_anchors
            }
        )
        unique_anchors: dict = defaultdict(int)
        for anchor in relevant_page_info["anchors"]:
            unique_anchors[anchor["page"]] += 1
            result["_global_counts"][anchor["page"]] += 1
        relevant_page_info["unique_anchors"] = dict(unique_anchors)
        result[relevant_page_info["title"]] = relevant_page_info
    for alias, page in redirects.items():
        result[alias] = result[page]
    return result


def clean_page_text(text: List[str]) -> str:
    """Clean Markdown text to make it more passable into an NLP model.

    This is currently very basic, and more advanced parsing could be employed
    if necessary."""

    return re.sub(r"[^a-zA-Z0-9_\s\.]", "", ",".join(text))
