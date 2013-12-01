# -*- coding: utf-8 -*-
#!/usr/bin/python


class Traffic:

    """Wikipedia article statistics."""

    def __init__(self, title, site):
        self.site = site
        self.title = title

    def _make_url(self, year, month):
        """Make the URL to the JSON output of stats.grok.se service."""
        return "http://stats.grok.se/json/{0:s}/{1:d}{2:02d}/{3:s}".format(self.site, year, month, self.title)
