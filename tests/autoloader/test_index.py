from django.test import Client
from pytest_django.asserts import assertTemplateUsed


def test_index_returns_200_with_correct_template():
    c = Client()
    r = c.get("/loader/")

    assert r.status_code == 200
    assertTemplateUsed(r, "autoloader/index.html")
