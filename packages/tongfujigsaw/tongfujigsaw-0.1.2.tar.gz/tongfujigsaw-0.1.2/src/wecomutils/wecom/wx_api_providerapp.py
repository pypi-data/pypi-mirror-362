from .wx_api import WXApiBase
from .license import LicenseModule

import logging
import requests

logger = logging.getLogger()


class WXApiProviderApp(WXApiBase):
    def __init__(self):
        super().__init__()
        self.license = LicenseModule()
    
    def get_suite_token(self, suite_id, suite_secret, suite_ticket):
        """获取第三方应用凭证 -- 代开发"""
        if not suite_ticket:
            logger.error("No suite_ticket provided")
            return None

        url = f"{self.base_url}/service/get_suite_token"
        data = {
            "suite_id": suite_id,
            "suite_secret": suite_secret,
            "suite_ticket": suite_ticket
        }
        
        result = self._request('POST', url, json=data)
        if result:
            return {
                'token': result.get('suite_access_token'),
                'expires_in': result.get('expires_in', 7200)
            }
        return None
    
    def get_permanent_code(self, suite_access_token, auth_code):
        """获取企业永久授权码 -- 代开发"""
        url = f"{self.base_url}/service/get_permanent_code?suite_access_token={suite_access_token}"
        data = {"auth_code": auth_code}
        
        result = self._request('POST', url, json=data)
        if not result:
            return None
        return result

    def get_corp_token_provider(self, suite_access_token, auth_corpid, permanent_code):
        """获取企业凭证 -- 第三方产品
        
        Args:
            suite_access_token: 第三方应用的suite_access_token
            auth_corpid: 授权方的企业ID
            permanent_code: 企业微信后台推送的永久授权码
            
        Returns:
            dict: 包含token和过期时间的字典，格式为:
                {
                    'token': 'access_token',
                    'expires_in': 7200
                }
            None: 获取失败时返回None
        """
        url = f"{self.base_url}/service/get_corp_token"
        params = {"suite_access_token": suite_access_token}
        data = {
            "auth_corpid": auth_corpid,
            "permanent_code": permanent_code
        }
        
        result = self._request('POST', url, params=params, json=data)
        if result:
            return {
                'token': result.get('access_token'),
                'expires_in': result.get('expires_in', 7200)
            }
        return None

    def get_user_info_3rd(self, suite_access_token: str, code: str) -> dict:
        """获取访问用户身份 -- 第三方产品
        
        该接口用于根据code获取成员信息。
        
        Args:
            suite_access_token: 第三方应用的suite_access_token
            code: 通过成员授权获取到的code
            
        Returns:
            dict: 用户身份信息，格式为:
                {
                    'errcode': 0,
                    'errmsg': 'ok',
                    'CorpId': 'CORPID',  # 用户所属企业的corpid
                    'UserId': 'USERID',   # 用户在企业内的UserID
                    'DeviceId': 'DEVICEID', # 手机设备号(由企业微信在安装时随机生成)
                    'user_ticket': 'USER_TICKET', # 成员票据，最大为512字节
                    'expires_in': 7200,    # user_ticket的有效时间（秒）
                    'open_userid': 'OPEN_USERID' # 全局唯一的用户标识
                }
            None: 获取失败时返回None
        """
        url = f"{self.base_url}/service/getuserinfo3rd"
        params = {
            "suite_access_token": suite_access_token,
            "code": code
        }
        
        result = self._request('GET', url, params=params)
        return result

    def get_auth_info(self, suite_access_token: str, auth_corpid: str, permanent_code: str) -> dict:
        """获取企业授权信息  -- 第三方产品
        
        该接口用于通过永久授权码换取企业微信的授权信息。 
        永久code的获取，是通过临时授权码使用get_permanent_code接口获取到的permanent_code。
        
        Args:
            suite_access_token: 第三方应用的suite_access_token
            auth_corpid: 授权方企业的corpid
            permanent_code: 企业微信永久授权码，通过get_permanent_code获取
            
        Returns:
            dict: 授权信息，格式为:
                {
                    'errcode': 0,
                    'errmsg': 'ok',
                    'auth_corp_info': {
                        'corpid': 'xxxx',
                        'corp_name': 'name',
                        'corp_type': 'verified',
                        'corp_square_logo_url': 'yyyyy',
                        'corp_user_max': 50,
                        'corp_agent_max': 30,
                        'corp_full_name': 'full_name',
                        'verified_end_time': 1431775834,
                        'subject_type': 1,
                        'corp_wxqrcode': 'zzzzz',
                        'corp_scale': '1-50人',
                        'corp_industry': 'IT服务',
                        'corp_sub_industry': '计算机软件/硬件/信息服务',
                        'location': '广东省广州市'
                    },
                    'auth_info': {
                        'agent': [  # 授权的应用信息
                            {
                                'agentid': 1,
                                'name': 'NAME',
                                'round_logo_url': 'xxxxxx',
                                'square_logo_url': 'yyyyyy',
                                'appid': 1,
                                'privilege': {
                                    'level': 1,
                                    'allow_party': [1,2,3],
                                    'allow_user': ['zhansan','lisi'],
                                    'allow_tag': [1,2,3],
                                    'extra_party': [4,5,6],
                                    'extra_user': ['wangwu'],
                                    'extra_tag': [4,5,6]
                                }
                            },
                            {
                                'agentid': 2,
                                'name': 'NAME2',
                                'round_logo_url': 'xxxxxx',
                                'square_logo_url': 'yyyyyy',
                                'appid': 5
                            }
                        ]
                    }
                }
            None: 获取失败时返回None
        """
        url = f"{self.base_url}/service/get_auth_info"
        params = {"suite_access_token": suite_access_token}
        data = {
            "auth_corpid": auth_corpid,
            "permanent_code": permanent_code
        }
        
        result = self._request('POST', url, params=params, json=data)
        return result

    def kf_get_customer_service_list(self, access_token):
        """获取客服列表"""
        url = f"{self.base_url}/kf/account/list"
        params = {"access_token": access_token}
        result = self._request('POST', url, params=params, json={"offset": 0, "limit": 100})
        return result

    def kf_create_customer_service_account(self, access_token, name, media_id):
        """创建客服账户"""
        url = f"{self.base_url}/kf/account/add"
        params = {"access_token": access_token}
        data = {
            "name": name,
            "media_id": media_id
        }
        result = self._request('POST', url, params=params, json=data)
        return result

    def kf_get_servicer_list(self, access_token, open_kfid):
        """获取客服接待人员列表"""
        url = f"{self.base_url}/kf/servicer/list"
        params = {
            "access_token": access_token,
            "open_kfid": open_kfid
        }
        result = self._request('GET', url, params=params)
        return result

    def kf_add_servicer(self, access_token, open_kfid, user_id_list):
        """添加客服接待人员"""
        url = f"{self.base_url}/kf/servicer/add"
        params = {"access_token": access_token}
        data = {
            "open_kfid": open_kfid,
            "userid_list": user_id_list
        }
        result = self._request('POST', url, params=params, json=data)
        return result

    def kf_sync_messages(self, access_token, open_kfid, cursor=None, voice_format=0, limit=1000, token=None):
        """同步消息
        
        Args:
            access_token (str): 调用接口凭证，必填
            open_kfid (str): 指定拉取某个客服账号的消息，必填
            cursor (str, optional): 上一次调用时返回的next_cursor。若不填，从3天内最早的消息开始返回。不多于64字节
            voice_format (int, optional): 语音消息类型，0-Amr 1-Silk，默认0。可通过该参数控制返回的语音格式
            limit (int, optional): 期望请求的数据量，默认值和最大值都为1000。注意：可能会出现返回条数少于limit的情况，需结合返回的has_more字段判断是否继续请求
            token (str, optional): 回调事件返回的token字段，10分钟内有效；可不填，如果不填接口有严格的频率限制。不多于128字节
            
        Returns:
            dict: API响应结果
        """
        url = f"{self.base_url}/kf/sync_msg"
        params = {"access_token": access_token}
        data = {
            "open_kfid": open_kfid,
            "limit": limit,
            "voice_format": voice_format
        }
        if cursor:
            data['cursor'] = cursor
        if token:
            data['token'] = token
            
        result = self._request('POST', url, params=params, json=data)
        return result

    def kf_assign_servicer(self, access_token, open_kfid, external_userid, service_state, servicer_userid=None):
        """变更会话状态
        
        Args:
            access_token (str): 调用接口凭证
            open_kfid (str): 客服账号ID
            external_userid (str): 客户UserID
            service_state (int): 会话状态(1-API对接,2-人工服务,3-结束会话)
            servicer_userid (str, optional): 接待人员UserID，人工服务时必填
            
        Returns:
            dict: API响应结果
        """
        url = f"{self.base_url}/kf/service_state/trans"
        params = {"access_token": access_token}
        data = {
            "open_kfid": open_kfid,
            "external_userid": external_userid,
            "service_state": service_state
        }
        if servicer_userid:
            data["servicer_userid"] = servicer_userid
        
        result = self._request('POST', url, params=params, json=data)
        return result

    def kf_get_service_state(self, access_token, open_kfid, external_userid):
        """获取客服状态"""
        url = f"{self.base_url}/kf/service_state/get"
        params = {"access_token": access_token}
        data = {
            "open_kfid": open_kfid,
            "external_userid": external_userid
        }
        result = self._request('POST', url, params=params, json=data)
        return result

    def kf_send_msg(self, access_token, open_kfid, external_userid, msgtype, **msg_content):
        """发送客服消息
        
        Args:
            access_token (str): 调用接口凭证
            open_kfid (str): 客服账号ID
            external_userid (str): 客户UserID
            msgtype (str): 消息类型
            **msg_content: 消息内容，如text={"content": "hello"}
            
        Returns:
            dict: API响应结果
        """
        url = f"{self.base_url}/kf/send_msg"
        params = {"access_token": access_token}
        data = {
            "touser": external_userid,
            "open_kfid": open_kfid,
            "msgtype": msgtype,
            **msg_content
        }
        result = self._request('POST', url, params=params, json=data)
        return result

    def get_user_list(self, access_token, department_id=1, fetch_child=1):
        """获取部门成员列表
        
        Args:
            access_token (str): 调用接口凭证
            department_id (int): 获取的部门id，默认为1（根部门）
            fetch_child (int): 是否递归获取子部门下面的成员，默认为1
            
        Returns:
            dict: API响应结果
        """
        url = f"{self.base_url}/user/list"
        params = {
            "access_token": access_token,
            "department_id": department_id,
            "fetch_child": fetch_child
        }
        result = self._request('GET', url, params=params)
        return result

    def get_provider_token(self, corpid, provider_secret):
        """
        获取服务商的 provider_access_token
        
        Args:
            corpid (str): 服务商的企业ID
            provider_secret (str): 服务商的密钥
            
        Returns:
            dict: 包含 token 和 expires_in 的字典，获取失败返回 None
            {
                'token': 'provider_access_token',
                'expires_in': 7200
            }
        """
        try:
            logger.info("Getting provider access token from WeChat API")
            url = f"{self.base_url}/service/get_provider_token"
            
            data = {
                "corpid": corpid,
                "provider_secret": provider_secret
            }
            
            response = requests.post(url, json=data)
            result = response.json()
            
            if 'errcode' not in result or result.get('errcode') == 0:
                return {
                    'token': result['provider_access_token'],
                    'expires_in': result.get('expires_in', 7200)
                }
            else:
                logger.error(f"Failed to get provider token: {result}")
                return None
            
        except Exception as e:
            logger.error(f"Error getting provider token: {str(e)}")
            return None