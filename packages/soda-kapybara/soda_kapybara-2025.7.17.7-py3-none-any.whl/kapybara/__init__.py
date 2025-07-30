"""通用组件以及浏览器库"""

from .form_element import FormElement
from .shared_data import shared_data
from .shortcuts import WebDriver, By, EC, WebDriverWait
from .browserlib.custom_browser import CustomBrowser

ec = EC

__all__ = [
    'FormElement',
    'shared_data',
    'WebDriver',
    'By',
    'EC',
    'ec',
    'WebDriverWait',
    'Keys',
    'CustomBrowser',
]
from selenium.webdriver.common.keys import Keys
