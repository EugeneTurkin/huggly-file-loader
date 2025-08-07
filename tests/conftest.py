from __future__ import annotations

import pytest
from django.test import Client


@pytest.fixture
def django_client():
    c = Client()
    return c
