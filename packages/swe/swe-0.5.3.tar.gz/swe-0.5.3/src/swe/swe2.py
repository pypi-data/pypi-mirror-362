#!/usr/bin/env python3

# import asyncio
import os
import argparse
import xml.etree.ElementTree as ET
import html
import tempfile
from pathlib import Path
from rich.jupyter import display
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, DataTable, Markdown
from textual.suggester import SuggestFromList
from textual.binding import Binding

from swe.sounds import play_word

# async def add_row_async(table, word):
#     table.add_row(*word)


visible_word = ""

xml_file = os.path.join(
    Path.home(), ".local", "share", "swe", "folkets_sv_en_public.xml"
)
last_word_file = os.path.join(tempfile.gettempdir(), "swe-last-word.txt")

if not os.path.exists(xml_file):
    print(
        "Before using swe, you need to download the latest dictionary file.\n\nDownload it from https://folkets-lexikon.csc.kth.se/folkets/folkets_sv_en_public.xml \nThe file is expected at",
        xml_file,
    )
    exit(1)


def get_answer(search_word) -> str:
    answer = ""
    for word in root.findall(".//word[@value]"):
        word_value = word.attrib["value"]
        inflections = word.findall("./paradigm/inflection[@value]")

        if word_value == search_word or any(
            inflection.attrib["value"] == search_word for inflection in inflections
        ):
            comment = word.get("comment", "")
            answer += "## " + word_value

            if inflections:
                answer += (
                    "\n"
                    + (
                        ", ".join(
                            inflection.attrib["value"] for inflection in inflections
                        )
                    )
                    + "\n"
                )

            translations = word.findall("./translation[@value]")
            if translations:
                answer += "\n\n**"

                answer += ", ".join(
                    (
                        f"{translation.attrib["value"]}</span> ({translation.attrib["comment"]})"
                        if translation.get("comment", "")
                        else "" + translation.attrib["value"] + ""
                    )
                    for translation in translations
                )
                answer += "**"
            if comment:
                answer += f"\n\n*{comment}*"
            synonyms = word.findall("./synonym[@value]")
            if synonyms:
                answer += "\n\n### Synonyms\n"
                answer += ", ".join(synonym.attrib["value"] for synonym in synonyms)
                answer += ""

            examples = word.findall(".//example[@value]")
            if examples:
                answer += "\n\n### Examples"
                for example in examples:
                    example_translation = example.find(".//translation[@value]")
                    if example_translation is not None:
                        answer += f"\n- {example.attrib["value"]}: *{example_translation.attrib["value"]}*"
                answer += ""

            idioms = word.findall("./idiom[@value]")
            if idioms:
                answer += "\n\n ### Idioms"
                for idiom in idioms:
                    idiom_translation = idiom.find("./translation[@value]")
                    if idiom_translation is not None:
                        answer += f"\n- {idiom.attrib["value"]}: *{idiom_translation.attrib["value"]}*"
                answer += ""

            return answer

    return "Word not found"


def search_words(xml_file, search_string):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    result = [
        word.attrib["value"]
        for word in root.findall(".//word[@value]")
        if search_string in word.attrib["value"]
    ]
    return result


ROWS = [
    ("⭐", "Svenska", "Engelska"),
]

ALL_WORDS = []

tree = ET.parse(xml_file)
root = tree.getroot()
for word in root.findall(".//word[@value]"):
    entry = [""]
    entry.append(word.attrib["value"])
    entry.append(", ".join([t.attrib["value"] for t in word.findall("./translation")]))
    entry.append(
        " ".join(
            [t.attrib["value"] for t in word.findall("./paradigm/inflection[@value]")]
        )
    )
    ALL_WORDS.append(entry)


ROWS = ROWS + list(map(lambda x: [x[0], x[1], x[2]], ALL_WORDS))


