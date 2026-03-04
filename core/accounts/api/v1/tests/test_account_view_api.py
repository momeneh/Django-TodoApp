import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta


@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def common_user():
    user = User.objects.create_user(email = 'admin@admin.com',password = '1234!@#$')
    return user

@pytest.mark.django_db
class TestAccountsApi:
   
    def test_accounts_registration_validation_400(self,api_client):        
        response = api_client.post(reverse('accounts:api-v1:registration'),{})
        assert response.status_code == 400 
        
        response = api_client.post(reverse('accounts:api-v1:registration'),{'email':'ddd'})
        assert response.status_code == 400 

        response = api_client.post(reverse('accounts:api-v1:registration'),{'email':'ss@dd.com','password':'1234','password_confirmation':'1234'})
        assert response.status_code == 400 

        response = api_client.post(reverse('accounts:api-v1:registration'),{'email':'ss@dd.com','password':'1234!@#$','password_confirmation':'1234'})
        assert response.status_code == 400 

    def test_accounts_registration_success_200(self,api_client):        
        response = api_client.post(reverse('accounts:api-v1:registration'),{'email':'ss@dd.com','password':'1234!@#$','password_confirmation':'1234!@#$'})
        assert response.status_code == 200 

        user = User.objects.get(email='ss@dd.com')
        assert user != None 
        return user.id
   
    def test_accounts_change_password_anonymous_response_403(self,api_client):
        response = api_client.put(reverse('accounts:api-v1:change-password'),{})
        assert response.status_code == 403 

    def test_accounts_change_password_400(self,api_client,common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.put(reverse('accounts:api-v1:change-password'),{}) #required
        assert response.status_code == 400 

        response = api_client.put(reverse('accounts:api-v1:change-password'),{'old_password':'12','password':'1234!@#$','confirm_password':'1234!@#$'}) #wrong old password
        assert response.status_code == 400 
 
        response = api_client.put(reverse('accounts:api-v1:change-password'),{'old_password':'1234!@#$','password':'12345!@#$','confirm_password':'1234!@#$'}) #not match new passwords
        assert response.status_code == 400 
        
        response = api_client.put(reverse('accounts:api-v1:change-password'),{'old_password':'1234!@#$','password':'123','confirm_password':'123'}) #simple new password
        assert response.status_code == 400 

    def test_accounts_change_password_200(self,api_client,common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.put(reverse('accounts:api-v1:change-password'),{'old_password':'1234!@#$','password':'12345!@#$','confirm_password':'12345!@#$'})
        assert response.status_code == 200 

    def test_accounts_reset_password_400(self,api_client):
        response = api_client.post(reverse('accounts:api-v1:reset-password'),{})
        assert response.status_code == 400 
        
        response = api_client.post(reverse('accounts:api-v1:reset-password'),{'email':'wrong@email.com'})
        assert response.status_code == 400 

    def test_accounts_reset_password_200(self,api_client,common_user):
        response = api_client.post(reverse('accounts:api-v1:reset-password'),{'email':'admin@admin.com'})
        assert response.status_code == 200 

    def test_accounts_reset_password_confirm_400(self,api_client):
        
        response = api_client.get(reverse('accounts:api-v1:reset-password-confirm',kwargs={'token':'ddd'}))
        assert response.status_code == 400 


    def test_accounts_reset_password_confirm_200(self,api_client,common_user):
        token = RefreshToken.for_user(common_user)
        access = token.access_token
        access.set_exp(lifetime=timedelta(minutes=15))

        response = api_client.put(reverse('accounts:api-v1:reset-password-confirm',kwargs={'token':token}),{'password':'1234!@#$','confirm_password':'1234!@#$'})
        assert response.status_code == 200 

    def test_accounts_token_login_400(self,api_client,common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        user.is_verified = True
        user.save()

        response = api_client.post(reverse('accounts:api-v1:login-token'),{}) #required
        assert response.status_code == 400 

        response = api_client.post(reverse('accounts:api-v1:login-token'),{'email':'wrong@email.com','password':'123'}) # wrong email
        assert response.status_code == 400 

        response = api_client.post(reverse('accounts:api-v1:login-token'),{'email':'admin@admin.com','password':'123'}) #wrong password
        assert response.status_code == 400 

    def test_accounts_token_login_200(self,api_client,common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        user.is_verified = True
        user.save()

        response = api_client.post(reverse('accounts:api-v1:login-token'),{'email':'admin@admin.com','password':'1234!@#$'})
        assert response.status_code == 200 

    def test_token_logout_200(self,api_client,common_user):
        self.test_accounts_token_login_200(api_client,common_user)
        response = api_client.post(reverse('accounts:api-v1:logout-token'))
        assert response.status_code == 204

    def test_accounts_jwt_create_400(self,api_client,common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        user.is_verified = True
        user.save()
       
        response = api_client.post(reverse('accounts:api-v1:jwt-create'),{}) #required
        assert response.status_code == 400

        response = api_client.post(reverse('accounts:api-v1:jwt-create'),{'email':'wrong@email.com','password':'123'}) # wrong email
        assert response.status_code == 401

        response = api_client.post(reverse('accounts:api-v1:jwt-create'),{'email':'admin@admin.com','password':'123'}) #wrong password
        assert response.status_code == 401

        user.is_verified = False
        user.save()
        response = api_client.post(reverse('accounts:api-v1:jwt-create'),{'email':'admin@admin.com','password':'1234!@#$'}) #not verified
        assert response.status_code == 400

    def test_accounts_jwt_create_200(self,api_client,common_user):
        user = common_user
        api_client.force_authenticate(user=user)
        user.is_verified = True
        user.save()
        response = api_client.post(reverse('accounts:api-v1:jwt-create'),{'email':'admin@admin.com','password':'1234!@#$'}) 
        assert response.status_code == 200
        assert response.data.get('user_id') == user.id
        return response

    def test_accounts_jwt_refresh_401(self,api_client):
        response = api_client.post(reverse('accounts:api-v1:jwt-refresh'),{"refresh": "string"}) #wrong refresh token
        assert response.status_code == 401

    def test_accounts_jwt_refresh_200(self,api_client,common_user):
        create = self.test_accounts_jwt_create_200(api_client,common_user)
        refresh = create.data.get('refresh')
        response = api_client.post(reverse('accounts:api-v1:jwt-refresh'),{"refresh": refresh}) 
        assert response.status_code == 200

    def test_accounts_jwt_verify_401(self,api_client):
        response = api_client.post(reverse('accounts:api-v1:jwt-verify'),{"token": "string"}) #wrong  token
        assert response.status_code == 401

    def test_accounts_jwt_verify_200(self,api_client,common_user):
        create = self.test_accounts_jwt_create_200(api_client,common_user)
        token = create.data.get('access')
        response = api_client.post(reverse('accounts:api-v1:jwt-verify'),{"token": token}) 
        assert response.status_code == 200
