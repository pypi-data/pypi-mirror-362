from time import time
import os
import logging

logger = logging.getLogger(__name__)

class TokenCache:
    def __init__(self, storage, wx_api):
        self.storage = storage
        self.wx_api = wx_api
    
    
    def get_access_token(self, filename='access_token'):
        """
        Get access token from cache or fetch new one if needed, just for wecom_internal_app  first
        
        Args:
            filename (str): Name of file to store access token. Defaults to 'access_token'
            
        Returns:
            str: The access token or None if failed to get token
        """
        # Load the cached access token
        access_token_info = self.storage.load_from_file(filename)
        current_time = int(time())
        
        # Check if the cached token is valid
        if access_token_info and isinstance(access_token_info, dict):
            if 'token' in access_token_info and 'expires_at' in access_token_info:
                if current_time < access_token_info['expires_at']:
                    logger.info("Using cached access token")
                    return access_token_info['token']
        
        logger.info("Local access_token not found or expired, fetching new one...")
        
        # Fetch a new access token from the API
        access_token_info = self.wx_api.get_access_token(
            corp_id=os.environ.get('CORP_ID'),
            corp_secret=os.environ.get('CORP_SECRET')
        )
        
        if not access_token_info or 'access_token' not in access_token_info:
            logger.error("Failed to get access_token")
            return None
        
        # Save the new token and its expiration time
        token_data = {
            'token': access_token_info['access_token'],
            'expires_at': current_time + access_token_info.get('expires_in', 7200)  # Default to 7200 seconds if not provided
        }
        self.storage.save_to_file(filename, token_data)
        logger.info(f"New access token saved: {token_data['token']}")
        return token_data['token']

    def get_suite_token(self, filename='suite_token', ticket_filename='suite_ticket'):
        """
        Get suite token from cache or fetch new one if needed
        
        Args:
            filename (str): Name of file to store suite token. Defaults to 'suite_token'
            ticket_filename (str): Name of file to read suite ticket. Defaults to 'suite_ticket'
        """
        # Load the cached suite token
        suite_token_info = self.storage.load_from_file(filename)
        current_time = int(time())
        
        # Check if the cached token is valid
        if suite_token_info and isinstance(suite_token_info, dict):
            if 'token' in suite_token_info and 'expires_at' in suite_token_info:
                if current_time < suite_token_info['expires_at']:
                    logger.info("Using cached suite token")
                    return suite_token_info['token']
        
        logger.info("Local suite_token not found or expired, fetching new one...")
        suite_ticket = self.storage.load_from_file(ticket_filename)
        if not suite_ticket:
            logger.error("suite_ticket not found")
            return None
            
        # Fetch a new suite token from the API
        suite_token_info = self.wx_api.get_suite_token(
            suite_id=os.environ.get('SUITE_ID'),
            suite_secret=os.environ.get('SUITE_SECRET'),
            suite_ticket=suite_ticket
        )
        
        if not suite_token_info:
            logger.error("Failed to get suite_access_token")
            return None
        
        # Save the new token and its expiration time
        token_data = {
            'token': suite_token_info['token'],
            'expires_at': current_time + suite_token_info.get('expires_in', 7200)  # Default to 7200 seconds if not provided
        }
        self.storage.save_to_file(filename, token_data)
        logger.info(f"New suite token saved: {token_data['token']}")
        return token_data['token']

    def get_corp_token(self, corp_id, permanent_code, suite_token, filename_prefix='corp_token'):
        """
        Get corp token from cache or fetch new one if needed
        
        Args:
            corp_id (str): Corporation ID
            permanent_code (str): Permanent authorization code
            suite_token (str): Suite access token
            filename_prefix (str): Prefix for token file name. Defaults to 'corp_token'
        """
        try:
            token_key = f'{filename_prefix}_{corp_id}'
            token_info = self.storage.load_from_file(token_key)
            
            current_time = int(time())
            if token_info:
                try:
                    if isinstance(token_info, dict) and 'token' in token_info and 'expires_at' in token_info:
                        if current_time < token_info['expires_at']:
                            logger.info("Using cached corp token")
                            return token_info['token']
                except (TypeError, ValueError, KeyError):
                    logger.warning("Local corp_token file format is invalid")
            
            logger.info(f"Fetching corporate access token: corp_id={corp_id}")
            new_token_info = self.wx_api.get_corp_token_provider(
                suite_access_token=suite_token,
                auth_corpid=corp_id,
                permanent_code=permanent_code
            )
            
            if not new_token_info:
                logger.error("Failed to get corporate access token")
                return None
                
            token_data = {
                'token': new_token_info['token'],
                'expires_at': current_time + new_token_info['expires_in']
            }
            self.storage.save_to_file(token_key, token_data)
            return token_data['token']
            
        except Exception as e:
            logger.error(f"Error getting corporate access token: {str(e)}")
            return None 

    def get_provider_token(self, filename='provider_token'):
        """
        Get provider access token from cache or fetch new one if needed
        
        Args:
            filename (str): Name of file to store provider token. Defaults to 'provider_token'
        """
        # Load the cached provider token
        provider_token_info = self.storage.load_from_file(filename)
        current_time = int(time())
        
        # Check if the cached token is valid
        if provider_token_info and isinstance(provider_token_info, dict):
            if 'token' in provider_token_info and 'expires_at' in provider_token_info:
                if current_time < provider_token_info['expires_at']:
                    logger.info("Using cached provider token")
                    return provider_token_info['token']
        
        logger.info("Local provider_token not found or expired, fetching new one...")
            
        # Fetch a new provider token from the API
        provider_token_info = self.wx_api.get_provider_token(
            corpid=os.environ.get('PROVIDER_CORP_ID'),
            provider_secret=os.environ.get('PROVIDER_CORP_SECRET')
        )
        
        if not provider_token_info:
            logger.error("Failed to get provider_access_token")
            return None
        
        # Save the new token and its expiration time
        token_data = {
            'token': provider_token_info['token'],
            'expires_at': current_time + provider_token_info.get('expires_in', 7200)  # Default to 7200 seconds if not provided
        }
        self.storage.save_to_file(filename, token_data)
        logger.info(f"New provider token saved: {token_data['token']}")
        return token_data['token'] 