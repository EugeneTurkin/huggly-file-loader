from pytest_django.asserts import assertTemplateUsed


def test_upload_view_returns_200_with_correct_template_used(django_client):
    resp = django_client.get("/upload/")

    assert resp.status_code == 200
    assertTemplateUsed(resp, "autoloader/upload.html")
