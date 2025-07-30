import logging
import xml.etree.ElementTree as ET
from .the3party.WXBizMsgCrypt3 import WXBizMsgCrypt

logger = logging.getLogger()

class WXCrypto:
    def __init__(self, token, encoding_aes_key, receive_id):
        self.crypto = WXBizMsgCrypt(token, encoding_aes_key, receive_id)

    def verify_url(self, msg_signature, timestamp, nonce, echostr):
        """验证URL"""
        ret, echo = self.crypto.VerifyURL(msg_signature, timestamp, nonce, echostr)
        return ret, echo

    def decrypt_msg(self, post_data, msg_signature, timestamp, nonce):
        """解密消息"""
        ret, decrypted_xml = self.crypto.DecryptMsg(post_data, msg_signature, timestamp, nonce)
        return ret, decrypted_xml

    @staticmethod
    def parse_xml(xml_string):
        """解析XML为字典"""
        try:
            root = ET.fromstring(xml_string)
            result = {}
            for child in root:
                result[child.tag] = child.text
            return result
        except Exception as e:
            logger.error(f"Failed to parse XML: {str(e)}")
            return None 