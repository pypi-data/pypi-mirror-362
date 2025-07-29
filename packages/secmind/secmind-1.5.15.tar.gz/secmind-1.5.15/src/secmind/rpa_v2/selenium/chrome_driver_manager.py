import socket
import time
import hashlib
import zlib
import dill
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('driver_client.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('DriverClient')


class ChromeDriverManager:
    """远程驱动管理器"""

    def __init__(self, host='localhost', port=15299):
        self.service_host = host
        self.service_port = port
        self.retry_count = 3
        self.retry_delay = 1  # 秒
        logger.info(f"Initialized for {host}:{port}")

    def _recv_all(self, sock, length):
        """可靠接收指定长度的数据"""
        data = bytearray()
        retries = 0
        max_retries = 10

        while len(data) < length:
            remaining = length - len(data)
            chunk_size = min(4096, remaining)

            try:
                sock.settimeout(10.0)
                packet = sock.recv(chunk_size)
                if packet:
                    data.extend(packet)
                    retries = 0
                else:
                    raise ConnectionError("Connection closed by peer")
            except socket.timeout:
                retries += 1
                if retries >= max_retries:
                    raise TimeoutError(f"Timeout after {retries} retries")
                time.sleep(0.1)
            except BlockingIOError:
                time.sleep(0.01)

        return bytes(data)

    def _send_all(self, sock, data):
        """可靠发送所有数据"""
        total_sent = 0
        retries = 0
        max_retries = 5

        while total_sent < len(data):
            try:
                sock.settimeout(10.0)
                sent = sock.send(data[total_sent:])
                if sent == 0:
                    raise ConnectionError("Connection broken")
                total_sent += sent
                retries = 0
            except socket.timeout:
                retries += 1
                if retries >= max_retries:
                    raise TimeoutError(f"Timeout after {retries} retries")
                time.sleep(0.1)

        return total_sent

    def compress_data(self, data):
        """压缩数据"""
        if len(data) < 1024:  # 小数据不压缩
            return data, False
        try:
            compressed = zlib.compress(data, level=3)
            return compressed, True
        except:
            logger.warning("Compression failed, sending uncompressed")
            return data, False

    def decompress_data(self, data, is_compressed):
        """解压数据"""
        if not is_compressed:
            return data
        try:
            return zlib.decompress(data)
        except:
            logger.error("Decompression failed")
            raise

    def send_data(self, sock, data):
        """发送带校验的数据"""
        # 计算校验和
        checksum = hashlib.md5(data).digest()
        total_size = len(data)

        # 发送元数据: 数据大小 + 校验和
        meta = total_size.to_bytes(8, 'big') + checksum
        self._send_all(sock, meta)

        # 发送实际数据
        sent = self._send_all(sock, data)
        logger.info(f"Sent {sent} bytes with checksum {checksum.hex()}")
        return sent

    def receive_data(self, sock):
        """接收带校验的数据"""
        # 接收元数据 (8字节大小 + 16字节MD5)
        try:
            meta = self._recv_all(sock, 24)  # 8 + 16
            if len(meta) != 24:
                raise ValueError("Invalid metadata received")
        except Exception as e:
            logger.error(f"Error receiving metadata: {str(e)}")
            raise

        total_size = int.from_bytes(meta[:8], 'big')
        expected_checksum = meta[8:]

        # 接收实际数据
        try:
            data = self._recv_all(sock, total_size)
        except Exception as e:
            logger.error(f"Error receiving data: {str(e)}")
            raise

        # 验证校验和
        actual_checksum = hashlib.md5(data).digest()
        if actual_checksum != expected_checksum:
            err_msg = f"Checksum mismatch: expected {expected_checksum.hex()}, got {actual_checksum.hex()}"
            logger.error(err_msg)
            raise ValueError(err_msg)

        logger.info(f"Received {len(data)} bytes with valid checksum")
        return data

    def get_driver(self):
        """从服务获取驱动实例"""
        for attempt in range(1, self.retry_count + 1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(20.0)
                    logger.info(f"Connecting to {self.service_host}:{self.service_port}")
                    sock.connect((self.service_host, self.service_port))

                    # 发送GET_DRIVER命令
                    self.send_data(sock, b"GET_DRIVER")
                    logger.info("GET_DRIVER command sent")

                    # 接收是否压缩标志
                    is_compressed = bool.from_bytes(sock.recv(1), 'big')
                    logger.info(f"Compression: {'yes' if is_compressed else 'no'}")

                    # 接收数据
                    compressed_data = self.receive_data(sock)

                    # 解压数据
                    driver_data = self.decompress_data(compressed_data, is_compressed)

                    # 使用dill反序列化
                    driver = dill.loads(driver_data)
                    logger.info(f"✅ Received driver: {driver.session_id}")
                    return driver

            except Exception as e:
                logger.error(f"Attempt {attempt}/{self.retry_count} failed: {str(e)}")
                if attempt < self.retry_count:
                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"❌ Failed to get driver after {self.retry_count} attempts")
                    raise RuntimeError(f"Failed to get driver: {str(e)}") from e