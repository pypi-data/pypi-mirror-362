# sparrowEncryptionDecryption

## 目录

- [简介](#简介)
- [安装](#安装)
- [入口](#入口)
    - [主入口](#主入口)
    - [子入口](#子入口)
    - [分入口](#分入口)
- [使用](#使用)
    - [加密](#解密)
        - [order_encryption](#order_encryption)
        - [easy_encryption](#easy_encryption)
    - [解密](#加密)
        - [order_decryption](#order_decryption)
        - [easy_decryption](#easy_decryption)
- [工具](#工具)
    - [binary_to_quaternary](#binary_to_quaternary)
    - [quaternary_to_binary](#quaternary_to_binary)
    - [string_to_binary](#string_to_binary)
    - [binary_to_string](#binary_to_string)
    - [split_pairwise](#split_pairwise)
    - [split_double_pairwise](#split_double_pairwise)
    - [order_compression_and_decompression2](#order_compression_and_decompression2)
    - [order_compression_and_decompression](#order_compression_and_decompression)

---

## 简介

* sparrowEncryptionDecryption 加密解密库是一个用于数据加密和解密的 Python 库，支持二进制和四进制两种加密模式，并提供同步和异步接口。

---

## 安装

```bash
pip install sparrowEncryptionDecryption
```

---

## 入口

* 导入类方式

### 主入口

* 直接从sparrowEncryptionDecryption导入

```python
import sparrowEncryptionDecryption as sed
from sparrowEncryptionDecryption import SparrowEncryptionDecryption
from sparrowEncryptionDecryption import SparrowEncryptionDecryptionAsync
```

---

### 子入口

* 从sparrowEncryptionDecryption.encryption_decryption导入

```python
from sparrowEncryptionDecryption.encryption_decryption import SparrowEncryption
from sparrowEncryptionDecryption.encryption_decryption import SparrowEncryptionAsync
from sparrowEncryptionDecryption.encryption_decryption import SparrowDecryption
from sparrowEncryptionDecryption.encryption_decryption import SparrowDecryptionAsync
from sparrowEncryptionDecryption.encryption_decryption import SparrowEncryptionDecryption
from sparrowEncryptionDecryption.encryption_decryption import SparrowEncryptionDecryptionAsync
```

---

### 分入口

* 从sparrowEncryptionDecryption.encryption_decryption.function导入

```python
from sparrowEncryptionDecryption.function.decryption import SparrowDecryption
from sparrowEncryptionDecryption.function.decryption import SparrowDecryptionAsync
from sparrowEncryptionDecryption.function.encryption import SparrowEncryption
from sparrowEncryptionDecryption.function.encryption import SparrowEncryptionAsync
```

---

## 使用

* sparrowEncryptionDecryption的使用方法
* sparrowEncryptionDecryption相关类初始化有六个参数，不输入则使用默认秘钥集
    * order_keys1: order方法第一次解密秘钥
    * order_keys2: order方法第二次解密秘钥
    * easy_keys1: easy方法第一次解密秘钥
    * easy_keys2: easy方法第二次解密秘钥
    * dict_key1： random方法的第一次加密键
    * dict_key2： random方法的第二次加密键
    * dict_value1： random方法的第一次加密值
    * dict_value2： random方法的第二次加密值

---

### 加密

* sparrowEncryptionDecryption的加密方法
* 一个有两种方法
    * order_encryption
    * easy_encryption
    * random_encryption

---

#### order_encryption

* 使用order_encryption方法加密数据
* 携带五个参数
    * string: 需要被加密的数据
    * key: 秘钥
    * effective_duration: 秘钥过期时间，-1为永不过期，默认-1
    * is_compression: 默认为2，二次压缩压缩，1为一次压缩，0为不压缩
    * mode: 加密模式，0为二进制加密，1为四进制加密，默认为0
    * compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
* 返回被加密好的数据

```python
from sparrowEncryptionDecryption import SparrowEncryptionDecryption

sed = SparrowEncryptionDecryption()
sed.order_encryption("test", "test")
```

---

#### easy_encryption

* 使用easy_encryption方法加密数据
* 携带三个参数
    * string: 需要被加密的数据
    * key: 秘钥
    * mode: 加密模式，0为二进制加密，1为四进制加密，默认为0
    * compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
* 返回被加密好的数据

```python
from sparrowEncryptionDecryption import SparrowEncryptionDecryption

sed = SparrowEncryptionDecryption()
sed.easy_encryption("test", "test")
```

---

#### random_encryption

* 使用random_encryption方法加密数据
* 携带五个参数
    * string: 需要被加密的数据
    * key: 秘钥
    * effective_duration: 秘钥过期时间，-1为永不过期，默认-1
    * is_compression: 默认为2，二次压缩压缩，1为一次压缩，0为不压缩
    * mode: 加密模式，0为二进制加密，1为四进制加密，默认为0
    * compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
* 返回被加密好的数据以及二进制秘钥

```python
from sparrowEncryptionDecryption import SparrowEncryptionDecryption

sed = SparrowEncryptionDecryption()
sed.random_encryption("test", "test")
```

---

### 解密

* sparrowEncryptionDecryption的解密方法
* 一个又两种方法
    * order_decryption
    * easy_decryption
    * random_decryption

---

#### order_decryption

* 使用order_decryption方法解密数据
* 携带两个参数
    * decompression: 需要被解密的数据
    * key: 秘钥
    * compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
* 返回被解密的数据或秘钥错误类型

```python
from sparrowEncryptionDecryption import SparrowEncryptionDecryption

sed = SparrowEncryptionDecryption()
sed.order_decryption("test", "test")
```

---

#### easy_decryption

* 使用easy_decryption方法解密数据
* 携带两个参数
    * decompression: 需要被解密的数据
    * key: 秘钥
    * compression_type: 压缩算法(zlib、gzip、bz2、lzma、lz4、brotli、snappy、huffman、deflate、lz77)
* 返回被解密的数据或秘钥错误类型

```python
from sparrowEncryptionDecryption import SparrowEncryptionDecryption

sed = SparrowEncryptionDecryption()
sed.easy_decryption("test", "test")
```

---

#### random_decryption

* 使用random_decryption方法解密数据
* 携带两个参数
    * decompression: 需要被解密的数据
    * key: 秘钥（二进制秘钥）
* 返回被解密的数据或秘钥错误类型

---

```python
from sparrowEncryptionDecryption import SparrowEncryptionDecryption

sed = SparrowEncryptionDecryption()
sed.random_decryption("test", b"test")
```

## 工具

* sparrowEncryptionDecryption涉及使用到的工具方法

### binary_to_quaternary

* 将二进制转换为四进制
* 携带一个参数
    * binary: 二进制串
* 返回二进制的四进制数据

---

### quaternary_to_binary

* 将四进制转换为二进制
* 携带一个参数
    * quaternary: 四进制串
* 返回四进制的二进制数据

---

### string_to_binary

* 将字符串转换为二进制
* 携带一个参数
    * string: 字符串
* 返回字符串的二进制数据

---

### binary_to_string

* 将二进制转换为字符串
* 携带一个参数
    * binary: 二进制串
* 返回二进制代表的字符串

---

### split_pairwise

* 将字符串两两分为一组并存入数组
* 携带一个参数
    * string: 被分割的字符串
* 返回分割好的数组

---

### split_double_pairwise

* 将字符串每四个分为一组并存入数组
* 携带一个参数
    * string: 被分割的字符串
* 返回分割好的数组

---

### order_compression_and_decompression2

* 将加密内容进行二次压缩或解压
* 携带三个参数
    * keys2: 密钥对
    * mode: True为加密，False为解密，bool类型
    * data: 需要被压缩或解压的数据
* 返回被压缩或解压的数据

---

### order_compression_and_decompression

* 将加密内容压缩或解压
* 携带三个参数
    * keys2: 密钥对
    * mode: True为加密，False为解密，bool类型
    * data: 需要被压缩或解压的数据
* 返回被压缩或解压的数据

---

### shuffle_by_seed

* 根据输入字符串作为种子打乱数组
* 携带两个参数
    * input_string: 用于生成随机种子的字符串
    * array: 需要被打乱的数组
* 打乱后的新数组

---

### get_random_key

* 生成随机密钥对
* 携带两个参数
    * keys： 秘钥键
    * values： 秘钥值