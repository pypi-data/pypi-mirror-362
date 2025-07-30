import ast
import time
import asyncio
from functools import partial
from sparrowEncryptionDecryption.tools import SparrowKeyTypeError, SparrowLengthError, SparrowListTypeError
from sparrowEncryptionDecryption.tools import quaternary_to_binary
from sparrowEncryptionDecryption.function.config import EASY_KEYS1
from sparrowEncryptionDecryption.function.config import EASY_KEYS2
from sparrowEncryptionDecryption.function.config import SPLIT_CHAR
from sparrowEncryptionDecryption.function.config import ORDER_KEYS1
from sparrowEncryptionDecryption.function.config import ORDER_KEYS2
from sparrowEncryptionDecryption.tools import SparrowSecretKeyError
from sparrowEncryptionDecryption.tools import COMPRESSION_ALGORITHMS
from sparrowEncryptionDecryption.tools import SparrowSecretKeyOverdueError
from sparrowEncryptionDecryption.tools import SparrowDecompressionTypeError
from sparrowEncryptionDecryption.tools import SparrowBeDecryptionContentError
from sparrowEncryptionDecryption.tools import order_compression_and_decompression
from sparrowEncryptionDecryption.tools import order_compression_and_decompression2
from sparrowEncryptionDecryption.tools import binary_to_string, SparrowCompressTypeError


