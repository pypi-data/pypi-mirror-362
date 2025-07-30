import bz2
import zlib
import lzma
import gzip
import heapq
import struct
import snappy
import brotli
import lz4.frame


# 优化后的哈夫曼编码实现
class HuffmanNode:
    __slots__ = ('value', 'count', 'left', 'right')

    def __init__(self, value, count):
        self.value = value  # 字节值 (0-255) 或 None（内部节点）
        self.count = count  # 频率计数
        self.left = None  # 左子节点
        self.right = None  # 右子节点

    def __lt__(self, other):
        return self.count < other.count


class HuffmanEncoder:
    @staticmethod
    def compress(data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        if not data:
            return b''

        # 创建频率字典
        freq = [0] * 256
        for byte in data:
            freq[byte] += 1

        # 创建哈夫曼树节点列表
        heap = []
        for byte, count in enumerate(freq):
            if count > 0:
                heapq.heappush(heap, HuffmanNode(byte, count))

        # 处理只有一个字符的特殊情况
        if len(heap) == 1:
            node = heapq.heappop(heap)
            root = HuffmanNode(None, node.count)
            root.left = node
            heap = [root]

        # 构建哈夫曼树
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            parent = HuffmanNode(None, left.count + right.count)
            parent.left = left
            parent.right = right
            heapq.heappush(heap, parent)

        root = heap[0] if heap else None

        # 生成编码表
        code_table = [None] * 256
        stack = [(root, "")]
        while stack:
            node, code = stack.pop()
            if node.value is not None:
                code_table[node.value] = code
            else:
                if node.right:
                    stack.append((node.right, code + "1"))
                if node.left:
                    stack.append((node.left, code + "0"))

        # 编码数据
        encoded_bits = ''.join(code_table[byte] for byte in data)

        # 添加填充信息
        padding = (8 - (len(encoded_bits) % 8)) % 8
        encoded_bits = f"{padding:08b}" + encoded_bits + '0' * padding

        # 将二进制字符串转换为字节
        encoded_bytes = HuffmanEncoder._bits_to_bytes(encoded_bits)

        # 序列化哈夫曼树
        tree_bytes = HuffmanEncoder._serialize_tree(root)

        # 合并树和压缩数据
        result = struct.pack(">H", len(tree_bytes)) + tree_bytes + encoded_bytes
        return result

    @staticmethod
    def _serialize_tree(root):
        if root is None:
            return b''

        result = bytearray()

        # 递归序列化
        def serialize_node(node):
            if node.value is not None:
                # 叶子节点: 标记位'1' + 字节值
                result.append(1)
                result.append(node.value)
            else:
                # 内部节点: 标记位'0'
                result.append(0)
                serialize_node(node.left)
                serialize_node(node.right)

        serialize_node(root)
        return bytes(result)

    @staticmethod
    def _deserialize_tree(data):
        if not data:
            return None

        data_iter = iter(data)

        def deserialize_node():
            try:
                flag = next(data_iter)
                if flag == 1:
                    value = next(data_iter)
                    return HuffmanNode(value, 0)
                else:
                    left = deserialize_node()
                    right = deserialize_node()
                    node = HuffmanNode(None, 0)
                    node.left = left
                    node.right = right
                    return node
            except StopIteration:
                return None

        return deserialize_node()

    @staticmethod
    def _bits_to_bytes(bits):
        # 确保二进制字符串长度是8的倍数
        bits = bits.ljust(((len(bits) + 7) // 8) * 8, '0')

        # 转换为字节
        bytes_list = bytearray()
        for i in range(0, len(bits), 8):
            byte_str = bits[i:i + 8]
            bytes_list.append(int(byte_str, 2))

        return bytes(bytes_list)

    @staticmethod
    def _bytes_to_bits(bytes_data):
        bits = []
        for byte in bytes_data:
            bits.append(f"{byte:08b}")
        return ''.join(bits)

    @staticmethod
    def decompress(compressed):
        if not compressed:
            return b''

        # 解析树长度
        if len(compressed) < 2:
            return b''

        tree_len = struct.unpack(">H", compressed[:2])[0]
        if len(compressed) < 2 + tree_len:
            return b''

        tree_data = compressed[2:2 + tree_len]
        encoded_bytes = compressed[2 + tree_len:]

        # 重建哈夫曼树
        root = HuffmanEncoder._deserialize_tree(tree_data)
        if root is None:
            return b''

        # 将字节转换为二进制字符串
        encoded_bits = HuffmanEncoder._bytes_to_bits(encoded_bytes)

        # 读取填充位数
        if len(encoded_bits) < 8:
            return b''

        padding = int(encoded_bits[:8], 2)
        if padding > 0:
            if len(encoded_bits) < 8 + padding:
                return b''
            encoded_bits = encoded_bits[8:-padding]
        else:
            encoded_bits = encoded_bits[8:]

        # 解码数据
        decoded = bytearray()
        current_node = root

        for bit in encoded_bits:
            if bit == '0':
                current_node = current_node.left
            else:
                current_node = current_node.right

            if current_node is None:
                break

            if current_node.value is not None:
                decoded.append(current_node.value)
                current_node = root

        return bytes(decoded)


# LZ77 算法实现（优化版）
def compress_lz77(data, window_size=4096, max_match_length=258):
    if isinstance(data, str):
        data = data.encode('utf-8')

    output = bytearray()
    i = 0
    data_length = len(data)

    while i < data_length:
        best_offset = 0
        best_length = 0

        # 查找最长匹配
        start = max(0, i - window_size)
        window = data[start:i]

        if window:
            # 在窗口中查找最长匹配
            for length in range(min(max_match_length, len(data) - i), 2, -1):
                pattern = data[i:i + length]
                pos = window.rfind(pattern)
                if pos != -1:
                    best_offset = i - (start + pos)
                    best_length = length
                    break

        if best_length >= 3:
            # 输出三元组 (offset, length)
            # 偏移量用2字节，长度用1字节（0-255）
            offset = min(best_offset, 65535)
            length = min(best_length, 255)
            # 使用标记1表示匹配
            output.append(1)
            output.extend(struct.pack(">H", offset))
            output.append(length)
            i += length
        else:
            # 输出单个字符 (标记位0 + 字符)
            output.append(0)
            output.append(data[i])
            i += 1

    return bytes(output)


def decompress_lz77(compressed):
    output = bytearray()
    i = 0
    compressed_len = len(compressed)

    while i < compressed_len:
        flag = compressed[i]
        i += 1

        if flag == 0:
            # 单个字符
            if i < compressed_len:
                output.append(compressed[i])
                i += 1
        elif flag == 1:
            # 三元组 (offset, length)
            if i + 3 > compressed_len:
                break

            # 大端序读取偏移量
            offset = (compressed[i] << 8) | compressed[i + 1]
            length = compressed[i + 2]
            i += 3

            # 复制匹配数据
            start = len(output) - offset
            if start < 0:
                # 处理无效偏移量
                start = 0
                length = min(length, len(output) - start)
                if length <= 0:
                    continue

            for j in range(length):
                if start + j < len(output):
                    output.append(output[start + j])
                else:
                    # 如果超出范围，使用最后一个有效字符
                    output.append(output[-1])

    return bytes(output).decode('utf-8')


# 压缩算法字典（统一字节接口）
COMPRESSION_ALGORITHMS = {
    'zlib': {
        'compress': lambda data: zlib.compress(data.encode('utf-8')),
        'decompress': lambda compressed: zlib.decompress(compressed).decode('utf-8'),
        'available': True
    },
    'gzip': {
        'compress': lambda data: gzip.compress(data.encode('utf-8')),
        'decompress': lambda compressed: gzip.decompress(compressed).decode('utf-8'),
        'available': True
    },
    'bz2': {
        'compress': lambda data: bz2.compress(data.encode('utf-8')),
        'decompress': lambda compressed: bz2.decompress(compressed).decode('utf-8'),
        'available': True
    },
    'lzma': {
        'compress': lambda data: lzma.compress(data.encode('utf-8')),
        'decompress': lambda compressed: lzma.decompress(compressed).decode('utf-8'),
        'available': True
    },
    'lz4': {
        'compress': lambda data: lz4.frame.compress(data.encode('utf-8')),
        'decompress': lambda compressed: lz4.frame.decompress(compressed).decode('utf-8'),
        'available': True
    },
    'brotli': {
        'compress': lambda data: brotli.compress(data.encode('utf-8')),
        'decompress': lambda compressed: brotli.decompress(compressed).decode('utf-8'),
        'available': True
    },
    'snappy': {
        'compress': lambda data: snappy.compress(data.encode('utf-8')),
        'decompress': lambda compressed: snappy.decompress(compressed).decode('utf-8'),
        'available': True
    },
    'huffman': {
        'compress': lambda data: HuffmanEncoder.compress(data),
        'decompress': lambda compressed: HuffmanEncoder.decompress(compressed).decode('utf-8'),
        'available': True
    },
    'deflate': {
        'compress': lambda data: zlib.compress(data.encode('utf-8'), 6),
        'decompress': lambda compressed: zlib.decompress(compressed).decode('utf-8'),
        'available': True
    },
    'lz77': {
        'compress': lambda data: compress_lz77(data),
        'decompress': lambda compressed: decompress_lz77(compressed),
        'available': True
    }
}
