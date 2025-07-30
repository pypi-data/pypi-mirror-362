# -*- coding: utf-8 -*-
import logging
import requests
import tempfile

logger = logging.getLogger("lolicon_api")

def tags_transformer(tags: list[str|list]) -> list[str]:
    """Transform a list of tags into a string.
    For example:
        1. tags_transformer([
            "Tag1|Tag2",
            "Tag3|Tag4"
        ]) -> ['tag1|tag2', 'tag3|tag4']

        2. tags_transformer([
            ['Tag1', 'Tag2'], ['Tag3', 'Tag4']
        ]) -> ['tag1|tag2', 'tag3|tag4']

        3. tags_transformer([
            ['Tag1'], ['Tag2'], ['Tag3'], ['Tag4']
        ]) -> ['tag1', 'tag2', 'tag3', 'tag4']
    :param tags: A list of tags.
    :return: A list of tag strings.
    """
    if not tags:
        return []
    
    result = []
    for tag in tags:
        if isinstance(tag, str):
            # 如果是字符串，直接转小写
            result.append(tag.lower())
        elif isinstance(tag, list):
            # 如果是列表，将列表内的元素用"|"连接，然后转小写
            tag_str = "|".join(str(t).lower() for t in tag)
            result.append(tag_str)
    
    return result

def fetch(tags: list = None, **params) -> dict | None:
    """Fetch data from the lolicon API.
    https://docs.api.lolicon.app/#/setu?id=%e8%af%b7%e6%b1%82

    :param tags:
    :param params:
    :return:
    """
    url = "https://api.lolicon.app/setu/v2"

    if tags:
        params['tag'] = tags_transformer(tags)
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return response.raise_for_status()

def download_image(url: str, save_path: str = tempfile.mkdtemp()) -> None:
    """Download an image from a given URL and save it to a specified path, if not provided, the system temporary directory will be used.

    :param url: The URL of the image to download.
    :param save_path: The local path where the image will be saved.
    """
    logger.debug(f"Downloading image from {url} to {save_path}")

    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
    else:
        response.raise_for_status()
