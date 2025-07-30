import json
import logging
from alibabacloud_fc20230330.client import Client as FC20230330Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_darabonba_stream.client import Client as StreamClient
from alibabacloud_fc20230330 import models as fc20230330_models
from alibabacloud_tea_util import models as util_models

logger = logging.getLogger()

class FCService:
    """Aliyun Function Compute Service"""
    
    def __init__(self, context):
        """Initialize FC client with context credentials"""
        config = open_api_models.Config(
            access_key_id=context.credentials.access_key_id,
            access_key_secret=context.credentials.access_key_secret,
            security_token=context.credentials.security_token
        )
        config.endpoint = "fcv3.cn-shenzhen.aliyuncs.com"
        self.client = FC20230330Client(config)
        
    def invoke_async(self, function_name, data):
        """
        Invoke function asynchronously
        
        Args:
            function_name (str): Name of the function to invoke
            data (dict): Data to pass to the function
            
        Returns:
            dict: Response containing request_id and status
        """
        try:
            # Prepare message data
            body_stream = StreamClient.read_from_string(json.dumps(data))
            
            # Set up invoke headers
            invoke_headers = fc20230330_models.InvokeFunctionHeaders(
                x_fc_invocation_type='Async',
                x_fc_log_type='None'
            )
            
            # Create invoke request
            invoke_request = fc20230330_models.InvokeFunctionRequest(
                qualifier='LATEST',
                body=body_stream
            )
            
            runtime = util_models.RuntimeOptions()
            
            # Call the function asynchronously
            result = self.client.invoke_function_with_options(
                function_name,
                invoke_request,
                invoke_headers,
                runtime
            )
            
            # Get request ID from response headers
            request_id = result.headers.get('x-fc-request-id')
            logger.info(f"Async function invocation started. Function: {function_name}, Request ID: {request_id}")
            
            return {
                'success': True,
                'request_id': request_id,
                'message': 'Function invocation started'
            }
            
        except Exception as e:
            logger.error(f"Error invoking function {function_name}: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            } 
    
    def invoke(self, function_name, data):
        """Invoke a function synchronously.
        
        Args:
            function_name (str): Name of the function to invoke
            data (dict): Data to pass to the function
            
        Returns:
            dict: Response from the function
        """
        try:
            # Prepare message data
            body_stream = StreamClient.read_from_string(json.dumps(data))
            
            # Set up invoke headers
            invoke_headers = fc20230330_models.InvokeFunctionHeaders(
                x_fc_invocation_type='Sync',
                x_fc_log_type='None'
            )
            
            # Create invoke request
            invoke_request = fc20230330_models.InvokeFunctionRequest(
                qualifier='LATEST',
                body=body_stream
            )
            
            runtime = util_models.RuntimeOptions()
            
            # Call the function synchronously
            result = self.client.invoke_function_with_options(
                function_name,
                invoke_request,
                invoke_headers,
                runtime
            )
            
            # Get response body
            response_body = result.body
            if response_body:
                response_data = json.loads(response_body.read())
                logger.info(f"Sync function invocation completed. Function: {function_name}")
                return response_data
            
            return None
            
        except Exception as e:
            logger.error(f"Error invoking function {function_name}: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }