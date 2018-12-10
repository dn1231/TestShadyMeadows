import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--url', action='store', default='https://automationintesting.online',
        help='The base URL of the website to test'
    )
