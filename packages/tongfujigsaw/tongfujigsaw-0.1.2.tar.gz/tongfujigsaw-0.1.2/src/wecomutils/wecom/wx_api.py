import time
import logging
import requests
import json

logger = logging.getLogger()

class WedocModule:
    """企微文档模块，处理文档相关的API调用"""
    
    def __init__(self, api_base):
        self.api_base = api_base
    
    def creat_doc(self, access_token, data):
        """创建文档
        
        Args:
            access_token (str): 调用接口凭证
            data (dict): 文档创建参数，包含以下字段：
                - spaceid (str, optional): 空间spaceid，可选参数
                - fatherid (str, optional): 父目录fileid，在根目录时为空，可选参数
                - doc_type (int): 文档类型, 3:文档 4:表格 10:智能表格
                - doc_name (str): 文档名字
                - admin_users (list, optional): 文档管理员userid列表，可选参数
                
        Returns:
            dict: API响应结果，包含创建的文档信息
        """
        url = f"{self.api_base.base_url}/wedoc/create_doc"
        params = {"access_token": access_token}
        
        # 构建请求数据
        request_data = {
            "doc_type": data.get("doc_type"),
            "doc_name": data.get("doc_name")
        }
        
        # 添加可选参数
        if "spaceid" in data:
            request_data["spaceid"] = data["spaceid"]
        if "fatherid" in data:
            request_data["fatherid"] = data["fatherid"]
        if "admin_users" in data:
            request_data["admin_users"] = data["admin_users"]
        
        result = self.api_base._request('POST', url, params=params, json=request_data)
        return result
    
    def smartsheet_get_sheet(self, access_token, data):
        """智能表格获取工作表详情

        Args:
            access_token (str): 调用接口凭证
            data (dict): 参数，包含以下字段：
                - docid (str): 智能表格的docid

        Returns:
            dict: API响应结果，包含工作表详情
        """
        url = f"{self.api_base.base_url}/wedoc/smartsheet/get_sheet"
        params = {"access_token": access_token}

        # 构建请求数据
        request_data = {
            "docid": data.get("docid")
        }

        result = self.api_base._request('POST', url, params=params, json=request_data)
        return result

    def smartsheet_add_sheet(self, access_token, data):
        """智能表格添加工作表
        
        Args:
            access_token (str): 调用接口凭证
            data (dict): 工作表创建参数，包含以下字段：
                - docid (str): 智能表格的docid
                - properties (dict): 工作表属性
                    - title (str): 工作表标题
                    - index (int): 工作表位置索引
                
        Returns:
            dict: API响应结果，包含创建的工作表信息
        """
        url = f"{self.api_base.base_url}/wedoc/smartsheet/add_sheet"
        params = {"access_token": access_token}
        
        # 构建请求数据
        request_data = {
            "docid": data.get("docid"),
            "properties": data.get("properties", {})
        }
        
        result = self.api_base._request('POST', url, params=params, json=request_data)
        return result
    
    def smartsheet_delete_sheet(self, access_token, data):
        """智能表格删除工作表

        Args:
            access_token (str): 调用接口凭证
            data (dict): 删除参数，包含以下字段：
                - docid (str): 智能表格的docid
                - sheet_id (str): 工作表ID

        Returns:
            dict: API响应结果
        """
        url = f"{self.api_base.base_url}/wedoc/smartsheet/delete_sheet"
        params = {"access_token": access_token}

        # 构建请求数据
        request_data = {
            "docid": data.get("docid"),
            "sheet_id": data.get("sheet_id")
        }

        result = self.api_base._request('POST', url, params=params, json=request_data)
        return result

    
    def smartsheet_get_views(self, access_token, data):
        """智能表格获取视图列表

        Args:
            access_token (str): 调用接口凭证
            data (dict): 参数，包含以下字段：
                - docid (str): 智能表格的docid
                - sheet_id (str): 工作表ID

        Returns:
            dict: API响应结果，包含视图列表等信息
        """
        url = f"{self.api_base.base_url}/wedoc/smartsheet/get_views"
        params = {"access_token": access_token}

        # 构建请求数据
        request_data = {
            "docid": data.get("docid"),
            "sheet_id": data.get("sheet_id")
        }

        result = self.api_base._request('POST', url, params=params, json=request_data)
        return result

    def smartsheet_delete_views(self, access_token, data):
        """智能表格删除视图

        Args:
            access_token (str): 调用接口凭证
            data (dict): 删除参数，包含以下字段：
                - docid (str): 智能表格的docid
                - sheet_id (str): 工作表ID
                - view_ids (list): 视图ID列表

        Returns:
            dict: API响应结果
        """
        url = f"{self.api_base.base_url}/wedoc/smartsheet/delete_views"
        params = {"access_token": access_token}

        # 构建请求数据
        request_data = {
            "docid": data.get("docid"),
            "sheet_id": data.get("sheet_id"),
            "view_ids": data.get("view_ids", [])
        }

        result = self.api_base._request('POST', url, params=params, json=request_data)
        return result

    
    def smartsheet_add_fields(self, access_token, data):
        """智能表格添加字段
        
        Args:
            access_token (str): 调用接口凭证
            data (dict): 字段添加参数，包含以下字段：
                - docid (str): 智能表格的docid
                - sheet_id (str): 工作表ID
                - fields (list): 字段列表，每个字段包含：
                    - field_title (str): 字段标题
                    - field_type (str): 字段类型，支持：
                        - FIELD_TYPE_TEXT: 文本
                        - FIELD_TYPE_NUMBER: 数字
                        - FIELD_TYPE_DATE_TIME: 日期时间
                        - FIELD_TYPE_SINGLE_SELECT: 单选
                        - FIELD_TYPE_MULTI_SELECT: 多选
                        - FIELD_TYPE_USER: 成员
                        - FIELD_TYPE_ATTACHMENT: 附件
                        - FIELD_TYPE_LINK: 链接
                        - FIELD_TYPE_LOCATION: 地理位置
                        - FIELD_TYPE_PHONE: 电话号码
                        - FIELD_TYPE_EMAIL: 邮箱
                    - field_property (dict, optional): 字段属性，根据字段类型不同而不同
                
        Returns:
            dict: API响应结果，包含添加的字段信息
        """
        url = f"{self.api_base.base_url}/wedoc/smartsheet/add_fields"
        params = {"access_token": access_token}
        
        # 构建请求数据
        request_data = {
            "docid": data.get("docid"),
            "sheet_id": data.get("sheet_id"),
            "fields": data.get("fields", [])
        }
        
        result = self.api_base._request('POST', url, params=params, json=request_data)
        return result
    
    def smartsheet_get_fields(self, access_token, data):
        """智能表格获取字段信息
        
        Args:
            access_token (str): 调用接口凭证
            data (dict): 查询参数，包含以下字段：
                - docid (str): 智能表格的docid
                - sheet_id (str): 工作表ID
                
        Returns:
            dict: API响应结果，包含字段信息，格式为：
                {
                    'errcode': 0,
                    'errmsg': 'ok',
                    'fields': [
                        {
                            'field_id': 'field_id',
                            'field_title': 'field_title',
                            'field_type': 'FIELD_TYPE_TEXT',
                            'field_desc': 'field_description',
                            'property': {
                                'defaultValue': '',
                                'precision': 0,
                                'symbol': '',
                                'options': []
                            }
                        }
                    ]
                }
        """
        url = f"{self.api_base.base_url}/wedoc/smartsheet/get_fields"
        params = {"access_token": access_token}
        
        # 构建请求数据
        request_data = {
            "docid": data.get("docid"),
            "sheet_id": data.get("sheet_id")
        }
        
        result = self.api_base._request('POST', url, params=params, json=request_data)
        return result

    def smartsheet_delete_fields(self, access_token, data):
        """智能表格删除字段

        Args:
            access_token (str): 调用接口凭证
            data (dict): 删除字段参数，包含以下字段：
                - docid (str): 智能表格的docid
                - sheet_id (str): 工作表ID
                - field_ids (list): 要删除的字段ID列表

        Returns:
            dict: API响应结果
        """
        url = f"{self.api_base.base_url}/wedoc/smartsheet/delete_fields"
        params = {"access_token": access_token}

        # 构建请求数据
        request_data = {
            "docid": data.get("docid"),
            "sheet_id": data.get("sheet_id"),
            "field_ids": data.get("field_ids", [])
        }

        result = self.api_base._request('POST', url, params=params, json=request_data)
        return result


    def smartsheet_add_records(self, access_token, data):
        """智能表格添加记录
        
        Args:
            access_token (str): 调用接口凭证
            data (dict): 记录添加参数，包含以下字段：
                - docid (str): 智能表格的docid
                - sheet_id (str): 工作表ID
                - key_type (str): 键类型，支持：
                    - CELL_VALUE_KEY_TYPE_FIELD_TITLE: 使用字段标题作为键
                    - CELL_VALUE_KEY_TYPE_FIELD_ID: 使用字段ID作为键
                - records (list): 记录列表，每个记录包含：
                    - values (dict): 字段值，键为字段标题或ID，值为字段值数组
                        每个字段值包含：
                        - type (str): 值类型 (text, number, date, user, etc.)
                        - 对应的值字段 (text, number, date, user_id, etc.)
        
        注意：
            不能通过此接口给创建时间、最后编辑时间、创建人和最后编辑人四种类型的字段添加记录
                
        Returns:
            dict: API响应结果，包含添加的记录信息
        """
        url = f"{self.api_base.base_url}/wedoc/smartsheet/add_records"
        params = {"access_token": access_token}
        
        # 构建请求数据
        request_data = {
            "docid": data.get("docid"),
            "sheet_id": data.get("sheet_id"),
            "key_type": data.get("key_type", "CELL_VALUE_KEY_TYPE_FIELD_TITLE"),
            "records": data.get("records", [])
        }
        
        result = self.api_base._request('POST', url, params=params, json=request_data)
        return result
    
    def smartsheet_get_records(self, access_token, data):
        """智能表格查询记录
        
        Args:
            access_token (str): 调用接口凭证
            data (dict): 查询参数，包含以下字段：
                - docid (str): 智能表格的docid
                - sheet_id (str): 工作表ID
                - view_id (str, optional): 视图ID，可选参数
                - filter_spec (dict, optional): 过滤条件规范，包含：
                    - conjunction (str): 连接方式，CONJUNCTION_AND 或 CONJUNCTION_OR
                    - conditions (list): 条件列表，每个条件包含：
                        - field_id (str, optional): 字段ID
                        - field_title (str, optional): 字段标题（field_id和field_title二选一）
                        - field_type (str): 字段类型，如FIELD_TYPE_TEXT
                        - operator (str): 操作符，如OPERATOR_EQUAL, OPERATOR_CONTAINS等
                        - string_value (dict): 字符串值，包含value字段
                        - number_value (dict): 数字值，包含value字段
                        - date_value (dict): 日期值，包含value字段
                - sorts (list, optional): 排序条件列表，每个排序条件包含：
                    - field_title (str): 字段标题
                    - desc (bool): 是否降序，true为降序，false为升序
                - limit (int, optional): 返回记录数量限制，默认100，最大1000
                - offset (int, optional): 偏移量，用于分页，默认0
                
        Returns:
            dict: API响应结果，包含查询到的记录信息，格式为：
                {
                    'errcode': 0,
                    'errmsg': 'ok',
                    'records': [
                        {
                            'record_id': 'record_id',
                            'values': {
                                'field_title': [{'type': 'text', 'text': 'value'}]
                            }
                        }
                    ],
                    'total': 总记录数,
                    'has_more': 是否还有更多记录
                }
        """
        url = f"{self.api_base.base_url}/wedoc/smartsheet/get_records"
        params = {"access_token": access_token}
        
        # 构建请求数据
        request_data = {
            "docid": data.get("docid"),
            "sheet_id": data.get("sheet_id")
        }
        
        # 添加可选参数
        if "view_id" in data:
            request_data["view_id"] = data["view_id"]
        if "filter_spec" in data:
            request_data["filter_spec"] = data["filter_spec"]
        if "sorts" in data:
            request_data["sorts"] = data["sorts"]
        if "limit" in data:
            request_data["limit"] = data["limit"]
        if "offset" in data:
            request_data["offset"] = data["offset"]
        
        result = self.api_base._request('POST', url, params=params, json=request_data)
        return result

    def smartsheet_del_records(self, access_token, data):
        """智能表格删除记录
        
        Args:
            access_token (str): 调用接口凭证
            data (dict): 删除参数，包含以下字段：
                - docid (str): 智能表格的docid
                - sheet_id (str): 工作表ID
                - record_ids (list): 要删除的记录ID列表，最多支持100个
                
        Returns:
            dict: API响应结果，包含删除结果信息
        """
        url = f"{self.api_base.base_url}/wedoc/smartsheet/delete_records"
        params = {"access_token": access_token}
        
        # 构建请求数据
        request_data = {
            "docid": data.get("docid"),
            "sheet_id": data.get("sheet_id"),
            "record_ids": data.get("record_ids", [])
        }
        
        result = self.api_base._request('POST', url, params=params, json=request_data)
        return result

    def smartsheet_update_records(self, access_token, data):
        """智能表格更新记录
        
        Args:
            access_token (str): 调用接口凭证
            data (dict): 更新参数，包含以下字段：
                - docid (str): 智能表格的docid
                - sheet_id (str): 工作表ID
                - key_type (str): 键类型，支持：
                    - CELL_VALUE_KEY_TYPE_FIELD_ID: 使用字段ID作为键
                    - CELL_VALUE_KEY_TYPE_FIELD_TITLE: 使用字段标题作为键
                - records (list): 要更新的记录列表，每个记录包含：
                    - record_id (str): 记录ID
                    - values (dict): 要更新的字段值，键为字段ID或标题，值为字段内容
                        - 文本字段格式: [{"type": "text", "text": "内容"}]
                        - 数字字段格式: 数字值
                        - 日期字段格式: 时间戳
                        - 选择字段格式: [{"type": "text", "text": "选项值"}]
                
        Returns:
            dict: API响应结果，包含更新结果信息，格式为：
                {
                    'errcode': 0,
                    'errmsg': 'ok',
                    'updated_count': 更新的记录数量
                }
        """
        url = f"{self.api_base.base_url}/wedoc/smartsheet/update_records"
        params = {"access_token": access_token}
        
        # 构建请求数据
        request_data = {
            "docid": data.get("docid"),
            "sheet_id": data.get("sheet_id"),
            "key_type": data.get("key_type", "CELL_VALUE_KEY_TYPE_FIELD_TITLE"),
            "records": data.get("records", [])
        }
        
        result = self.api_base._request('POST', url, params=params, json=request_data)
        return result

   
