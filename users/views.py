import jwt

from datetime import datetime, timedelta

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from core.utils   import KakaoAPI
from users.models import User

class KakaoLoginView(View):
   def get(self, request):
        try:
            auth_code      = request.GET.get('code')
            kakao_user     = KakaoAPI(auth_code, settings.REDIRECT_URI, settings.KAKAO_API_KEY).get_user()
            kakao_id       = kakao_user['id']
            email          = kakao_user['kakao_account']['email']
            name           = kakao_user['kakao_account']['profile']['nickname']

            user, created  = User.objects.get_or_create(
                kakao    = kakao_id,
                email    = email,
                nickname = name
            )
            status_code    = 201 if created else 200
            access_token   = jwt.encode(
                {
                'user_id' : user.id,
                'exp'     : datetime.utcnow() + timedelta(days=1)
                },
                settings.SECRET_KEY,
                settings.ALGORITHM
            )
            return JsonResponse({'message' : "SUCCESS", 'access_token' : access_token}, status = status_code)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)