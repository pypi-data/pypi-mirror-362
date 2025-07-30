# -*- encoding: utf-8 -*-

'''
@File    :   paramiko_helper.py
@Time    :   2025/07/16 12:13:19
@Author  :   test233
@Version :   1.0
'''

import time
import paramiko
from loguru import logger
from typing import Optional, Union


class SSHClient:
    """
    SSH 客户端，用于远程执行命令，支持 su 切换为 root 用户。
    """

    def __init__(self, ip: str, port: int, user: str, password: str, root_password: Optional[str] = None):
        """
        初始化 SSH 客户端。
        :param ip: 远程主机 IP 地址，例如 "127.0.0.1"
        :param port: 远程主机端口，例如 22
        :param user: 用户名，例如 "user"
        :param password: 用户密码，例如 "password"
        :param root_password: root 用户密码，例如 "rootpassword"（可选）
        """
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.root_password = root_password
        self.ssh: Optional[paramiko.SSHClient] = None

    def connect(self) -> bool:
        """
        连接到远程主机。
        :return: 连接成功返回 True，失败返回 False
        """
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=self.ip, port=self.port,
                             username=self.user, password=self.password)
            return True
        except Exception as e:
            logger.error(
                f"Failed to connect to SSH {self.user}@{self.ip}:{self.port}", exc_info=True)
            return False

    def execute_command(self, command: str, use_su: bool = False) -> Union[str, bool]:
        """
        在远程主机上执行命令。
        :param command: 要执行的命令，例如 "whoami"
        :param use_su: 是否使用 su 切换为 root 用户执行命令，默认为 False
        :return: 成功返回命令输出，失败返回 False
        """
        if not self.ssh:
            logger.error("SSH connection is not established")
            return False
        try:
            if use_su:
                if not self.root_password:
                    logger.error(
                        "Root password is not provided for su operation")
                    return False
                # 使用 invoke_shell 创建交互式 shell
                shell = self.ssh.invoke_shell()
                shell.settimeout(5)  # 设置超时时间
                # 发送 su 命令
                shell.send("su -\n")
                time.sleep(1)  # 等待 su 提示符出现
                # 发送 root 密码
                shell.send(f"{self.root_password}\n")
                time.sleep(1)  # 等待密码验证
                # 发送要执行的命令
                shell.send(f"{command}\n")
                time.sleep(1)  # 等待命令执行
                # 读取命令输出
                output = ""
                while shell.recv_ready():
                    output += shell.recv(1024).decode()
                # 退出 root 用户
                shell.send("exit\n")
                shell.close()
                return output.strip()
            else:
                # 直接执行命令
                _, stdout, stderr = self.ssh.exec_command(command)
                result = stdout.read() or stderr.read()
                return result.decode()
        except Exception as e:
            logger.error(
                f"Failed to execute command '{command}' on {self.user}@{self.ip}:{self.port}", exc_info=True)
            return False

    def close(self) -> None:
        """
        关闭 SSH 连接。
        """
        if self.ssh:
            self.ssh.close()

    def __del__(self):
        self.close()


class SFTPClient:
    """
    SFTP 客户端，用于文件上传和下载。
    """

    def __init__(self, ip: str, port: int, user: str, password: str):
        """
        初始化 SFTP 客户端。
        :param ip: 远程主机 IP 地址，例如 "127.0.0.1"
        :param port: 远程主机端口，例如 22
        :param user: 用户名，例如 "root"
        :param password: 密码，例如 "123456"
        """
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.transport: Optional[paramiko.Transport] = None
        self.sftp: Optional[paramiko.SFTPClient] = None

    def connect(self) -> bool:
        """
        连接到远程主机。
        :return: 连接成功返回 True，失败返回 False
        """
        try:
            self.transport = paramiko.Transport((self.ip, self.port))
            self.transport.connect(username=self.user, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            return True
        except Exception as e:
            logger.error(
                f"Failed to connect to SFTP {self.user}@{self.ip}:{self.port}", exc_info=True)
            return False

    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """
        上传文件到远程主机。
        :param local_path: 本地文件路径，例如 "./test.txt"
        :param remote_path: 远程文件路径，例如 "/tmp/test.txt"
        :return: 成功返回 True，失败返回 False
        """
        if not self.sftp:
            logger.error("SFTP connection is not established")
            return False
        try:
            self.sftp.put(local_path, remote_path)
            return True
        except Exception as e:
            logger.error(
                f"Failed to upload file {local_path} to {remote_path} on {self.user}@{self.ip}:{self.port}", exc_info=True)
            return False

    def download_file(self, remote_path: str, local_path: str) -> bool:
        """
        从远程主机下载文件。
        :param remote_path: 远程文件路径，例如 "/tmp/test.txt"
        :param local_path: 本地文件路径，例如 "./test.txt"
        :return: 成功返回 True，失败返回 False
        """
        if not self.sftp:
            logger.error("SFTP connection is not established")
            return False
        try:
            self.sftp.get(remote_path, local_path)
            return True
        except Exception as e:
            logger.error(
                f"Failed to download file {remote_path} to {local_path} on {self.user}@{self.ip}:{self.port}", exc_info=True)
            return False

    def close(self) -> None:
        """
        关闭 SFTP 连接。
        """
        if self.transport:
            self.transport.close()
        if self.sftp:
            self.sftp.close()

    def __del__(self):
        self.close()


# 测试代码
if __name__ == "__main__":
    # 测试 SSHClient
    print("========== Testing SSHClient ==========")
    # 初始化 SSHClient
    ssh_client = SSHClient(ip="127.0.0.1", port=22, user="user",
                           password="userpassword", root_password="rootpassword")
    if ssh_client.connect():
        print("SSH connection established.")
        # 测试 1: 普通用户执行命令
        print("\nTest 1: Executing command as regular user...")
        command_output = ssh_client.execute_command("whoami")
        print(f"Command output: {command_output}")
        # 测试 2: 使用 su 切换为 root 用户执行命令
        print("\nTest 2: Executing command as root user...")
        command_output = ssh_client.execute_command("whoami", use_su=True)
        print(f"Command output: {command_output}")
        # 测试 3: su 切换失败（密码错误）
        print("\nTest 3: su switch failure (incorrect password)...")
        ssh_client.root_password = "wrongpassword"  # 设置错误的 root 密码
        command_output = ssh_client.execute_command("whoami", use_su=True)
        print(f"Command output: {command_output}")
        ssh_client.root_password = "rootpassword"  # 恢复正确的 root 密码
        # 测试 4: 未提供 root_password 时尝试 su 操作
        print("\nTest 4: Attempting su without root_password...")
        ssh_client.root_password = None  # 清空 root_password
        command_output = ssh_client.execute_command("whoami", use_su=True)
        print(f"Command output: {command_output}")
        # 关闭连接
        ssh_client.close()
    else:
        print("Failed to establish SSH connection.")
    # 测试 SFTPClient
    print("\nTesting SftpClient...")
    sftp_client = SFTPClient(ip="127.0.0.1", port=22,
                             user="root", password="password")
    if sftp_client.connect():
        print("SFTP connection established.")
        if sftp_client.upload_file("./test.txt", "/tmp/test.txt"):
            print("File uploaded successfully.")
        if sftp_client.download_file("/tmp/test.txt", "./downloaded_test.txt"):
            print("File downloaded successfully.")
        sftp_client.close()
    else:
        print("Failed to establish SFTP connection.")
