from .wx_api import WXApiBase
import logging

logger = logging.getLogger()

class LicenseModule(WXApiBase):
    """企业微信许可证管理模块"""
    
    def get_order_list(self, access_token, corpid=None, start_time=None, end_time=None, cursor=None, limit=500):
        """获取订单列表
        
        Args:
            access_token: provider_access_token
            corpid: 企业id
            start_time: 开始时间
            end_time: 结束时间
            cursor: 分页游标
            limit: 返回的最大记录数,默认500
        """
        logger.info(f"Getting order list for corp {corpid}")
        url = f"{self.base_url}/license/list_order"
        params = {"provider_access_token": access_token}
        data = {
            "corpid": corpid,
            "limit": limit
        }
        if start_time:
            data["start_time"] = start_time 
        if end_time:
            data["end_time"] = end_time
        if cursor:
            data["cursor"] = cursor
        
        result = self._request('POST', url, params=params, json=data)
        logger.info(f"Got order list result: {result}")
        return result

    def get_order_detail(self, access_token, order_id):
        """获取订单详情
        
        Args:
            access_token: provider_access_token
            order_id: 订单ID
        """
        logger.info(f"Getting order detail for order {order_id}")
        url = f"{self.base_url}/license/get_order"
        params = {"provider_access_token": access_token}
        data = {"order_id": order_id}
        
        result = self._request('POST', url, params=params, json=data)
        logger.info(f"Got order detail result: {result}")
        return result

    def get_order_account_list(self, access_token, order_id, cursor=None, limit=200):
        """获取订单可激活账户列表
        
        Args:
            access_token: provider_access_token
            order_id: 订单ID
            cursor: 分页游标
            limit: 返回的最大记录数,默认200
        """
        logger.info(f"Getting account list for order {order_id}")
        url = f"{self.base_url}/license/list_order_account"
        params = {"provider_access_token": access_token}
        data = {
            "order_id": order_id,
            "limit": limit
        }
        if cursor:
            data["cursor"] = cursor
        
        result = self._request('POST', url, params=params, json=data)
        logger.info(f"Got account list result: {result}")
        return result

    def get_actived_accounts(self, access_token, corpid, cursor=None, limit=500):
        """获取企业的账号列表
        
        Args:
            access_token: provider_access_token
            corpid: 企业corpid
            cursor: 分页游标
            limit: 返回的最大记录数,默认500,最大1000
        """
        logger.info(f"Getting actived accounts for corp {corpid}")
        url = f"{self.base_url}/license/list_actived_account"
        params = {"provider_access_token": access_token}
        data = {
            "corpid": corpid,
            "limit": min(limit, 1000)  # 最大值1000
        }
        if cursor:
            data["cursor"] = cursor
        
        result = self._request('POST', url, params=params, json=data)
        logger.info(f"Got actived accounts result: {result}")
        return result

    def get_account_detail(self, access_token, corp_id, user_id):
        """获取账号激活详情
        
        Args:
            access_token: provider_access_token
            corp_id: 企业ID
            user_id: 用户ID
        """
        logger.info(f"Getting account detail for user {user_id} in corp {corp_id}")
        url = f"{self.base_url}/license/get_active_info_by_user"
        params = {"provider_access_token": access_token}
        data = {
            "corpid": corp_id,
            "userid": user_id
        }
        
        result = self._request('POST', url, params=params, json=data)
        logger.info(f"Got account detail result: {result}")
        return result

    def get_active_code_detail(self, access_token, corp_id, active_code):
        """获取激活码详情
        
        Args:
            access_token: provider_access_token
            corp_id: 企业ID
            active_code: 激活码
        """
        logger.info(f"Getting active code detail for code {active_code} in corp {corp_id}")
        url = f"{self.base_url}/license/get_active_info_by_code"
        params = {"provider_access_token": access_token}
        data = {
            "corpid": corp_id,
            "active_code": active_code
        }
        
        result = self._request('POST', url, params=params, json=data)
        logger.info(f"Got active code detail result: {result}")
        return result

    def activate_account(self, access_token, corp_id, active_code, user_id):
        """激活企业账号
        
        Args:
            access_token: provider_access_token
            corp_id: 企业ID
            active_code: 激活码
            user_id: 用户ID
        """
        logger.info(f"Activating account for user {user_id} with code {active_code} in corp {corp_id}")
        url = f"{self.base_url}/license/active_account"
        params = {"provider_access_token": access_token}
        data = {
            "corpid": corp_id,
            "active_code": active_code,
            "userid": user_id
        }
        
        result = self._request('POST', url, params=params, json=data)
        logger.info(f"Account activation result: {result}")
        return result
