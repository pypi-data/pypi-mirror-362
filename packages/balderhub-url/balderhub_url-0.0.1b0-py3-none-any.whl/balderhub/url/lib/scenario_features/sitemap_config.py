from __future__ import annotations

from typing import List

import balder
from balderhub.url.lib.utils import Url


class SitemapConfig(balder.Feature):
    """
    Basic configuration feature for handling multiple :class:`Url` objects for a specific system.
    """

    #: prefix that is used within this feature for all :class:`Url` objects.
    url_prefix = 'url_'

    def get_all_urls(self) -> List[Url]:
        """
        Method that returns all :class:Url objects within this configuration feature. It looks for all defined
        attributes within this feature that starts with the defined :meth:`SitemapConfig.url_prefix`.`

        :return: returns a list with all defined :class:`Url` objects
        """
        all_urls = []
        for cur_attr in self.__dict__.keys():
            if cur_attr.startswith(self.url_prefix):
                url = getattr(balder, cur_attr)
                if not isinstance(url, Url):
                    raise TypeError(f'unknown type for url `{url}` - needs to be subclass of `{Url}`')
                all_urls.append(getattr(self, cur_attr))

        if len(all_urls) == 0:
            raise ValueError(f'you need to define at least one url (does the prefix match? - '
                             f'configured prefix is `{self.url_prefix}`)')

        return all_urls
