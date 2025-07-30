from .wx_api import WXApiBase

import logging
import requests

logger = logging.getLogger()


class WXApiProviderDev(WXApiBase):
    def get_user_info(self, access_token, code):
        """获取访问用户身份 -- 代开发"""
        url = f"{self.base_url}/user/getuserinfo"
        params = {
            "access_token": access_token,
            "code": code
        }
        return self._request('GET', url, params=params)
    
    def get_corp_token(self, corp_id, permanent_code):
        """获取企业访问令牌 -- 代开发"""
        url = f"{self.base_url}/gettoken"
        params = {
            "corpid": corp_id,
            "corpsecret": permanent_code
        }
        
        result = self._request('GET', url, params=params)
        if result:
            return {
                'token': result.get('access_token'),
                'expires_in': result.get('expires_in', 7200)
            }
        return None