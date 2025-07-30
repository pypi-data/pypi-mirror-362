from .wx_api import WXApiBase

class WXApiInternal(WXApiBase):
    """
    WeChat API client for internal applications.
    This class handles API interactions specific to internal enterprise WeChat applications.
    """
    def get_permissions(self, access_token):
        """获取应用权限详情"""
        url = f"{self.base_url}/agent/get_permissions?access_token={access_token}"
        return self._request('GET', url)

    # Add other internal specific methods here

    def get_admin_list(self, access_token):
        """获取应用管理员列表"""
        url = f"{self.base_url}/agent/get_admin_list?access_token={access_token}"
        return self._request('GET', url)
    
    def get_access_token(self, corp_id, corp_secret):
        """获取企业微信的access_token"""
        url = f"{self.base_url}/gettoken?corpid={corp_id}&corpsecret={corp_secret}"
        return self._request('GET', url)
