import time
import asyncio
from functools import partial
from sparrowEncryptionDecryption.tools import split_pairwise, SparrowListTypeError, SparrowLengthError
from sparrowEncryptionDecryption.tools import string_to_binary, choice_key
from sparrowEncryptionDecryption.tools import SparrowKeyTypeError
from sparrowEncryptionDecryption.function.config import EASY_KEYS1, RANDOM_KEY
from sparrowEncryptionDecryption.function.config import EASY_KEYS2
from sparrowEncryptionDecryption.tools import binary_to_quaternary
from sparrowEncryptionDecryption.function.config import SPLIT_CHAR
from sparrowEncryptionDecryption.function.config import ORDER_KEYS1
from sparrowEncryptionDecryption.function.config import ORDER_KEYS2
from sparrowEncryptionDecryption.function.config import DICT_KEY1
from sparrowEncryptionDecryption.function.config import DICT_KEY2
from sparrowEncryptionDecryption.function.config import DICT_VALUE1
from sparrowEncryptionDecryption.function.config import DICT_VALUE2
from sparrowEncryptionDecryption.function.config import RANDOM_KEY
from sparrowEncryptionDecryption.tools import split_double_pairwise
from sparrowEncryptionDecryption.tools import SparrowModeRangeError
from sparrowEncryptionDecryption.tools import COMPRESSION_ALGORITHMS
from sparrowEncryptionDecryption.tools import SparrowStringTypeError
from sparrowEncryptionDecryption.tools import SparrowCompressionRangeError
from sparrowEncryptionDecryption.tools import order_compression_and_decompression
from sparrowEncryptionDecryption.tools import order_compression_and_decompression2
from sparrowEncryptionDecryption.tools.tools import get_random_key


