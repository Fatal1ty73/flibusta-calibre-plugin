# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__ = 'GPL 3'
__copyright__ = '2022, Fatal1ty73 https://github.com/Fatal1ty73'
__docformat__ = 'restructuredtext en'

from calibre.customize import StoreBase

class FlibustaStore(StoreBase):
    name = 'Флибуста'
    description = _('Книжное братство')
    actual_plugin = 'calibre_plugins.store_flibusta.flibusta:FlibustaStore'
    author = 'Fatal1ty73'

    drm_free_only = True
    headquarters = 'RU'
    formats = ['EPUB', 'TXT', 'RTF', 'HTML', 'FB2', 'PDF', 'MOBI']
    affiliate = False
