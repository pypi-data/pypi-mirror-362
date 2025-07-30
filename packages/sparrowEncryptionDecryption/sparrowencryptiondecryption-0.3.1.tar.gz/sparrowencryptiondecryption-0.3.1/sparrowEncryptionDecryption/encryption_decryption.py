import asyncio
from functools import partial
from sparrowEncryptionDecryption.function.config import EASY_KEYS1
from sparrowEncryptionDecryption.function.config import EASY_KEYS2
from sparrowEncryptionDecryption.function.config import ORDER_KEYS1
from sparrowEncryptionDecryption.function.config import ORDER_KEYS2
from sparrowEncryptionDecryption.function.config import DICT_KEY1
from sparrowEncryptionDecryption.function.config import DICT_KEY2
from sparrowEncryptionDecryption.function.config import DICT_VALUE1
from sparrowEncryptionDecryption.function.config import DICT_VALUE2
from sparrowEncryptionDecryption.tools import SparrowInputDataNoneError
from sparrowEncryptionDecryption.function import SparrowDecryption, SparrowDecryptionAsync
from sparrowEncryptionDecryption.function import SparrowEncryption, SparrowEncryptionAsync


class SparrowEncryptionDecryption:
    def __init__(self, order_keys1=ORDER_KEYS1, order_keys2=ORDER_KEYS2, easy_keys1=EASY_KEYS1, easy_keys2=EASY_KEYS2,
                 dict_key1=DICT_KEY1, dict_key2=DICT_KEY2, dict_value1=DICT_VALUE1, dict_value2=DICT_VALUE2):
        self._encryption_ = SparrowEncryption(order_keys1, order_keys2, easy_keys1, easy_keys2, dict_key1,
                                              dict_key2, dict_value1, dict_value2)
        self._decryption_ = SparrowDecryption(order_keys1, order_keys2, easy_keys1, easy_keys2)

    def order_encryption(self, string: str, key: str, effective_duration: int = -1, is_compression: int = 2,
                         mode: int = 0, compression_type: str = None):
        """
        加密数据
        :param string: 需要被加密的数据
        :param key: 秘钥
        :param effective_duration: 秘钥过期时间，-1为永不过期
        :param is_compression: 默认为2，二次压缩压缩，1为一次压缩，0为不压缩
        :param mode: 加密模式，0为二进制加密，1为四进制加密
        :param compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
        :return: 返回被加密好的数据
        """
        if string == "" or string is None:
            raise SparrowInputDataNoneError
        if key == "" or key is None:
            raise SparrowInputDataNoneError
        return self._encryption_.order_encryption(string, key, effective_duration, is_compression, mode,
                                                  compression_type)

    def easy_encryption(self, string: str, key: str, mode: int = 0, compression_type: str = None):
        """
        加密数据
        :param string: 需要被加密的数据
        :param key: 秘钥
        :param mode: 加密模式，0为二进制加密，1为四进制加密
        :param compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
        :return: 返回被加密好的数据
        """
        if string == "" or string is None:
            raise SparrowInputDataNoneError
        if key == "" or key is None:
            raise SparrowInputDataNoneError
        return self._encryption_.easy_encryption(string, key, mode, compression_type)

    def random_encryption(self, string: str, effective_duration: int = -1, is_compression: int = 2,
                          mode: int = 0, compression_type: str = None):
        """
        加密数据
        :param string: 需要被加密的数据
        :param effective_duration: 秘钥过期时间，-1为永不过期
        :param is_compression: 默认为2，二次压缩压缩，1为一次压缩，0为不压缩
        :param mode: 加密模式，0为二进制加密，1为四进制加密
        :param compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
        :return: 返回被加密好的数据
        """
        if string == "" or string is None:
            raise SparrowInputDataNoneError
        return self._encryption_.random_encryption(string, effective_duration, is_compression, mode,
                                                   compression_type)

    def order_decryption(self, decompression: str, key: str, compression_type: str = None):
        """
        将被加密的数据解密
        :param decompression: 需要被解密的数据
        :param key: 秘钥
        :param compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
        :return: 返回被解密的数据或秘钥错误类型
        """
        if decompression == "" or decompression is None:
            raise SparrowInputDataNoneError
        if key == "" or key is None:
            raise SparrowInputDataNoneError
        return self._decryption_.order_decryption(decompression, key, compression_type)

    def easy_decryption(self, decompression: str, key: str, compression_type: str = None):
        """
        将被加密的数据解密
        :param decompression: 需要被解密的数据
        :param key: 秘钥
        :param compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
        :return: 返回被解密的数据或秘钥错误类型
        """
        if decompression == "" or decompression is None:
            raise SparrowInputDataNoneError
        if key == "" or key is None:
            raise SparrowInputDataNoneError
        return self._decryption_.easy_decryption(decompression, key, compression_type)

    def random_decryption(self, decompression: str, key: str, compression_type: str = None):
        """
        将被加密的数据解密
        :param decompression: 需要被解密的数据
        :param key: 秘钥
        :param compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
        :return: 返回被解密的数据或秘钥错误类型
        """
        if decompression == "" or decompression is None:
            raise SparrowInputDataNoneError
        if key == "" or key is None:
            raise SparrowInputDataNoneError
        return self._decryption_.random_decryption(decompression, key, compression_type)


class SparrowEncryptionDecryptionAsync(SparrowEncryptionDecryption):
    def __init__(self, order_keys1=ORDER_KEYS1, order_keys2=ORDER_KEYS2, easy_keys1=EASY_KEYS1, easy_keys2=EASY_KEYS2):
        super().__init__(order_keys1, order_keys2, easy_keys1, easy_keys2)
        self._encryption_ = SparrowEncryptionAsync(order_keys1, order_keys2, easy_keys1, easy_keys2)
        self._decryption_ = SparrowDecryptionAsync(order_keys1, order_keys2, easy_keys1, easy_keys2)

    async def order_encryption(self, string: str, key: str, effective_duration: int = -1, is_compression: int = 2,
                               mode: int = 0, compression_type: str = None):
        """
        异步加密数据。
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(
            super().order_encryption, string=string, key=key, effective_duration=effective_duration,
            is_compression=is_compression, mode=mode, compression_type=compression_type))

    async def easy_encryption(self, string: str, key: str, mode: int = 0, compression_type: str = None):
        """
        异步简单加密数据。
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(
            super().easy_encryption, string=string, key=key, mode=mode, compression_type=compression_type))

    async def random_encryption(self, string: str, effective_duration: int = -1, is_compression: int = 2,
                                mode: int = 0, compression_type: str = None):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(
            super().random_encryption, string=string, effective_duration=effective_duration,
            is_compression=is_compression, mode=mode, compression_type=compression_type
        ))

    async def order_decryption(self, decompression: str, key: str, compression_type: str = None):
        """
        异步解密数据。
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(
            super().order_decryption, decompression=decompression, key=key, compression_type=compression_type))

    async def easy_decryption(self, decompression: str, key: str, compression_type: str = None):
        """
        异步简单解密数据。
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(
            super().easy_decryption, decompression=decompression, key=key, compression_type=compression_type))

    async def random_decryption(self, decompression: str, key: bytes, compression_type: str = None):
        """
        异步秘钥加密数据
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(
            super().random_decryption, decompression=decompression, key=key
        ))
