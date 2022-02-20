import requests

class KakaoAPI:
    def __init__(self, auth_code, REDIRECT_URI, KAKAO_API_KEY):
        self.auth_code      = auth_code
        self.redirect_uri   = REDIRECT_URI
        self.rest_api_key   = KAKAO_API_KEY
        self.grant_type     = "authorization_code"
        self.token_url      = "https://kauth.kakao.com/oauth/token?grant_type={0}&client_id={1}&redirect_uri={2}&code={3}"\
            .format(
                    self.grant_type,
                    self.rest_api_key,
                    self.redirect_uri,
                    self.auth_code
                )
        self.access_token   = self.get_token()
        
    def get_token(self):
        headers        = {'Content-Type' : 'application/x-www-form-urlencoded'}
        response       = requests.post(self.token_url, headers = headers)
        access_token   = response.json()['access_token']
        
        return access_token
    
    def get_user(self):
        headers      = {"Authorization" : f"Bearer {self.access_token}"}
        response     = requests.get("https://kapi.kakao.com/v2/user/me", headers = headers, timeout = 3)

        return response.json()
