import sys
from bs4 import BeautifulSoup
import requests
import re

from requests.exceptions import MissingSchema, InvalidURL

def is_key_value_pair(tag):
    if not tag.has_attr("class"):
        return False

    if "row" not in tag.get_attribute_list("class"):
        return False

    res = tag.find_all('div', class_='col-xs-12')    
    if len(res) != 2:
        return False

    return True


def get_census(url):
    page = requests.get(url)
    tree = BeautifulSoup(page.content, 'html.parser')

    breadcrumbs = tree.find("ul", "da-breadcrumb").find_all("li")

    census = breadcrumbs[2].get("title")
    district = breadcrumbs[4].get("title")
    residence = breadcrumbs[5].get("title")

    apartment = None
    if len(breadcrumbs) > 6:
        apartment = breadcrumbs[6].get("title")

    attributes = []
    people = []

    data_containers = tree.find("div", attrs={'class': "left-view-column"})
    data_container = data_containers.find('div', attrs={'class': 'row'})

    while data_container is not None:
        if 'hidden-print' in data_container.attrs['class']:
            data_container = data_container.find_next_sibling('div',
                                                              attrs={'class': 'row'})

        agriculture = data_container.div.find('div', id="accordion-agriculure")
        if agriculture:
            data = agriculture.find_all(is_key_value_pair)
            for d in data:
                keyval = d.find_all("div", class_="col-xs-12")
                key, value = keyval
                key = key.text.strip()
                value = value.text.strip()
                if value != '-':
                    attributes.append((key[:-1], value))

        persons = data_container.div.find('div', id="accordion-persons")
        if persons:
            data = persons.find_all('div', attrs={'class': 'data-item'})
            for person in data:
                name_tag = person.find('h4').a

                idx = name_tag.contents[1].text.strip()
                name = name_tag.contents[2].strip()
                personattributes = []

                data_rows = person.find('div',
                                        attrs={'class': 'row'}).find_all('div',
                                                                         attrs={'class': 'row'})
                for row in data_rows:
                    keyval = row.find_all('div')
                    if len(keyval) == 2:
                        key, value = keyval
                        key = key.text.strip()
                        value = value.text.strip()
                        personattributes.append((key[:-1], value))

                people.append((idx, name, personattributes))
        else:
            data_rows = data_container.find_all('div', attrs={'class': 'row'})
            for row in data_rows:
                keyval = row.find_all('div')
                if len(keyval) == 2:
                    key, value = keyval
                    key = key.text.strip()
                    value = value.text.strip()

                    if value != '-':
                        attributes.append((key[:-1], value))

        data_container = data_container.find_next_sibling('div', attrs={'class': 'row'})

    return {
        'census': census,
        'district': district,
        'residence': residence,
        'apartment': apartment,
        'attributes': attributes,
        'people': people,
        'url': url
    }


def census_to_markdown(census,
                       district,
                       residence,
                       apartment,
                       attributes,
                       people,
                       url):
    markdown_lines = []

    markdown_lines.append("{}, {}, {}, {}\n".format(census,
                                                    district,
                                                    residence,
                                                    apartment or ""))

    for attribute in attributes:
        markdown_lines.append("{}: {}".format(attribute[0], attribute[1]))

    markdown_lines.append("\n")

    markdown_lines.append("Beboere:\n")

    people_table = []
    for index, name, attributes in people:
        if len(people_table) == 0:
            header_line = '|      |'
            for attribute in attributes:
                header_line += attribute[0] + '|'

            divider_line = '|' + '--------|' * (len(attributes) + 1)
            people_table.append(header_line)
            people_table.append(divider_line)

        person_line = '|{} {}|'.format(index, name)
        for attribute in attributes:
            person_line += '{}|'.format(attribute[1])
        people_table.append(person_line)

    markdown_lines += people_table
    markdown_lines.append("\n<{}>\n".format(url))

    return "\n".join(markdown_lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: {} <censuspageurl>".format(__file__))

    url = sys.argv[1]
    census_data = get_census(url)
    print(census_to_markdown(**census_data))


if __name__ == '__main__':
    main()
