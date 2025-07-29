"""
Implementation of the MkDocs Kuma Uptime Badge Plugin.

This plugin converts shorthand placeholders of the form:
{{uptime id=<monitorID> [type=<badgeType>] [hours=<int>] [key=value ...]}}

to full Uptime Kuma badge links:
![<badgeType>](<baseUrl>/api/badge/<monitorID>/<badgePath>[?<qs>])
"""

import re
import urllib.parse
from typing import Any, Dict

from mkdocs.config import config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin


class UptimeBadgePlugin(BasePlugin):
    """
    MkDocs plugin that converts Kuma uptime badge shorthand to full Markdown image links.
    """

    config_scheme = (
        ('base_url', config_options.Type(str, default='https://kuma.intra')),
    )

    def __init__(self):
        self.base_url = 'https://kuma.intra'

    def on_config(self, config: MkDocsConfig) -> Dict[str, Any]:
        """
        Process the configuration.

        Args:
            config: The MkDocs configuration.

        Returns:
            The updated configuration.
        """
        self.base_url = self.config['base_url']
        return config

    def on_page_markdown(self, markdown: str, **kwargs) -> str:
        """
        Process the Markdown content of each page.

        Args:
            markdown: The Markdown content.
            **kwargs: Additional arguments.

        Returns:
            The processed Markdown content.
        """
        if '{{uptime' not in markdown:
            return markdown

        pattern = r"\{\{uptime\s+([^}]+)\}\}"

        def replace_match(match):
            params_str = match.group(1)
            params = self._parse_params(params_str)

            if 'id' not in params:
                return match.group(0)  # Return unchanged if no ID

            monitor_id = params.pop('id')
            badge_type = params.pop('type', 'status')

            # Handle hours parameter for specific badge types
            badge_path = badge_type
            if badge_type in ['ping', 'uptime', 'avg-response', 'response']:
                hours = params.pop('hours', None)
                if hours:
                    badge_path = f"{badge_type}/{hours}"

            # Build query string from remaining parameters
            query_string = urllib.parse.urlencode(params) if params else ""
            url = f"{self.base_url}/api/badge/{monitor_id}/{badge_path}"
            if query_string:
                url = f"{url}?{query_string}"

            return f"![{badge_type}]({url})"

        return re.sub(pattern, replace_match, markdown)

    def _parse_params(self, params_str: str) -> Dict[str, str]:
        """
        Parse the parameters from the shorthand notation.

        Args:
            params_str: The parameter string from the shorthand.

        Returns:
            A dictionary of parameter key-value pairs.
        """
        params = {}
        # Split by spaces, but respect quoted values
        parts = re.findall(r'([^=\s]+)=(?:"([^"]*)"|([^\s]*))', params_str)

        for key, quoted_value, unquoted_value in parts:
            value = quoted_value if quoted_value else unquoted_value
            params[key] = value

        return params
