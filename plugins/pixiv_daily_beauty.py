#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from pixivpy3 import *

_USERNAME = "zdf0221"
_PASSWORD = "creative"


_REQUESTS_KWARGS = {
  # 'proxies': {
  #   'https': 'http://127.0.0.1:2237',
  # },
  # 'verify': False,       # PAPI use https, an easy way is disable requests SSL verify
}


def get_daily_ranking(aapi):
    json_result = aapi.illust_ranking('day', date='2019-06-21')
    directory = "dl"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # download top10 day rankings to 'dl' dir
    for illust in json_result.illusts[:10]:
        image_url = illust.meta_single_page.get('original_image_url', illust.image_urls.large)
        print("%s: %s" % (illust.title, image_url))
        # a_api.download(image_url)

        url_basename = os.path.basename(image_url)
        extension = os.path.splitext(url_basename)[1]
        name = "illust_id_%d_%s%s" % (illust.id, illust.title, extension)
        aapi.download(image_url, path=directory, name=name)


def proxy_get_tokens():

    aapi = AppPixivAPI(proxies={'https': 'http://127.0.0.1:2237'}, verify=False)
    return aapi.login(_USERNAME, _PASSWORD)


if __name__ == '__main__':

    a_api = AppPixivAPI()

    tokens = proxy_get_tokens()
    a_api.set_auth(tokens.response.access_token)

    a_api.set_api_proxy("http://app-api.pixivlite.com")

    get_daily_ranking(a_api)



