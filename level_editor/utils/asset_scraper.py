import requests
from bs4 import BeautifulSoup
from lxml import etree
import logging
import shutil
from pathlib import Path
import json


class NethackScraper():

    def __init__(self):
        self._log = logging.getLogger('Nethack Scraper')
        logging.basicConfig(level=logging.INFO)

        self._visited_pages = set()
        self._added_items = set()

        self._blacklist_pages = {
            'https://nethackwiki.com/wiki/Quest_artifact',
            'https://nethackwiki.com/wiki/Polypiling',
            'https://nethackwiki.com/wiki/Polypiling#Forbidden_items',
            'https://nethackwiki.com/wiki/Weight',
            'https://nethackwiki.com/wiki/Wish',
        }

    def _download_image(self, img_src, output_location, name):
        filename = Path(output_location).joinpath(f'{name}.png')

        if not filename.exists():
            r = requests.get(img_src, stream=True)
            if r.status_code == 200:
                with open(filename, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

        return str(filename)

    def _remove_whitespace_entries(self, entries):
        return [entry for entry in entries if len(entry.strip()) > 0]

    def scrape_items_class(self, output_location, item_class_page):

        if item_class_page in self._blacklist_pages:
            return []
        elif item_class_page in self._visited_pages:
            return []
        else:
            self._visited_pages.add(item_class_page)

        self._log.info(f'Visiting wiki page: \'{item_class_page}\'.')

        # Load the page
        page = requests.get(item_class_page)
        soup = BeautifulSoup(page.content, "html.parser")

        dom = etree.HTML(str(soup))

        items = []
        # try to get image/info for item class, otherwise try to scrape a data table (swords etc)
        single_item_node = dom.xpath('//div[@class="mw-parser-output"]/div[@class="thumb tright"]//th//img')
        if len(single_item_node) > 0:
            for item_node_image in single_item_node:

                item_node = item_node_image.xpath('../..')[0]

                name = item_node.xpath('../../tr[2]/td/text()')[0].strip()

                if name not in self._added_items:
                    self._added_items.add(name)

                    item_glyph_char = item_node.xpath('./span/text()')
                    item_glyph_color = item_node.xpath('./span/@class')
                    item_glyph_char = item_glyph_char[0] if len(item_glyph_char) > 0 else ''
                    item_glyph_color = item_glyph_color[0] if len(item_glyph_color) > 0 else ''

                    item_glyph = {
                        'character': item_glyph_char,
                        'color': item_glyph_color
                    }

                    ## HACK
                    if name == 'statue of a':
                        name = 'statue'

                    original_image_src = 'https://nethackwiki.com' + item_node.xpath('./a/img/@src')[0]

                    item_data = {
                        'name': name,
                        'wiki_link': item_class_page,
                        'image': self._download_image(original_image_src, output_location, name),
                        'original_image_src': original_image_src,
                        'glyph': item_glyph,
                    }

                    self._log.info(f'Adding item \'{name}\'.')
                    items.append(item_data)
        else:
            item_list_nodes = dom.xpath(
                '//div[not(@class="thumb tright itemclasses")]/table[@class="prettytable"]//tr/td[1]/a')
            for item_list_node in item_list_nodes:
                if len(self._remove_whitespace_entries(item_list_node.xpath('..//text()'))) > 1:
                    self._log.info(f'Skipping ambiguous entry, {"".join(self._remove_whitespace_entries(item_list_node.xpath("..//text()")))}')
                    continue
                item_list_node_page = 'https://nethackwiki.com' + item_list_node.xpath('./@href')[0]
                self._log.info(f'Link from {item_class_page} to {item_list_node_page} found in item description')
                items.extend(self.scrape_items_class(output_location, item_list_node_page))

            item_list_nodes = dom.xpath('//div[@class="mw-parser-output"]/table//tr/td[1]/a')
            for item_list_node in item_list_nodes:
                # Check that this is not just a link hidden in some text
                if len(self._remove_whitespace_entries(item_list_node.xpath('..//text()'))) > 1:
                    self._log.info(f'Skipping ambiguous entry, {"".join(self._remove_whitespace_entries(item_list_node.xpath("..//text()")))}')
                    continue
                item_list_node_page = 'https://nethackwiki.com' + item_list_node.xpath('./@href')[0]
                self._log.info(f'Link from {item_class_page} to {item_list_node_page} found in table')
                items.extend(self.scrape_items_class(output_location, item_list_node_page))

        return items

    def scrape_items(self, output_location):

        Path(output_location).mkdir(parents=True, exist_ok=True)

        # Get the item classes from any of the pages with item classes on it
        initial_class_url = 'https://nethackwiki.com/wiki/Amulet'
        initial_class_name = 'Amulet'

        # Load the page
        page = requests.get(initial_class_url)
        soup = BeautifulSoup(page.content, "html.parser")

        dom = etree.HTML(str(soup))

        # Get a list of classes
        item_classes = []
        class_nodes = dom.xpath('//div[@class="mw-parser-output"]/div[@class="thumb tright itemclasses"]//td')
        for class_node in class_nodes:
            class_name = class_node.xpath('./a/@title')
            glyph_char = class_node.xpath('./a/span/text()')
            glyph_color = class_node.xpath('./a/span/@class')

            class_name = class_name[0] if len(class_name) > 0 else ''
            glyph_char = glyph_char[0] if len(glyph_char) > 0 else ''
            glyph_color = glyph_color[0] if len(glyph_color) > 0 else ''

            if len(class_name) == 0:
                item_class_page = initial_class_url
                class_name = initial_class_name
            else:
                item_class_page = 'https://nethackwiki.com' + class_node.xpath('./a/@href')[0]

            self._log.info(f'Processing item class with name {class_name} and glyph \'{glyph_char}\'...')

            class_glyph = {
                'character': glyph_char,
                'color': glyph_color
            }

            items = self.scrape_items_class(output_location, item_class_page)

            item_class_data = {
                'class': class_name,
                'glyph': class_glyph,
                'objects': items
            }

            item_classes.append(item_class_data)

        filename = Path(output_location).joinpath('../items.json')
        with open(filename, 'w') as f:
            json.dump(item_classes, f)

    def scrape_monsters(self, output_location):
        """
        Scrape the nethack wiki for all monsters and their associated images: https://nethackwiki.com/wiki/Monster

        builds a json file with all the information that can be used in the UI for generating nethack levels.

        this information can be used to build the 'MONSTER' specification in `.des` files i.e: MONSTER:'X',"monst",place
        see here for more information https://nethackwiki.com/wiki/Des-file_format#MONSTER

        monsters.json will look like the following:
        [
            {
                'class': ['ants', 'insects']
                'glyph: {
                    'character': 'a'
                    'color': 'clr-white' # need to convert these from css to actual colors (can probably find a lookup table somewhere
                }
                'objects': [
                    {
                        'name': 'soldier ant',
                        'original_image_src': 'https://nethackwiki.com/mediawiki/images/f/f1/Soldier_ant.png',
                        'image': f'{output_location}/Soldier_ant.png',
                        'glyph: {
                            'character': 'a'
                            'color': 'clr-blue' # need to convert these from css to actual colors (can probably find a lookup table somewhere
                        }

                    }
                ]
        ]
        """

        Path(output_location).mkdir(parents=True, exist_ok=True)

        # Load the page
        URL = "https://nethackwiki.com/wiki/Monster"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        dom = etree.HTML(str(soup))

        # Get a list of classes
        classes = []
        class_nodes = dom.xpath('//div[@class="mw-parser-output"]/ul[1]/li')
        for class_node in class_nodes:
            class_names = class_node.xpath('./a/text()')
            glyph_char = class_node.xpath('./span/text()')
            glyph_color = class_node.xpath('./span/@class')

            glyph_char = glyph_char[0] if len(glyph_char) > 0 else ''
            glyph_color = glyph_color[0] if len(glyph_color) > 0 else ''

            class_glyph = {
                'character': glyph_char,
                'color': glyph_color
            }

            self._log.info(f'Processing monster class with names {class_names} and glyph \'{glyph_char}\'...')

            monsters = []
            monster_nodes = class_node.xpath('./ul/li')
            for monster_node in monster_nodes:
                monster_glyph_char = class_node.xpath('./span/text()')
                monster_glyph_color = class_node.xpath('./span/@class')
                monster_glyph_char = monster_glyph_char[0] if len(monster_glyph_char) > 0 else ''
                monster_glyph_color = monster_glyph_color[0] if len(monster_glyph_color) > 0 else ''

                monster_glyph = {
                    'character': monster_glyph_char,
                    'color': monster_glyph_color
                }

                info_node = monster_node.xpath('./a[2]')[0]

                name = info_node.xpath('./@title')[0]
                wiki_link = info_node.xpath('./@href')[0]

                original_image_src = 'https://nethackwiki.com' + monster_node.xpath('./a/img/@src')[0]

                monster_data = {
                    'name': name,
                    'wiki_link': 'https://nethackwiki.com' + wiki_link,
                    'image': self._download_image(original_image_src, output_location, name),
                    'original_image_src': original_image_src,
                    'glyph': monster_glyph,
                }

                self._log.info(f'Adding monster \'{name}\'.')

                monsters.append(monster_data)

            class_data = {
                'class': class_names,
                'glyph': class_glyph,
                'objects': monsters
            }

            classes.append(class_data)

        filename = Path(output_location).joinpath('../monsters.json')
        with open(filename, 'w') as f:
            json.dump(classes, f)


if __name__ == '__main__':
    scraper = NethackScraper()
    scraper.scrape_monsters('monsters')
    scraper.scrape_items('items')
