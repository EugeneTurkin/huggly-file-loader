from pytest_django.asserts import assertTemplateUsed


def test_index_returns_200_with_correct_template(django_client):
    resp = django_client.get("")

    assert resp.status_code == 200
    assertTemplateUsed(resp, "index.html")