class SparrowEncryption:
    def __init__(self, order_keys1: list = None, order_keys2: list = None, easy_keys1: list = None,
                 easy_keys2: list = None):
        """
        初始化加密类
        :param order_keys1: order方法第一次加密秘钥
        :param order_keys2: order方法第二次加密秘钥
        :param easy_keys1: easy方法第一次加密秘钥
        :param easy_keys2: easy方法第二次加密秘钥
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
        self._t_dict_key1_ = DICT_KEY1
        self._t_dict_key2_ = DICT_KEY2
        self._t_dict_value1_ = DICT_VALUE1
        self._t_dict_value2_ = DICT_VALUE2
        self._full_key_ = RANDOM_KEY

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
            string = split_pairwise(str(string_to_binary(string)))
            key = split_pairwise(str(string_to_binary(key)))
            effective_duration = split_pairwise(str(string_to_binary(str(effective_duration))))
            encryption_time = split_pairwise(str(string_to_binary(str(time.time()))))
            mapping = {"00": "A", "01": "T", "11": "C", "10": "G"}
            string_binary = ''.join(mapping[i] for i in string)
            key_binary = ''.join(mapping[i] for i in key)
            effective_duration_binary = ''.join(mapping[i] for i in effective_duration)
            encryption_time_binary = ''.join(mapping[i] for i in encryption_time)
            if is_compression == 0:
                return string_binary + SPLIT_CHAR + effective_duration_binary + SPLIT_CHAR + key_binary + SPLIT_CHAR + encryption_time_binary + "零三"
            if is_compression == 1:
                string_binary = order_compression_and_decompression(True, string_binary, self._keys1_)
                key_binary = order_compression_and_decompression(True, key_binary, self._keys1_)
                effective_duration_binary = order_compression_and_decompression(True, effective_duration_binary,
                                                                                self._keys1_)
                encryption_time_binary = order_compression_and_decompression(True, encryption_time_binary, self._keys1_)
                compression = string_binary + SPLIT_CHAR + effective_duration_binary + SPLIT_CHAR + key_binary + SPLIT_CHAR + encryption_time_binary + "一三"
            if is_compression == 2:
                string_binary = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, string_binary.replace("一", ''), self._keys1_), self._keys2_)
                key_binary = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, key_binary.replace("一", ''), self._keys1_), self._keys2_)
                effective_duration_binary = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, effective_duration_binary.replace("一", ''), self._keys1_), self._keys2_)
                encryption_time_binary = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, encryption_time_binary.replace("一", ''), self._keys1_), self._keys2_)
                compression = string_binary + SPLIT_CHAR + effective_duration_binary + SPLIT_CHAR + key_binary + SPLIT_CHAR + encryption_time_binary + "二三"
        elif mode == 1:
            string = str(binary_to_quaternary(string_to_binary(string)))
            key = str(binary_to_quaternary(string_to_binary(key)))
            effective_duration = str(binary_to_quaternary(string_to_binary(str(effective_duration))))
            encryption_time = str(binary_to_quaternary(string_to_binary(str(time.time()))))
            mapping = {"0": "A", "1": "T", "2": "C", "3": "G"}
            string_quaternary = ''.join(mapping[i] for i in string)
            key_quaternary = ''.join(mapping[i] for i in key)
            effective_duration_quaternary = ''.join(mapping[i] for i in effective_duration)
            encryption_time_quaternary = ''.join(mapping[i] for i in encryption_time)
            if is_compression == 0:
                return string_quaternary + SPLIT_CHAR + effective_duration_quaternary + SPLIT_CHAR + key + SPLIT_CHAR + encryption_time_quaternary + "零四"
            if is_compression == 1:
                string_quaternary = order_compression_and_decompression(True, string_quaternary, self._keys1_)
                key_quaternary = order_compression_and_decompression(True, key_quaternary, self._keys1_)
                effective_duration_quaternary = order_compression_and_decompression(True, effective_duration_quaternary,
                                                                                    self._keys1_)
                encryption_time_quaternary = order_compression_and_decompression(True, encryption_time_quaternary,
                                                                                 self._keys1_)
                compression = string_quaternary + SPLIT_CHAR + effective_duration_quaternary + SPLIT_CHAR + key_quaternary + SPLIT_CHAR + encryption_time_quaternary + "一四"
            if is_compression == 2:
                string_quaternary = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, string_quaternary.replace("一", ''), self._keys1_), self._keys2_)
                key_quaternary = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, key_quaternary.replace("一", ''), self._keys1_), self._keys2_)
                effective_duration_quaternary = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, effective_duration_quaternary.replace("一", ''), self._keys1_), self._keys2_)
                encryption_time_quaternary = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, encryption_time_quaternary.replace("一", ''), self._keys1_), self._keys2_)
                compression = string_quaternary + SPLIT_CHAR + effective_duration_quaternary + SPLIT_CHAR + key_quaternary + SPLIT_CHAR + encryption_time_quaternary + "二四"
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
            string = split_pairwise(str(string_to_binary(string)))
            effective_duration = split_pairwise(str(string_to_binary(str(effective_duration))))
            encryption_time = split_pairwise(str(string_to_binary(str(time.time()))))
            mapping = {"00": "A", "01": "T", "11": "C", "10": "G"}
            string_binary = ''.join(mapping[i] for i in string)
            effective_duration_binary = ''.join(mapping[i] for i in effective_duration)
            encryption_time_binary = ''.join(mapping[i] for i in encryption_time)
            if is_compression == 0:
                return (
                    string_binary + SPLIT_CHAR + effective_duration_binary + SPLIT_CHAR + encryption_time_binary + "零三",
                    COMPRESSION_ALGORITHMS["zlib"]['compress'](str({"keys1": keys1, "keys2": keys2})))
            if is_compression == 1:
                string_binary = order_compression_and_decompression(True, string_binary, keys1)
                effective_duration_binary = order_compression_and_decompression(True, effective_duration_binary,
                                                                                keys1)
                encryption_time_binary = order_compression_and_decompression(True, encryption_time_binary, keys1)
                compression = string_binary + SPLIT_CHAR + effective_duration_binary + SPLIT_CHAR + encryption_time_binary + "一三"
            if is_compression == 2:
                string_binary = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, string_binary.replace("一", ''), keys1), keys2)
                effective_duration_binary = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, effective_duration_binary.replace("一", ''), keys1), keys2)
                encryption_time_binary = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, encryption_time_binary.replace("一", ''), keys1), keys2)
                compression = string_binary + SPLIT_CHAR + effective_duration_binary + SPLIT_CHAR + encryption_time_binary + "二三"
        elif mode == 1:
            string = str(binary_to_quaternary(string_to_binary(string)))
            effective_duration = str(binary_to_quaternary(string_to_binary(str(effective_duration))))
            encryption_time = str(binary_to_quaternary(string_to_binary(str(time.time()))))
            mapping = {"0": "A", "1": "T", "2": "C", "3": "G"}
            string_quaternary = ''.join(mapping[i] for i in string)
            effective_duration_quaternary = ''.join(mapping[i] for i in effective_duration)
            encryption_time_quaternary = ''.join(mapping[i] for i in encryption_time)
            if is_compression == 0:
                return (
                    string_quaternary + SPLIT_CHAR + effective_duration_quaternary + SPLIT_CHAR + encryption_time_quaternary + "零四",
                    COMPRESSION_ALGORITHMS["zlib"]['compress'](str({"keys1": keys1, "keys2": keys2}))
                )
            if is_compression == 1:
                string_quaternary = order_compression_and_decompression(True, string_quaternary, keys1)
                effective_duration_quaternary = order_compression_and_decompression(True, effective_duration_quaternary,
                                                                                    keys1)
                encryption_time_quaternary = order_compression_and_decompression(True, encryption_time_quaternary,
                                                                                 keys1)
                compression = string_quaternary + SPLIT_CHAR + effective_duration_quaternary + SPLIT_CHAR + encryption_time_quaternary + "一四"
            if is_compression == 2:
                string_quaternary = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, string_quaternary.replace("一", ''), keys1), keys2)
                effective_duration_quaternary = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, effective_duration_quaternary.replace("一", ''), keys1), keys2)
                encryption_time_quaternary = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, encryption_time_quaternary.replace("一", ''), keys1), keys2)
                compression = string_quaternary + SPLIT_CHAR + effective_duration_quaternary + SPLIT_CHAR + encryption_time_quaternary + "二四"
        if compression_type is None:
            return compression, COMPRESSION_ALGORITHMS["zlib"]['compress'](
                str({"keys1": keys1, "keys2": keys2}))
        else:
            return COMPRESSION_ALGORITHMS[compression_type]['compress'](compression), COMPRESSION_ALGORITHMS["zlib"][
                'compress'](str({"keys1": keys1, "keys2": keys2}))

    def full_random_encryption(self, string: str, effective_duration: int = -1, is_compression: int = 2,
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
        split_char, zero, one, twe, three, four = SPLIT_CHAR, "零", "一", "二", "三", "四"
        a, t, c, g = "A", "T", "C", "G"
        if is_compression == 2:
            value1, k1 = choice_key(RANDOM_KEY, 20)
            key2 = []
            for i in range(20):
                for j in range(20):
                    key2.append(value1[i] + value1[j])
            value2, other = choice_key(k1, 400)
            keys1 = get_random_key(self._t_dict_key1_, value1)
            keys2 = get_random_key(key2, value2)
            other_dt = choice_key(other, 6)
            split_char, zero, one, twe, three, four = other_dt[0]
            a, t, c, g = choice_key(other_dt[1], 4)[0]
        elif is_compression == 1:
            value1, other = choice_key(RANDOM_KEY, 20)
            keys1 = get_random_key(self._t_dict_key1_, value1)
            other_dt = choice_key(other, 6)
            split_char, zero, one, twe, three, four = other_dt[0]
            a, t, c, g = choice_key(other_dt[1], 4)[0]
        elif is_compression == 0:
            other_dt = choice_key(RANDOM_KEY, 6)
            split_char, zero, one, twe, three, four = other_dt[0]
            a, t, c, g = choice_key(other_dt[1], 4)[0]
        compression = None
        if mode == 0:
            string = split_pairwise(str(string_to_binary(string)))
            effective_duration = split_pairwise(str(string_to_binary(str(effective_duration))))
            encryption_time = split_pairwise(str(string_to_binary(str(time.time()))))
            mapping = {"00": a, "01": t, "11": c, "10": g}

            string_binary = ''.join(mapping[i] for i in string)
            effective_duration_binary = ''.join(mapping[i] for i in effective_duration)
            encryption_time_binary = ''.join(mapping[i] for i in encryption_time)
            if is_compression == 0:
                return string_binary + split_char + effective_duration_binary + split_char + encryption_time_binary + f"{zero}{three}", \
                    COMPRESSION_ALGORITHMS["zlib"]['compress'](str(
                        {
                            "keys1": keys1, "keys2": keys2, "split_char": split_char, "one": one, "twe": twe,
                            "three": three, "four": four, "a": a, "t": t, "c": c, "g": g, "zero": zero
                        }))
            if is_compression == 1:
                string_compression = order_compression_and_decompression(True, string_binary, keys1)
                effective_duration_compression = order_compression_and_decompression(True, effective_duration_binary,
                                                                                     keys1)
                encryption_time_compression = order_compression_and_decompression(True, encryption_time_binary,
                                                                                  keys1)
                compression = string_compression + split_char + effective_duration_compression + split_char + encryption_time_compression + f"{one}{three}"
            if is_compression == 2:
                string_compression = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, string_binary.replace(one, ''), keys1), keys2) + f"{twe}{three}"
                effective_duration_compression = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, effective_duration_binary.replace(one, ''), keys1), keys2) + f"{twe}{three}"
                encryption_time_compression = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, encryption_time_binary.replace(one, ''), keys1), keys2) + f"{twe}{three}"
                compression = string_compression + split_char + effective_duration_compression + split_char + encryption_time_compression + f"{twe}{three}"
        elif mode == 1:
            string = str(binary_to_quaternary(string_to_binary(string)))
            effective_duration = str(binary_to_quaternary(string_to_binary(str(effective_duration))))
            encryption_time = str(binary_to_quaternary(string_to_binary(str(time.time()))))
            mapping = {"0": a, "1": t, "2": c, "3": g}
            string_quaternary = ''.join(mapping[i] for i in string)
            effective_duration_quaternary = ''.join(mapping[i] for i in effective_duration)
            encryption_time_quaternary = ''.join(mapping[i] for i in encryption_time)

            if is_compression == 0:
                return string_quaternary + split_char + effective_duration_quaternary + split_char + encryption_time_quaternary + f"{zero}{four}", \
                    COMPRESSION_ALGORITHMS["zlib"]['compress'](str(
                        {
                            "keys1": keys1, "keys2": keys2, "split_char": split_char, "one": one, "twe": twe,
                            "three": three, "four": four, "a": a, "t": t, "c": c, "g": g, "zero": zero
                        }))
            if is_compression == 1:
                string_compression = order_compression_and_decompression(True, string_quaternary, keys1)
                effective_duration_compression = order_compression_and_decompression(True,
                                                                                     effective_duration_quaternary,
                                                                                     keys1)
                encryption_time_compression = order_compression_and_decompression(True, encryption_time_quaternary,
                                                                                  keys1)
                compression = string_compression + split_char + effective_duration_compression + split_char + encryption_time_compression + f"{one}{four}"
            if is_compression == 2:
                string_compression = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, string_quaternary.replace(one, ''), keys1), keys2)
                effective_duration_compression = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, effective_duration_quaternary.replace(one, ''), keys1), keys2)
                encryption_time_compression = order_compression_and_decompression2(
                    True, order_compression_and_decompression(
                        True, encryption_time_quaternary.replace(one, ''), keys1), keys2)
                compression = string_compression + split_char + effective_duration_compression + split_char + encryption_time_compression + f"{twe}{four}"
        if compression_type is None:
            return compression, COMPRESSION_ALGORITHMS["zlib"]['compress'](
                str({"keys1": keys1, "keys2": keys2, "split_char": split_char, "one": one, "twe": twe,
                     "three": three, "four": four, "a": a, "t": t, "c": c, "g": g, "zero": zero}))
        else:
            return COMPRESSION_ALGORITHMS[compression_type]['compress'](compression), COMPRESSION_ALGORITHMS["zlib"][
                'compress'](str({"keys1": keys1, "keys2": keys2, "split_char": split_char, "one": one, "twe": twe,
                                 "three": three, "four": four, "a": a, "t": t, "c": c, "g": g, "zero": zero}))


class SparrowEncryptionAsync(SparrowEncryption):
    def __init__(self, order_keys1: list = None, order_keys2: list = None, easy_keys1: list = None,
                 easy_keys2: list = None):
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

    async def full_random_encryption(self, string: str, effective_duration: int = -1, is_compression: int = 2,
                                     mode: int = 0, compression_type: str = None):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(
            super().full_random_encryption, string=string, effective_duration=effective_duration,
            is_compression=is_compression, mode=mode, compression_type=compression_type
        ))
