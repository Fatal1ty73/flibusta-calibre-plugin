# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__ = 'GPL 3'
__copyright__ = ''
__docformat__ = 'restructuredtext en'

from contextlib import closing

from calibre import (browser, guess_extension)
from calibre.gui2.store.basic_config import BasicStoreConfig
from calibre.gui2.store.opensearch_store import OpenSearchOPDSStore
from calibre.gui2.store.search_result import SearchResult
from calibre.utils.opensearch.description import Description
from calibre.utils.opensearch.query import Query
from lxml import etree


def search_flibusta(url, query, web_url, max_results=10, timeout=60):
    description = Description(url)
    url_template = description.get_best_template()
    if not url_template:
        return
    oquery = Query(url_template)

    # set up initial values
    oquery.searchTerms = query
    oquery.count = max_results
    url = oquery.url()

    counter = max_results
    br = browser()
    with closing(br.open(url, timeout=timeout)) as f:
        doc = etree.fromstring(f.read())
        for data in doc.xpath('//*[local-name() = "entry"]'):
            if counter <= 0:
                break

            counter -= 1

            s = SearchResult()

            s.detail_item = ''.join(data.xpath('./*[local-name() = "id"]/text()')).strip()

            for link in data.xpath('./*[local-name() = "link"]'):
                rel = link.get('rel')
                href = link.get('href')
                type = link.get('type')

                if rel and href and type:
                    if 'http://opds-spec.org/thumbnail' in rel:
                        s.cover_url = web_url + href
                    elif 'http://opds-spec.org/image/thumbnail' in rel:
                        s.cover_url = web_url + href
                    elif 'http://opds-spec.org/acquisition/buy' in rel:
                        s.detail_item = web_url + href
                    elif 'http://opds-spec.org/acquisition/sample' in rel:
                        pass
                    elif 'http://opds-spec.org/acquisition/open-access' in rel:
                        if 'application/fb2+zip' in type:
                            s.downloads['FB2.ZIP'] = web_url + href
                        elif 'application/txt+zip' in type:
                            s.downloads['TXT.ZIP'] = web_url + href
                        elif 'application/html+zip' in type:
                            s.downloads['HTML.ZIP'] = web_url + href
                        elif 'application/x-mobipocket-ebook' in type:
                            s.downloads['MOBI'] = web_url + href
                        elif type:
                            ext = guess_extension(type)
                            ext2 = guess_extension(type.replace("+zip", ""))
                            if ext:
                                ext = ext[1:].upper().strip()
                                s.downloads[ext] = web_url + href
                            elif ext2:
                                ext2 = ext2[1:].upper().strip()
                                s.downloads[ext2+".ZIP"] = web_url + href
            s.formats = ', '.join(s.downloads.keys()).strip()

            s.title = ' '.join(data.xpath('./*[local-name() = "title"]//text()')).strip()
            s.author = ', '.join(data.xpath('./*[local-name() = "author"]//*[local-name() = "name"]//text()')).strip()

            s.price = '$0.00'
            s.drm = SearchResult.DRM_UNLOCKED

            yield s


class FlibustaStore(BasicStoreConfig, OpenSearchOPDSStore):
    open_search_url = 'https://flibusta.is/opds-opensearch.xml'
    web_url = 'https://flibusta.is'

    def search(self, query, max_results=10, timeout=60):
        for r in search_flibusta(self.open_search_url, query, self.web_url, max_results=max_results, timeout=timeout):
            yield r