class SparrowDecryption:
    def __init__(self, order_keys1: list = None, order_keys2: list = None, easy_keys1: list = None,
                 easy_keys2: list = None):
        """
        初始化解密类
        :param order_keys1: order方法第一次解密秘钥
        :param order_keys2: order方法第二次解密秘钥
        :param easy_keys1: easy方法第一次解密秘钥
        :param easy_keys2: easy方法第二次解密秘钥
        """
        self._keys1_ = {}
        self._keys2_ = {}
        self._easy_keys1_ = {}
        self._easy_keys2_ = {}
        if order_keys1 is None:
            self._keys1_ = ORDER_KEYS1
        else:
            if type(order_keys1) is not list:
                raise SparrowListTypeError
            if len(order_keys1) != len(ORDER_KEYS1.keys()):
                raise SparrowLengthError("order_keys1加密数组长度错误，长度应为20")
            if len(set(order_keys1)) != len(ORDER_KEYS1.keys()):
                raise SparrowLengthError("order_keys1加密数组有重复值")
            for i in range(0, len(order_keys1)):
                self._keys1_[list(ORDER_KEYS1.keys())[i]] = order_keys1[i]
        if order_keys2 is None:
            self._keys2_ = ORDER_KEYS2
        else:
            if type(order_keys2) is not list:
                raise SparrowListTypeError
            if len(order_keys2) != len(ORDER_KEYS2.keys()):
                raise SparrowLengthError("order_keys2加密数组长度错误，长度应为400")
            if len(set(order_keys2)) != len(ORDER_KEYS2.keys()):
                raise SparrowLengthError("order_keys2加密数组有重复值")
            if (len(set(order_keys1)) + len(set(order_keys2))) != (len(ORDER_KEYS1.keys()) + len(ORDER_KEYS2.keys())):
                raise SparrowLengthError("order_keys1和order_keys2存在重复值")
            okl = list(self._keys1_.values())
            ok = []
            for i in range(len(okl)):
                for j in range(len(okl)):
                    ok.append(okl[i] + okl[j])
            for i in range(0, len(order_keys2)):
                self._keys2_[ok[i]] = order_keys2[i]
        if easy_keys1 is None:
            self._easy_keys1_ = EASY_KEYS1
        else:
            if type(easy_keys1) is not list:
                raise SparrowListTypeError
            if len(easy_keys1) != len(EASY_KEYS1.keys()):
                raise SparrowLengthError("easy_keys1加密数组长度错误，长度应为16")
            if len(set(easy_keys1)) != len(EASY_KEYS1.keys()):
                raise SparrowLengthError("easy_keys1加密数组有重复值")
            for i in range(0, len(easy_keys1)):
                self._easy_keys1_[list(EASY_KEYS1.keys())[i]] = easy_keys1[i]
        if easy_keys2 is None:
            self._easy_keys2_ = EASY_KEYS2
        else:
            if type(easy_keys2) is not list:
                raise SparrowListTypeError
            if len(easy_keys2) != len(EASY_KEYS2.keys()):
                raise SparrowLengthError("easy_keys2加密数组长度错误，长度应为256")
            if len(set(easy_keys2)) != len(EASY_KEYS2.keys()):
                raise SparrowLengthError("easy_keys2加密数组有重复值")
            if (len(set(easy_keys1)) + len(set(easy_keys2))) != (len(EASY_KEYS1.keys()) + len(EASY_KEYS2.keys())):
                raise SparrowLengthError("easy_keys1和easy_keys2存在重复值")
            ekl = list(self._easy_keys1_.values())
            ek = []
            for i in range(len(ekl)):
                for j in range(len(ekl)):
                    ek.append(ekl[i] + ekl[j])
            for i in range(0, len(easy_keys2)):
                self._keys2_[ek[i]] = easy_keys2[i]

    def order_decryption(self, decompression: str, keyword: str, compression_type: str = None):
        """
        将被加密的数据解密
        :param decompression: 需要被解密的数据
        :param keyword: 秘钥
        :param compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
        :return: 返回被解密的数据或秘钥错误类型
        """
        if compression_type is None:
            if type(decompression) is not str:
                raise SparrowDecompressionTypeError
        else:
            try:
                decompression = COMPRESSION_ALGORITHMS[compression_type]['decompress'](decompression)
            except Exception:
                raise SparrowCompressTypeError
        if type(keyword) is not str:
            raise SparrowKeyTypeError
        if "三" in decompression:
            decompression = decompression.replace("三", "")
            if "零" in decompression:
                string, effective_duration, key, encryption_time = decompression.replace("零", '').split(SPLIT_CHAR)
            elif "一" in decompression:
                string, effective_duration, key, encryption_time = decompression.replace("一", '').split(SPLIT_CHAR)
                string = order_compression_and_decompression(False, string, self._keys1_)
                key = order_compression_and_decompression(False, key, self._keys1_)
                effective_duration = order_compression_and_decompression(False, effective_duration, self._keys1_)
                encryption_time = order_compression_and_decompression(False, encryption_time, self._keys1_)
            elif "二" in decompression:
                string, effective_duration, key, encryption_time = decompression.replace("二", '').split(SPLIT_CHAR)
                string = order_compression_and_decompression(
                    False, order_compression_and_decompression2(False, string, self._keys2_), self._keys1_)
                key = order_compression_and_decompression(
                    False, order_compression_and_decompression2(False, key, self._keys2_), self._keys1_)
                effective_duration = order_compression_and_decompression(
                    False, order_compression_and_decompression2(False, effective_duration, self._keys2_), self._keys1_)
                encryption_time = order_compression_and_decompression(
                    False, order_compression_and_decompression2(False, encryption_time, self._keys2_), self._keys1_)
            else:
                raise SparrowBeDecryptionContentError

            string = binary_to_string(
                string.replace("A", "00").replace("T", "01").replace("C", "11")
                .replace("G", "10"))
            key = binary_to_string(
                key.replace("A", "00").replace("T", "01").replace("C", "11")
                .replace("G", "10"))
            effective_duration = binary_to_string(
                effective_duration.replace("A", "00").replace("T", "01").replace("C", "11")
                .replace("G", "10"))
            encryption_time = binary_to_string(
                encryption_time.replace("A", "00").replace("T", "01").replace("C", "11")
                .replace("G", "10"))
        elif "四" in decompression:
            decompression = decompression.replace("四", "")
            if "零" in decompression:
                string, effective_duration, key, encryption_time = decompression.replace("零", '').split(SPLIT_CHAR)
            if "一" in decompression:
                string, effective_duration, key, encryption_time = decompression.replace("一", '').split(SPLIT_CHAR)
                key = order_compression_and_decompression(False, key, self._keys1_)
                string = order_compression_and_decompression(False, string, self._keys1_)
                effective_duration = order_compression_and_decompression(False, effective_duration, self._keys1_)
                encryption_time = order_compression_and_decompression(False, encryption_time, self._keys1_)
            elif "二" in decompression:
                string, effective_duration, key, encryption_time = decompression.replace("二", '').split(SPLIT_CHAR)
                string = order_compression_and_decompression(
                    False, order_compression_and_decompression2(False, string, self._keys2_), self._keys1_)
                key = order_compression_and_decompression(
                    False, order_compression_and_decompression2(False, key, self._keys2_), self._keys1_)
                effective_duration = order_compression_and_decompression(
                    False, order_compression_and_decompression2(False, effective_duration, self._keys2_), self._keys1_)
                encryption_time = order_compression_and_decompression(
                    False, order_compression_and_decompression2(False, encryption_time, self._keys2_), self._keys1_)
            else:
                raise SparrowBeDecryptionContentError
            string = binary_to_string(quaternary_to_binary(
                string.replace("A", "0").replace("T", "1").replace("C", "2").replace("G", "3")))
            key = binary_to_string(quaternary_to_binary(
                key.replace("A", "0").replace("T", "1").replace("C", "2").replace("G", "3")))
            effective_duration = binary_to_string(quaternary_to_binary(
                effective_duration.replace("A", "0").replace("T", "1").replace("C", "2").replace("G", "3")))
            encryption_time = binary_to_string(quaternary_to_binary(
                encryption_time.replace("A", "0").replace("T", "1").replace("C", "2").replace("G", "3")))
        else:
            raise SparrowBeDecryptionContentError
        if compression_type is not None:
            string_data = ast.literal_eval(string)
        else:
            string_data = string
        if effective_duration != "-1":
            effective_duration = int(time.time() - float(encryption_time))
            if key == keyword:
                if effective_duration < int(effective_duration):
                    return string_data
                else:
                    raise SparrowSecretKeyOverdueError
            else:
                raise SparrowSecretKeyError
        else:
            if key == keyword:
                return string_data
            else:
                raise SparrowSecretKeyError

    def easy_decryption(self, decompression: str, key: str, compression_type: str = None):
        """
        将被加密的数据解密
        :param decompression: 需要被解密的数据
        :param key: 秘钥
        :return: 返回被解密的数据或秘钥错误类型
        :param compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
        """
        if compression_type is None:
            if type(decompression) is not str:
                raise SparrowDecompressionTypeError
        else:
            try:
                decompression = COMPRESSION_ALGORITHMS[compression_type]['decompress'](decompression)
            except Exception:
                raise SparrowCompressTypeError
        if type(key) is not str:
            raise SparrowKeyTypeError
        decryption_list = decompression.split(SPLIT_CHAR)
        decryption_key_part = decryption_list[0] + decryption_list[4]
        decryption_key_group = decryption_list[2]
        encryption_mode = decryption_list[5]
        decryption_keys = {}
        if decryption_key_part == decryption_key_group:
            if encryption_mode == "四":
                for k, v in self._easy_keys2_.items():
                    decryption_keys[v] = k
                decryption_key = ""
                for i in decryption_key_group:
                    decryption_key += decryption_keys[i]
                decryption_key = binary_to_string(quaternary_to_binary(decryption_key))
                if decryption_key == key:
                    try:
                        encryption_data = decryption_list[1] + decryption_list[3]
                        decryption_data = ""
                        for i in encryption_data:
                            decryption_data += decryption_keys[i]
                        return binary_to_string(quaternary_to_binary(decryption_data))
                    except Exception:
                        raise SparrowBeDecryptionContentError
                else:
                    raise SparrowSecretKeyError
            elif encryption_mode == "二":
                for k, v in self._easy_keys1_.items():
                    decryption_keys[v] = k
                decryption_key = ""
                for i in decryption_key_group:
                    decryption_key += decryption_keys[i]
                decryption_key = binary_to_string(decryption_key)
                if decryption_key == key:
                    try:
                        encryption_data = decryption_list[1] + decryption_list[3]
                        decryption_data = ""
                        for i in encryption_data:
                            decryption_data += decryption_keys[i]
                        return binary_to_string(decryption_data)
                    except Exception:
                        raise SparrowBeDecryptionContentError
                else:
                    raise SparrowSecretKeyError
            else:
                raise SparrowBeDecryptionContentError
        else:
            raise SparrowBeDecryptionContentError("加密内容中秘钥数据已被修改，程序不解密")

    @staticmethod
    def random_decryption(decompression: str, key: bytes, compression_type: str = None):
        """
        将被加密的数据解密
        :param decompression: 需要被解密的数据
        :param key: 秘钥
        :param compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
        :return: 返回被解密的数据或秘钥错误类型
        """
        if compression_type is None:
            if type(decompression) is not str:
                raise SparrowDecompressionTypeError
        else:
            try:
                decompression = COMPRESSION_ALGORITHMS[compression_type]['decompress'](decompression)
            except Exception:
                raise SparrowCompressTypeError
        if type(key) is not bytes:
            raise SparrowKeyTypeError("秘钥类型错误，输入类型为二进制数据")
        keys = eval(COMPRESSION_ALGORITHMS["zlib"]['decompress'](key))
        keys1 = keys.get("keys1")
        keys2 = keys.get("keys2")
        mode = None
        if "三" not in decompression and "四" not in decompression:
            raise SparrowBeDecryptionContentError
        if "四" in decompression:
            mode = True
            decompression = decompression.replace("四", "")
        if "三" in decompression:
            mode = False
            decompression = decompression.replace("三", "")
        try:
            if "零" in decompression:
                decompression = decompression.replace("零", '')
                string, effective_duration, encryption_time = decompression.split(SPLIT_CHAR)
            elif "一" in decompression:
                decompression = decompression.replace("一", '')
                string, effective_duration, encryption_time = decompression.split(SPLIT_CHAR)
                string = order_compression_and_decompression(False, string, keys1)
                effective_duration = order_compression_and_decompression(False, effective_duration, keys1)
                encryption_time = order_compression_and_decompression(False, encryption_time, keys1)
            elif "二" in decompression:
                decompression = decompression.replace("二", '')
                string, effective_duration, encryption_time = decompression.split(SPLIT_CHAR)
                string = order_compression_and_decompression(
                    False, order_compression_and_decompression2(False, string, keys2), keys1)
                effective_duration = order_compression_and_decompression(
                    False, order_compression_and_decompression2(False, effective_duration, keys2), keys1)
                encryption_time = order_compression_and_decompression(
                    False, order_compression_and_decompression2(False, encryption_time, keys2), keys1)
            else:
                raise SparrowBeDecryptionContentError
            if mode:
                string = binary_to_string(quaternary_to_binary(
                    string.replace("A", "0").replace("T", "1").replace("C", "2").replace("G", "3")))
                effective_duration = binary_to_string(quaternary_to_binary(
                    effective_duration.replace("A", "0").replace("T", "1").replace("C", "2").replace("G", "3")))
                encryption_time = binary_to_string(quaternary_to_binary(
                    encryption_time.replace("A", "0").replace("T", "1").replace("C", "2").replace("G", "3")))
            else:
                string = binary_to_string(
                    string.replace("A", "00").replace("T", "01").replace("C", "11")
                    .replace("G", "10"))
                effective_duration = binary_to_string(
                    effective_duration.replace("A", "00").replace("T", "01").replace("C", "11")
                    .replace("G", "10"))
                encryption_time = binary_to_string(
                    encryption_time.replace("A", "00").replace("T", "01").replace("C", "11")
                    .replace("G", "10"))
        except Exception:
            raise SparrowBeDecryptionContentError
        if compression_type is not None:
            string_data = ast.literal_eval(string)
        else:
            string_data = string
        if effective_duration != "-1":
            effective_duration = int(time.time() - float(encryption_time))
            if effective_duration < int(effective_duration):
                return string_data
            else:
                raise SparrowSecretKeyOverdueError
        else:
            return string_data

    @staticmethod
    def full_random_decryption(decompression: str, key: bytes, compression_type: str = None):
        """
        将被加密的数据解密
        :param decompression: 需要被解密的数据
        :param key: 秘钥
        :param compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
        :return: 返回被解密的数据或秘钥错误类型
        """
        if compression_type is None:
            if type(decompression) is not str:
                raise SparrowDecompressionTypeError
        else:
            try:
                decompression = COMPRESSION_ALGORITHMS[compression_type]['decompress'](decompression)
            except Exception:
                raise SparrowCompressTypeError
        if type(key) is not bytes:
            raise SparrowKeyTypeError("秘钥类型错误，输入类型为二进制数据")
        keys = eval(COMPRESSION_ALGORITHMS["zlib"]['decompress'](key))
        keys1 = keys.get("keys1")
        keys2 = keys.get("keys2")
        split_char = keys.get("split_char")
        zero = keys.get("zero")
        one = keys.get("one")
        twe = keys.get("twe")
        three = keys.get("three")
        four = keys.get("four")
        a = keys.get("a")
        t = keys.get("t")
        c = keys.get("c")
        g = keys.get("g")
        mode = None
        if three not in decompression and four not in decompression:
            raise SparrowBeDecryptionContentError
        if four in decompression:
            mode = True
            decompression = decompression.replace(four, "")
        if three in decompression:
            mode = False
            decompression = decompression.replace(three, "")
        try:
            if zero in decompression:
                decompression = decompression.replace(zero, '')
                string, effective_duration, encryption_time = decompression.split(split_char)
            elif one in decompression:
                decompression = decompression.replace(one, '')
                string, effective_duration, encryption_time = decompression.split(split_char)
                string = order_compression_and_decompression(False, string, keys1)
                effective_duration = order_compression_and_decompression(False, string, keys1)
                encryption_time = order_compression_and_decompression(False, string, keys1)
            elif twe in decompression:
                decompression = decompression.replace(twe, '')
                string, effective_duration, encryption_time = decompression.split(split_char)
                string = order_compression_and_decompression(
                    False, order_compression_and_decompression2(False, string, keys2), keys1)
                effective_duration = order_compression_and_decompression(
                    False, order_compression_and_decompression2(False, effective_duration, keys2), keys1)
                encryption_time = order_compression_and_decompression(
                    False, order_compression_and_decompression2(False, encryption_time, keys2), keys1)
            else:
                raise SparrowBeDecryptionContentError
            if mode:
                string = binary_to_string(
                    quaternary_to_binary(string.replace(a, "0").replace(t, "1").replace(c, "2").replace(g, "3")))
                effective_duration = binary_to_string(
                    quaternary_to_binary(
                        effective_duration.replace(a, "0").replace(t, "1").replace(c, "2").replace(g, "3")))
                encryption_time = binary_to_string(
                    quaternary_to_binary(
                        encryption_time.replace(a, "0").replace(t, "1").replace(c, "2").replace(g, "3")))
            else:
                string = binary_to_string(
                    string.replace(a, "00").replace(t, "01").replace(c, "11").replace(g, "10"))
                effective_duration = binary_to_string(
                    effective_duration.replace(a, "00").replace(t, "01").replace(c, "11").replace(g, "10"))
                encryption_time = binary_to_string(
                    encryption_time.replace(a, "00").replace(t, "01").replace(c, "11").replace(g, "10"))
        except Exception:
            raise SparrowBeDecryptionContentError
        if compression_type is not None:
            string_data = ast.literal_eval(string)
        else:
            string_data = string
        if effective_duration != "-1":
            effective_duration = int(time.time() - float(encryption_time))
            if effective_duration < int(effective_duration):
                return string_data
            else:
                raise SparrowSecretKeyOverdueError
        else:
            return string_data


class SparrowDecryptionAsync(SparrowDecryption):
    def __init__(self, order_keys1: list = None, order_keys2: list = None, easy_keys1: list = None,
                 easy_keys2: list = None):
        super().__init__(order_keys1, order_keys2, easy_keys1, easy_keys2)

    async def order_decryption(self, decompression: str, key: str, compression_type: str = None):
        """
        异步解密数据。
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(
            super().order_decryption, decompression=decompression, key=key
        ))

    async def easy_decryption(self, decompression: str, key: str, compression_type: str = None):
        """
        异步简单解密数据。
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(
            super().easy_decryption, decompression=decompression, key=key
        ))

    async def random_decryption(self, decompression: str, key: bytes, compression_type: str = None):
        """
        异步秘钥加密数据
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(
            super().random_decryption, decompression=decompression, key=key
        ))

    async def full_random_decryption(self, decompression: str, key: bytes, compression_type: str = None):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(
            super().full_random_decryption, decompression=decompression, key=key, compression_type=compression_type
        ))
