import time
import asyncio
from functools import partial
from sparrowEncryptionDecryption.tools import split_pairwise
from sparrowEncryptionDecryption.tools import string_to_binary
from sparrowEncryptionDecryption.tools import SparrowKeyTypeError
from sparrowEncryptionDecryption.function.config import EASY_KEYS1
from sparrowEncryptionDecryption.function.config import EASY_KEYS2
from sparrowEncryptionDecryption.tools import binary_to_quaternary
from sparrowEncryptionDecryption.function.config import SPLIT_CHAR
from sparrowEncryptionDecryption.function.config import ORDER_KEYS1
from sparrowEncryptionDecryption.function.config import ORDER_KEYS2
from sparrowEncryptionDecryption.function.config import DICT_KEY1
from sparrowEncryptionDecryption.function.config import DICT_KEY2
from sparrowEncryptionDecryption.function.config import DICT_VALUE1
from sparrowEncryptionDecryption.function.config import DICT_VALUE2
from sparrowEncryptionDecryption.tools import split_double_pairwise
from sparrowEncryptionDecryption.tools import SparrowModeRangeError
from sparrowEncryptionDecryption.tools import COMPRESSION_ALGORITHMS
from sparrowEncryptionDecryption.tools import SparrowStringTypeError
from sparrowEncryptionDecryption.tools import SparrowCompressionRangeError
from sparrowEncryptionDecryption.tools import order_compression_and_decompression
from sparrowEncryptionDecryption.tools import order_compression_and_decompression2
from sparrowEncryptionDecryption.tools.tools import get_random_key


