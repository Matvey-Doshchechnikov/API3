from dotenv import load_dotenv
load_dotenv()

import os

import requests

import argparse

def shorten_link(token, url):
    api_url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    request_body = {
        "long_url": url,
    }

    response = requests.post(api_url, headers=headers, json=request_body)
    response.raise_for_status()

    return response.json()['id']


def count_clicks(token, link):
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    headers = {
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    return response.json()['total_clicks']


def is_bitlink(url, token):
    headers = {
        'Authorization': f'Bearer {token}',
    }

    request_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url}'
    response = requests.get(request_url, headers=headers)

    return response.ok


def main():
    token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(
        description='Программа при вводе обычной ссылки делает битлинк, при вводе битлинка выводит количество кликов'
    )
    parser.add_argument('link', help='Ваша ссылка')
    args = parser.parse_args()
    url = args.link

    if is_bitlink(url, token):
        try:
            click_count = count_clicks(token, url)
            print('Количество кликов:', click_count)
        except requests.exceptions.HTTPError as err:
            print(err)
            print('Не удалось получить количество кликов')
    else:
        try:
            bitlink = shorten_link(token, url)
            print('Битлинк:', bitlink)
        except requests.exceptions.HTTPError as err:
            print(err)
            print('Не удалось создать битлинк')


if __name__ == "__main__":
    main()