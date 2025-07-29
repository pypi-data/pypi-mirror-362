"""{{ project_description }}"""

__version__ = "0.1.0"
{% if author_name %}__author__ = "{{ author_name }}"{% endif %}
{% if author_email %}__email__ = "{{ author_email }}"{% endif %}

from {{ package_name }}.main import app

__all__ = ["app"]

