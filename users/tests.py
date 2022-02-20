import jwt

from datetime      import datetime, timedelta

from django.conf   import settings
from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock

from .models       import *

class KakaoLoginTest(TestCase):
    def setUp(self):
        pass
    @patch('core.utils.requests')
    def test_kakao_login_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):

                return {
                    "id":1,
                    "kakao_account": { 
                        "profile_needs_agreement": False,
                        "profile": {
                            "nickname": "홍길동",
                            "thumbnail_image_url": "http://yyy.kakao.com/.../img_110x110.jpg",
                            "profile_image_url": "http://yyy.kakao.com/dn/.../img_640x640.jpg",
                            "is_default_image": False
                        },
                        "email_needs_agreement":False,
                        "is_email_valid": True,
                        "is_email_verified": True, 
                        "email": "sample@sample.com",
                        "age_range_needs_agreement":False,
                        "age_range":"20~29",
                        "birthday_needs_agreement":False,
                        "birthday":"1130"
                        }
                    }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"Authorization": "access_token"}
        response            = client.get("/users/login", **headers)
        access_token        = jwt.encode({'user_id' : 1,'exp': datetime.utcnow() + timedelta(days=1)}, settings.SECRET_KEY, settings.ALGORITHM)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : "SUCCESS", 'access_token' : access_token})