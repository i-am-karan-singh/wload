import os
import re
import urllib

import click
import multiprocess
import requests
from tqdm import tqdm

locale_list = ['ar-XA', 'bg-BG', 'cs-CZ', 'da-DK', 'de-AT', 'de-CH', 'de-DE', 'el-GR', 'en-AU', 'en-CA', 'en-GB',
               'en-ID', 'en-IE', 'en-IN', 'en-MY', 'en-NZ', 'en-PH', 'en-SG', 'en-US', 'en-XA', 'en-ZA', 'es-AR',
               'es-CL', 'es-ES', 'es-MX', 'es-US', 'es-XL', 'et-EE', 'fi-FI', 'fr-BE', 'fr-CA', 'fr-CH', 'fr-FR',
               'he-IL', 'hr-HR', 'hu-HU', 'it-IT', 'ja-JP', 'ko-KR', 'lt-LT', 'lv-LV', 'nb-NO', 'nl-BE', 'nl-NL',
               'pl-PL', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 'sk-SK', 'sl-SL', 'sv-SE', 'th-TH', 'tr-TR', 'uk-UA',
               'zh-CN', 'zh-HK', 'zh-TW', 'all']
resolution_list = ['1024x768', '1280x720', '1366x768', '1920x1080', '1920x1200', 'UHD']
url_base = "https://www.bing.com/HPImageArchive.aspx?format=js&idx={0}&n={1}&mkt={2}"
prefix = "https://www.bing.com/"
regex_base = r"OHR.([a-zA-Z0-9]*)_"


def batchload(resolution, locale, number, delay, path, threads):
    json_result = requests.get(url_base.format(delay, number, locale)).json()
    url_name_list = map(
        lambda x: (prefix + x['url'].replace('1920x1080', resolution),
                   os.path.join(path, re.search(regex_base, x['url']).group(1) + '.jpg')),
        json_result['images'])
    url_name_list = filter(lambda x: not os.path.exists(x[1]), url_name_list)
    multiprocess.Pool(threads).map(lambda x: urllib.request.urlretrieve(x[0], x[1]), url_name_list)


@click.command()
@click.option('-r', '--resolution', default='UHD', type=click.Choice(resolution_list))
@click.option('-l', '--locale', default='all', type=click.Choice(locale_list))
@click.option('-n', '--number', default=15, type=click.IntRange(0, 15, clamp=True))
@click.option('-d', '--delay', default=0, type=click.IntRange(0, 7, clamp=True))
@click.option('-p', '--path', default='/home/karan/Pictures/Wallpapers/')
@click.option('-t', '--threads', default=1, type=click.IntRange(1, 8, clamp=True))
def wload(resolution, locale, number, delay, path, threads):
    locales = locale_list[:-1] if locale == 'all' else [locale]
    for l in tqdm(range(len(locales))):
        # Bing does not furnish more than 8 images at once, and more than 15 in total.
        for i in range(delay, delay + number, 8):
            batchload(resolution, locales[l], min(8, number - delay), i, path, threads)


if __name__ == '__main__':
    wload()