class SparrowEncryption:
    def __init__(self, order_keys1=ORDER_KEYS1, order_keys2=ORDER_KEYS2, easy_keys1=EASY_KEYS1, easy_keys2=EASY_KEYS2,
                 dict_key1=DICT_KEY1, dict_key2=DICT_KEY2, dict_value1=DICT_VALUE1, dict_value2=DICT_VALUE2):
        """
        初始化加密类
        :param order_keys1: order方法第一次加密秘钥
        :param order_keys2: order方法第二次加密秘钥
        :param easy_keys1: easy方法第一次加密秘钥
        :param easy_keys2: easy方法第二次加密秘钥
        """
        self._keys1_ = order_keys1
        self._keys2_ = order_keys2
        self._easy_keys1_ = easy_keys1
        self._easy_keys2_ = easy_keys2
        self._t_dict_key1_ = dict_key1
        self._t_dict_key2_ = dict_key2
        self._t_dict_value1_ = dict_value1
        self._t_dict_value2_ = dict_value2

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
        if type(key) is not str:
            raise SparrowKeyTypeError
        if type(string) is not str:
            raise SparrowStringTypeError
        if str(is_compression) not in ['0', '1', '2']:
            raise SparrowCompressionRangeError
        if str(mode) not in ['0', '1']:
            raise SparrowModeRangeError
        compression = None
        if mode == 0:
            binary_list = split_pairwise(
                str(string_to_binary(
                    string + SPLIT_CHAR + str(effective_duration) + SPLIT_CHAR + key + SPLIT_CHAR + str(time.time()))))
            binary = ""
            for i in binary_list:
                if i == "00":
                    binary += "A"
                elif i == "01":
                    binary += "T"
                elif i == "11":
                    binary += "C"
                elif i == "10":
                    binary += "G"
            if is_compression == 0:
                return binary + "零三"
            if is_compression == 1:
                compression = order_compression_and_decompression(True, binary, self._keys1_) + "一三"
            if is_compression == 2:
                compression = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, binary.replace("一", ''), self._keys1_), self._keys2_) + "二三"
        elif mode == 1:
            binary = string_to_binary(
                string + SPLIT_CHAR + str(effective_duration) + SPLIT_CHAR + key + SPLIT_CHAR + str(time.time()))
            quaternary = (str(binary_to_quaternary(binary)).replace("0", "A")
                          .replace("1", "T").replace("2", "C").replace("3", "G"))
            if is_compression == 0:
                return quaternary + "零四"
            if is_compression == 1:
                compression = order_compression_and_decompression(True, quaternary, self._keys1_) + "一四"
            if is_compression == 2:
                compression = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, quaternary.replace("一", ''), self._keys1_), self._keys2_) + "二四"
        if compression_type is None:
            return compression
        else:
            return COMPRESSION_ALGORITHMS[compression_type]['compress'](compression)

    def easy_encryption(self, string: str, key: str, mode: int = 0, compression_type: str = None):
        """
        加密数据
        :param compression_type:
        :param string: 需要被加密的数据
        :param key: 秘钥
        :param mode: 加密模式，0为二进制加密，1为四进制加密
        :return: 返回被加密好的数据
        :param compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
        """
        if type(key) is not str:
            raise SparrowKeyTypeError
        if type(string) is not str:
            raise SparrowStringTypeError
        if str(mode) not in ['0', '1']:
            raise SparrowModeRangeError
        encryption_data = ""
        encryption_key_data = ""
        if str(mode) == "0":
            split_data = split_double_pairwise(str(string_to_binary(string)))
            for i in split_data:
                encryption_data += self._easy_keys1_[i]
            split_key_data = split_double_pairwise(str(string_to_binary(key)))
            for i in split_key_data:
                encryption_key_data += self._easy_keys1_[i]
        elif str(mode) == "1":
            split_data = split_double_pairwise(str(binary_to_quaternary(str(string_to_binary(string)))))
            for i in split_data:
                encryption_data += self._easy_keys2_[i]
            split_key_data = split_double_pairwise(str(binary_to_quaternary(str(string_to_binary(key)))))
            for i in split_key_data:
                encryption_key_data += self._easy_keys2_[i]
        key_a = encryption_key_data[0: int(len(encryption_key_data) / 2)]
        key_b = encryption_key_data[int(len(encryption_key_data) / 2)::]
        data_a = encryption_data[0: int(len(encryption_data) / 2)]
        data_b = encryption_data[int(len(encryption_data) / 2)::]
        if str(mode) == "0":
            compression = key_a + SPLIT_CHAR + data_a + SPLIT_CHAR + encryption_key_data + SPLIT_CHAR + data_b + SPLIT_CHAR + key_b + SPLIT_CHAR + "二"
        elif str(mode) == "1":
            compression = key_a + SPLIT_CHAR + data_a + SPLIT_CHAR + encryption_key_data + SPLIT_CHAR + data_b + SPLIT_CHAR + key_b + SPLIT_CHAR + "四"
        else:
            raise SparrowModeRangeError
        if compression_type is None:
            return compression
        else:
            return COMPRESSION_ALGORITHMS[compression_type]['compress'](compression)

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
        if type(string) is not str:
            raise SparrowStringTypeError
        if str(is_compression) not in ['0', '1', '2']:
            raise SparrowCompressionRangeError
        if str(mode) not in ['0', '1']:
            raise SparrowModeRangeError
        keys1 = {}
        keys2 = {}
        if is_compression == 2:
            keys1 = get_random_key(self._t_dict_key1_, self._t_dict_value1_)
            keys2 = get_random_key(self._t_dict_key2_, self._t_dict_value2_)
        elif is_compression == 1:
            keys1 = get_random_key(self._t_dict_key1_, self._t_dict_value1_)
        compression = None
        if mode == 0:
            binary_list = split_pairwise(
                str(string_to_binary(
                    string + SPLIT_CHAR + str(effective_duration) + SPLIT_CHAR + str(time.time()))))
            binary = ""
            print(keys1)
            for i in binary_list:
                if i == "00":
                    binary += "A"
                elif i == "01":
                    binary += "T"
                elif i == "11":
                    binary += "C"
                elif i == "10":
                    binary += "G"
            if is_compression == 0:
                return binary + "零三", COMPRESSION_ALGORITHMS["zlib"]['compress'](
                    str({"keys1": keys1, "keys2": keys2}))
            if is_compression == 1:
                compression = order_compression_and_decompression(True, binary, keys1) + "一三"
            if is_compression == 2:
                compression = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, binary.replace("一", ''), keys1), keys2) + "二三"
        elif mode == 1:
            binary = string_to_binary(
                string + SPLIT_CHAR + str(effective_duration) + SPLIT_CHAR + str(time.time()))
            quaternary = (str(binary_to_quaternary(binary)).replace("0", "A")
                          .replace("1", "T").replace("2", "C").replace("3", "G"))
            if is_compression == 0:
                return quaternary + "零四", COMPRESSION_ALGORITHMS["zlib"]['compress'](
                    str({"keys1": keys1, "keys2": keys2}))
            if is_compression == 1:
                compression = order_compression_and_decompression(True, quaternary, keys1) + "一四"
            if is_compression == 2:
                compression = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, quaternary.replace("一", ''), keys1), keys2) + "二四"
        if compression_type is None:
            return compression, COMPRESSION_ALGORITHMS["zlib"]['compress'](
                str({"keys1": keys1, "keys2": keys2}))
        else:
            return COMPRESSION_ALGORITHMS[compression_type]['compress'](compression), COMPRESSION_ALGORITHMS["zlib"][
                'compress'](str({"keys1": keys1, "keys2": keys2}))


class SparrowEncryptionAsync(SparrowEncryption):
    def __init__(self, order_keys1=ORDER_KEYS1, order_keys2=ORDER_KEYS2, easy_keys1=EASY_KEYS1, easy_keys2=EASY_KEYS2):
        super().__init__(order_keys1, order_keys2, easy_keys1, easy_keys2)

    async def order_encryption(self, string: str, key: str, effective_duration: int = -1, is_compression: int = 2,
                               mode: int = 0, compression_type: str = None):
        """
        异步加密数据。
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(
            super().order_encryption, string=string, key=key, effective_duration=effective_duration,
            is_compression=is_compression, mode=mode
        ))

    async def easy_encryption(self, string: str, key: str, mode: int = 0, compression_type: str = None):
        """
        异步简单加密数据。
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(
            super().easy_encryption, string=string, key=key, mode=mode
        ))

    async def random_encryption(self, string: str, effective_duration: int = -1, is_compression: int = 2,
                                mode: int = 0, compression_type: str = None):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(
            super().random_encryption, string=string, effective_duration=effective_duration,
            is_compression=is_compression, mode=mode, compression_type=compression_type
        ))
