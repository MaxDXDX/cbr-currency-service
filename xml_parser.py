"""A primitive xml/html parser for extracting contents of tags.
It was also possible to use ready to use modules (xml for example), but I have built this one from scratch to decrease
    count of third-party modules.

.. moduleauthor:: Max Dubrovin <mihadxdx@gmail.com>

"""

import re, xml


def tag_attribute(text: str, tag_name: str, attr_name: str):
    """Find first tag and return it attribute value.

    :param text: Xml formatted text
    :param tag_name: Tag name to find
    :param attr_name: Attribute name of searched tag
    :return: Value of extracted attribute
    """
    regex = f'<{tag_name}.*{attr_name}="(.*?)"'
    match = re.search(regex, text)
    if match:
        return match.group(1)
    else:
        return False


def tag_content(text, tag_name, find_all=False):
    """Return content of tag specified its name

    :param text: Xml formatted text
    :param tag_name: Target tag name
    :param find_all: If True it returns list of contents of all founded tags with matched name.
        If False - only content of first founded tag will be returned.
    :return: content list of all founded tags (if find_all=True) or content of first founded tag (if fina_all=False)
    """
    regex = f'<{tag_name}>(.*?)<\/{tag_name}>'
    if find_all:
        tag_contents = [item.rstrip() for item in re.findall(regex, text)]
    else:
        tag_contents = re.search(regex, text).group(1).rstrip()
    return tag_contents


def xml_date(date: str):
    """Convert DD.MM.YYYY date to YYYY-MM-DD format"""
    return f'{date[6:]}-{date[3:5]}-{date[:2]}'
