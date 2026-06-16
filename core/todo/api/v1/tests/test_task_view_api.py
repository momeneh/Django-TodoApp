import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="admin@admin.com", password="1234!@#$", is_verified=True
    )
    return user


@pytest.mark.django_db
class TestTaskApi:
    def test_task_list_anonymous_response_403(self, api_client):
        response = api_client.get(reverse("todo:api-v1:todo-list"))
        assert response.status_code == 403

    def test_task_list_logged_in_response_200(self, api_client, common_user):
        api_client.force_authenticate(user=common_user)
        response = api_client.get(reverse("todo:api-v1:todo-list"))
        assert response.status_code == 200

    def test_task_create_anonymous_response_403(self, api_client):
        response = api_client.post(reverse("todo:api-v1:todo-list"), {})
        assert response.status_code == 403

    def test_task_create_logged_in_response_201(self, api_client, common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        data = {"title": "task1"}
        response = api_client.post(reverse("todo:api-v1:todo-list"), data)
        assert response.status_code == 201
        assert response.data.get("user") == user.id
        assert response.data.get("title") == "task1"

    def test_task_create_logged_in_response_400(self, api_client, common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(reverse("todo:api-v1:todo-list"), {})
        assert response.status_code == 400

    def test_task_detail_anonymous_response_403(self, api_client):
        response = api_client.get(reverse("todo:api-v1:todo-detail", kwargs={"pk": 1}))
        assert response.status_code == 403

    def test_task_detail_logged_in_response_200(self, api_client, common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        data = {"title": "task2"}
        response = api_client.post(reverse("todo:api-v1:todo-list"), data)
        assert response.status_code == 201

        response = api_client.get(
            reverse("todo:api-v1:todo-detail", kwargs={"pk": response.data.get("id")})
        )
        assert response.status_code == 200

    def test_task_detail_not_owner_response_404(self, api_client, common_user):
        """create a task by one user"""
        user = common_user
        api_client.force_authenticate(user=user)
        data = {"title": "task"}
        response = api_client.post(reverse("todo:api-v1:todo-list"), data)
        assert response.status_code == 201
        id = response.data.get("id")
        api_client.logout()

        """view the same task by another user 
            permission testing
        """
        user2 = User.objects.create_user(
            email="admin2@admin.com", password="1234!@#$", is_verified=True
        )
        api_client.force_authenticate(user=user2)
        response = api_client.get(reverse("todo:api-v1:todo-detail", kwargs={"pk": id}))
        assert response.status_code == 404

    def test_task_detail_logged_in_wrong_id_response_404(self, api_client, common_user):
        api_client.force_authenticate(user=common_user)
        response = api_client.get(
            reverse("todo:api-v1:todo-detail", kwargs={"pk": 100000})
        )
        assert response.status_code == 404

    def test_task_update_anonymous_response_403(self, api_client):
        response = api_client.post(
            reverse("todo:api-v1:todo-detail", kwargs={"pk": 1}), {}
        )
        assert response.status_code == 403

    def test_task_update_logged_in_response_200(self, api_client, common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        data = {"title": "task2"}
        response = api_client.post(reverse("todo:api-v1:todo-list"), data)
        assert response.status_code == 201

        data["title"] = "task2--"
        response = api_client.put(
            reverse("todo:api-v1:todo-detail", kwargs={"pk": response.data.get("id")}),
            data,
        )
        assert response.status_code == 200
        assert response.data.get("title") == data["title"]

    def test_task_update_not_owner_response_404(self, api_client, common_user):
        """create a task by one user"""
        user = common_user
        api_client.force_authenticate(user=user)
        data = {"title": "task"}
        response = api_client.post(reverse("todo:api-v1:todo-list"), data)
        assert response.status_code == 201
        id = response.data.get("id")
        api_client.logout()

        """view the same task by another user 
            permission testing
        """
        user2 = User.objects.create_user(
            email="admin2@admin.com", password="1234!@#$", is_verified=True
        )
        api_client.force_authenticate(user=user2)
        data["title"] = "task2--"
        response = api_client.put(
            reverse("todo:api-v1:todo-detail", kwargs={"pk": id}), data
        )
        assert response.status_code == 404

    def test_task_update_logged_in_wrong_id_response_404(self, api_client, common_user):
        api_client.force_authenticate(user=common_user)
        response = api_client.put(
            reverse("todo:api-v1:todo-detail", kwargs={"pk": 100000}), {}
        )
        assert response.status_code == 404

    def test_task_delete_anonymous_response_403(self, api_client):
        response = api_client.delete(
            reverse("todo:api-v1:todo-detail", kwargs={"pk": 1})
        )
        assert response.status_code == 403

    def test_task_delete_logged_in_response_200(self, api_client, common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        data = {"title": "task2"}
        response = api_client.post(reverse("todo:api-v1:todo-list"), data)
        assert response.status_code == 201

        response = api_client.delete(
            reverse("todo:api-v1:todo-detail", kwargs={"pk": response.data.get("id")})
        )
        assert response.status_code == 204

    def test_task_delete_not_owner_response_404(self, api_client, common_user):
        """create a task by one user"""
        user = common_user
        api_client.force_authenticate(user=user)
        data = {"title": "task"}
        response = api_client.post(reverse("todo:api-v1:todo-list"), data)
        assert response.status_code == 201
        id = response.data.get("id")
        api_client.logout()

        """view the same task by another user 
            permission testing
        """
        user2 = User.objects.create_user(
            email="admin2@admin.com", password="1234!@#$", is_verified=True
        )
        api_client.force_authenticate(user=user2)
        response = api_client.delete(
            reverse("todo:api-v1:todo-detail", kwargs={"pk": id})
        )
        assert response.status_code == 404

    def test_task_delete_logged_in_wrong_id_response_404(self, api_client, common_user):
        api_client.force_authenticate(user=common_user)
        response = api_client.delete(
            reverse("todo:api-v1:todo-detail", kwargs={"pk": 100000})
        )
        assert response.status_code == 404