class SearchInput(Input):
    BINDINGS = [
        ("down", "unfocus", "Unfocus"),
    ]

    def action_unfocus(self) -> None:
        if self.has_parent:
            table = self.parent.query_one(DataTable)
            if table.display:
                table.focus()


class WordViewer(Markdown):
    BINDINGS = [
        ("p", "play", "Play"),
    ]

    def action_play(self) -> None:
        play_word(visible_word)


class SvenskaApp(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "style.tcss"

    BINDINGS = [
        ("ctrl+d", "toggle_dark", "Toggle dark mode"),
        Binding("ctrl+q", "quit", "Quit", priority=True),
        Binding("escape", "clear_search", "Clear search", priority=True),
        ("p", "play", "Play"),
    ]

    def action_play(self) -> None:
        play_word(visible_word)

    TITLE = "swe"

    def action_clear_search(self) -> None:
        table = self.query_one(DataTable)
        viewer = self.query_one(WordViewer)
        viewer.display = False
        table.display = True

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield SearchInput()
        yield DataTable(cursor_type="row", classes="box")
        yield WordViewer()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        viewer = self.query_one(WordViewer)
        viewer.display = False
        for col in ROWS[0]:
            table.add_column(col, key=col)
        table.add_rows(ROWS[1:])

    @on(Input.Changed)
    def filter_results(self, event: Input.Changed) -> None:
        table = self.query_one(DataTable)
        viewer = self.query_one(WordViewer)
        table.display = True
        viewer.display = False
        table.clear()
        rows = [
            [word[0], word[1], word[2]]
            for word in ALL_WORDS
            if event.value in " ".join(word)
        ]
        # for row in rows:
        #     asyncio.create_task(add_row_async(table, row))
        table.add_rows(rows[:500])

        table.sort("Svenska", key=lambda svenska: len(svenska))

    @on(DataTable.RowSelected)
    def select_word(self, event: DataTable.RowSelected) -> None:
        global visible_word
        table = self.query_one(DataTable)
        row_key = event.row_key
        row = table.get_row(row_key)
        word = row[1]
        table.display = False
        viewer = self.query_one(WordViewer)
        viewer.update(get_answer(word))
        visible_word = word
        viewer.display = True
        viewer.focus()

    @on(DataTable.RowHighlighted)
    def select_word(self, event: DataTable.RowHighlighted) -> None:
        global visible_word
        table = self.query_one(DataTable)
        row_key = event.row_key
        row = table.get_row(row_key)
        visible_word = row[1]


if __name__ == "__main__":
    app = SvenskaApp()
    app.run()

speech_tags = {
    "CC": "Coordinating conjunction",
    "CD": "Cardinal number",
    "DT": "Determiner",
    "EX": "Existential there",
    "FW": "Foreign word",
    "IN": "Preposition or subordinating conjunction",
    "JJ": "Adjective",
    "JJR": "Adjective, comparative",
    "JJS": "Adjective, superlative",
    "LS": "List item marker",
    "MD": "Modal",
    "NN": "Noun, singular or mass",
    "NNS": "Noun, plural",
    "NNP": "Proper noun, singular",
    "NNPS": "Proper noun, plural",
    "PDT": "Predeterminer",
    "POS": "Possessive ending",
    "PRP": "Personal pronoun",
    "PRP": "Possessive pronoun",
    "RB": "Adverb",
    "RBR": "Adverb, comparative",
    "RBS": "Adverb, superlative",
    "RP": "Particle",
    "SYM": "Symbol",
    "TO": "to",
    "UH": "Interjection",
    "VB": "Verb, base form",
    "VBD": "Verb, past tense",
    "VBG": "Verb, gerund or present participle",
    "VBN": "Verb, past participle",
    "VBP": "Verb, non-3rd person singular present",
    "VBZ": "Verb, 3rd person singular present",
    "WDT": "Wh-determiner",
    "WP": "Wh-pronoun",
    "WP": "Possessive wh-pronoun",
    "WRB": "Wh-adverb",
}


def print_header(text):
    print(f"\n### {text}")


def print_translations(xml_file, search_word):
    found_word = False
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for word in root.findall(".//word[@value]"):
        word_value = word.attrib["value"]
        inflections = word.findall("./paradigm/inflection[@value]")
        if word_value == search_word or any(
            inflection.attrib["value"] == search_word for inflection in inflections
        ):
            found_word = True
            comment = word.get("comment", "")
            print(f"\033[58;5;158m\033[4:2m\033[1m{word_value}\033[0m", end="")
            if "class" in word.attrib:
                print(f" ({word.attrib['class']})", end="")

            if comment:
                print(f" ({html.unescape(comment)})")
            else:
                print()
            if inflections:
                print(
                    ", ".join(inflection.attrib["value"] for inflection in inflections)
                )
            translations = word.findall("./translation[@value]")
            if translations:
                print_header("Translations")
                for translation in translations:
                    comment = translation.get("comment", "")
                    print(
                        f'-> \033[1m{html.unescape(translation.attrib["value"])}\033[0m',
                        end="",
                    )
                    if comment:
                        print(f" ({html.unescape(comment)})")
                    else:
                        print()

            synonyms = word.findall("./synonym[@value]")
            if synonyms:
                print_header("Synonyms")
                for synonym in synonyms:
                    level = synonym.get("level", "")
                    print(f'- {html.unescape(synonym.attrib["value"])}', end="")
                    if level:
                        print(f" ({html.unescape(level)})")
                    else:
                        print()

            examples = word.findall(".//example[@value]")
            if examples:
                print_header("Examples")
                for example in examples:
                    example_translation = example.find(".//translation[@value]")
                    if example_translation is not None:
                        print(
                            f'- {html.unescape(example.attrib["value"])}: {html.unescape(example_translation.attrib["value"])}'
                        )

            related = word.findall("./related[@value]")
            if related:
                print_header("Related")
                for rel in related:
                    rel_type = rel.get("type", "")
                    rel_translation = rel.find("./translation[@value]")
                    if rel_translation is not None:
                        print(
                            f'- {html.unescape(rel.attrib["value"])} ({html.unescape(rel_type)}): {html.unescape(rel_translation.attrib["value"])}'
                        )

            idioms = word.findall("./idiom[@value]")
            if idioms:
                print_header("Idioms")
                for idiom in idioms:
                    idiom_translation = idiom.find("./translation[@value]")
                    if idiom_translation is not None:
                        print(
                            f'- {html.unescape(idiom.attrib["value"])}: {html.unescape(idiom_translation.attrib["value"])}'
                        )
            print("")

    if not found_word:
        print(f'Word "{search_word}" not found in the XML file.')


def main():
    parser = argparse.ArgumentParser(
        description="Search XML file for words containing a given string."
    )
    parser.add_argument(
        "word", nargs="?", default="", help="Word to get definition for"
    )
    parser.add_argument(
        "-s",
        "--search",
        dest="search_string",
        required=False,
        help="Search words in the dictionary",
    )

    parser.add_argument(
        "-p",
        "--play",
        dest="play_word",
        required=False,
        help="Play a word",
    )
    args = parser.parse_args()

    last_searched_word = False
    if os.path.exists(last_word_file):
        with open(last_word_file, "r") as f:
            last_searched_word = f.read().strip()

    if args.search_string:
        result = search_words(xml_file, args.search_string)
        print("\n".join(result))
    elif args.play_word:
        play_word(args.play_word)
    elif args.word:
        if args.word != last_searched_word:
            with open(last_word_file, "w") as f:
                f.write(args.word)
            print_translations(xml_file, args.word)
        else:
            play_word(last_searched_word)
    else:
        print(
            "swe\n\nUsage: 'swe ord' OR 'swe -s ord'\nAfter printing a definition, rerun 'swe' to hear it"
        )


# asyncio.run(main())
if __name__ == "__main__":
    main()