class WXApiBase:
    def __init__(self):
        self.base_url = "https://qyapi.weixin.qq.com/cgi-bin"
        self.wedoc = WedocModule(self)

    def _request(self, method, url, **kwargs):
        """统一的请求处理，增强日志记录"""
        request_id = f"REQ-{int(time.time() * 1000)}-{id(kwargs)}"  # 生成唯一请求ID
        
        try:
            # 记录请求的详细信息
            logger.info(f"[{request_id}] 请求开始: {method} {url}")
            
            # 记录请求参数
            request_details = {
                "method": method,
                "url": url,
            }
            
            # 记录请求头（排除敏感信息）
            if 'headers' in kwargs and kwargs['headers']:
                headers = kwargs['headers'].copy()
                for key, value in list(headers.items()):
                    if 'token' in key.lower() or 'secret' in key.lower() or 'auth' in key.lower():
                        headers[key] = "******"
                request_details["headers"] = headers
            
            # 记录URL参数
            if 'params' in kwargs and kwargs['params']:
                params = kwargs['params'].copy()
                for key, value in list(params.items()):
                    if 'token' in key.lower() or 'secret' in key.lower() or 'access' in key.lower():
                        params[key] = "******"
                request_details["params"] = params
                
                # 构建完整URL用于日志记录
                query_string = "&".join([f"{k}={'******' if 'token' in str(k).lower() else v}" for k, v in kwargs['params'].items()])
                logger.info(f"[{request_id}] 完整URL: {url}?{query_string}")
            
            # 记录请求体
            if 'json' in kwargs and kwargs['json']:
                request_details["body"] = kwargs['json']
                logger.info(f"[{request_id}] 请求体: {json.dumps(kwargs['json'], ensure_ascii=False)}")
            elif 'data' in kwargs and kwargs['data']:
                try:
                    if isinstance(kwargs['data'], bytes):
                        request_details["body"] = "(二进制数据)"
                    else:
                        request_details["body"] = kwargs['data']
                        logger.info(f"[{request_id}] 请求体: {kwargs['data']}")
                except:
                    request_details["body"] = "(无法序列化的数据)"
            
            # 记录请求细节摘要
            logger.info(f"[{request_id}] 请求详情: {json.dumps(request_details, ensure_ascii=False)}")
            
            # 执行实际请求
            start_time = time.time()
            response = requests.request(method, url, **kwargs)
            duration = time.time() - start_time
            
            # 记录响应状态和时间
            logger.info(f"[{request_id}] 响应状态: {response.status_code}, 耗时: {duration:.3f}秒")
            
            # 尝试解析并记录响应体
            try:
                result = response.json()
                # 根据响应大小决定日志详细程度
                result_str = json.dumps(result, ensure_ascii=False)
                if len(result_str) > 1000:
                    # 对于大型响应，只记录关键信息
                    if isinstance(result, dict):
                        errcode = result.get('errcode', 'N/A')
                        errmsg = result.get('errmsg', 'N/A')
                        logger.info(f"[{request_id}] 响应(摘要): errcode={errcode}, errmsg={errmsg}, 数据大小={len(result_str)}字节")
                        
                        # 对于错误响应，记录完整内容
                        if errcode != 0 and errcode != 'N/A':
                            logger.error(f"[{request_id}] 错误响应: {result_str}")
                    else:
                        logger.info(f"[{request_id}] 响应太大，长度为{len(result_str)}字节")
                else:
                    # 对于小型响应，记录完整内容
                    logger.info(f"[{request_id}] 响应体: {result_str}")
                
                # 返回结果前检查错误码
                if 'errcode' not in result or result.get('errcode') == 0:
                    return result
                
                logger.error(f"[{request_id}] 微信API错误: {result_str}")
                return result  # 返回包含错误信息的结果，而不是None
                
            except ValueError:
                # 非JSON响应
                content = response.text[:200] + "..." if len(response.text) > 200 else response.text
                logger.warning(f"[{request_id}] 非JSON响应: {content}")
                return {
                    'errcode': 50002,
                    'errmsg': f'非JSON响应: {content}'
                }
                
        except requests.RequestException as e:
            logger.error(f"[{request_id}] 请求异常: {str(e)}", exc_info=True)
            return {
                'errcode': 50003,
                'errmsg': f'请求异常: {str(e)}'
            }
        except Exception as e:
            logger.error(f"[{request_id}] 未预期的异常: {str(e)}", exc_info=True)
            return {
                'errcode': 50004,
                'errmsg': f'未预期的异常: {str(e)}'
            }

    def send_text_message(self, access_token, user_id, agent_id, content):
        """发送文本消息"""
        url = f"{self.base_url}/message/send"
        params = {"access_token": access_token}
        data = {
            "touser": user_id,
            "msgtype": "text",
            "agentid": agent_id,
            "text": {
                "content": content
            }
        }
        
        result = self._request('POST', url, params=params, json=data)
        return result is not None and result.get('errcode') == 0



    # Add other provider-app specific methods here



    # Add other provider-dev specific methods here

    def get_approval_info(self, access_token, starttime, endtime, new_cursor="", size=100, filters=None):
        """
        获取审批数据
        
        Args:
            access_token (str): 调用接口凭证
            starttime (str): 开始时间戳
            endtime (str): 结束时间戳
            new_cursor (str, optional): 分页查询游标，默认为空
            size (int, optional): 每次拉取的数据量，默认为100
            filters (list, optional): 筛选条件，可选值包括：
                - template_id: 模板类型/模板id
                - creator: 申请人
                - department: 审批单提单者所在部门
                - sp_status: 审批状态，1-审批中；2-已通过；3-已驳回；4-已撤销；6-通过后撤销；7-已删除；10-已支付
        
        Returns:
            dict: 审批数据，如果请求失败则返回None
        """
        url = f"{self.base_url}/oa/getapprovalinfo"
        params = {"access_token": access_token}
        
        data = {
            "starttime": starttime,
            "endtime": endtime,
            "new_cursor": new_cursor,
            "size": size
        }
        
        if filters:
            data["filters"] = filters
        
        result = self._request('POST', url, params=params, json=data)
        return result
    
    def get_approval_detail(self, access_token, sp_no):
        """
        获取审批申请详情
        
        Args:
            access_token (str): 调用接口凭证
            sp_no (str): 审批单编号
            
        Returns:
            dict: 审批详情数据，如果请求失败则返回None
        """
        url = f"{self.base_url}/oa/getapprovaldetail"
        params = {"access_token": access_token}
        
        data = {
            "sp_no": sp_no
        }
        
        result = self._request('POST', url, params=params, json=data)
        return result

    
