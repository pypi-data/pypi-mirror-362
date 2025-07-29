# HIdP templates for Wagtail

## Overview

This package contains Wagtail-styled templates for HIdP.

## Installation

1. Install the package using pip:

```bash
pip install django-hidp-wagtail
```

2. Add the package to your `INSTALLED_APPS` in your Django settings:

```python
INSTALLED_APPS = [
    ...
    "hidp_wagtail",  # Should be above "hidp" for templates to work
]
```

3. Set the correct settings for your project:

```python
WAGTAILADMIN_LOGIN_URL = 'hidp_accounts:login'
```

4. Add the provided `account_management_links` context_processor to your settings.py:

```python
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                "hidp_wagtail.context_processors.account_management_links",
            ],
        },
    },
]
```
