import os
import logging
import colorama
from colorama import Fore, Style
import random

colorama.init()

class VersionInfo:
    """版本信息结构，包含所有可自定义字段"""
    def __init__(
        self,
        major: int = 1,
        minor: int = 0,
        micro: int = 0,
        build: int = 0,
        file_version: str = None,
        product_version: str = None,
        company_name: str = "hbindpy",
        file_description: str = "hbindpy Generated Application",
        internal_name: str = "hbindpy_app",
        legal_copyright: str = "Copyright (C) hbindpy",
        original_filename: str = "hbindpy.exe",
        product_name: str = "hbindpy Application",
    ):
        """
        :param major: 主版本号
        :param minor: 次版本号
        :param micro: 修订版本号
        :param build: 构建号
        :param file_version: 文件版本字符串 (格式: "1.2.3.4")
        :param product_version: 产品版本字符串
        :param company_name: 公司名称
        :param file_description: 文件描述
        :param internal_name: 程序内部名 (任务管理器显示名称)
        :param legal_copyright: 版权信息
        :param original_filename: 原始文件名
        :param product_name: 产品名称
        """
        self.major = major
        self.minor = minor
        self.micro = micro
        self.build = build
        self.file_version = file_version or f"{major}.{minor}.{micro}.{build}"
        self.product_version = product_version or self.file_version
        self.company_name = company_name
        self.file_description = file_description
        self.internal_name = internal_name
        self.legal_copyright = legal_copyright
        self.original_filename = original_filename
        self.product_name = product_name
    
    def to_version_numbers(self):
        """返回逗号分隔的版本号"""
        return f"{self.major},{self.minor},{self.micro},{self.build}"
    
    def to_rc_data(self):
        """生成资源文件内容"""
        return f"""#include <windows.h>
VS_VERSION_INFO VERSIONINFO
 FILEVERSION {self.major},{self.minor},{self.micro},{self.build}
 PRODUCTVERSION {self.major},{self.minor},{self.micro},{self.build}
 FILEFLAGSMASK 0x3fL
 FILEFLAGS 0x0L
 FILEOS 0x40004L
 FILETYPE 0x1L
 FILESUBTYPE 0x0L
BEGIN
    BLOCK "StringFileInfo"
    BEGIN
        BLOCK "040904b0"
        BEGIN
            VALUE "CompanyName", "{self.company_name}"
            VALUE "FileDescription", "{self.file_description}"
            VALUE "FileVersion", "{self.file_version}"
            VALUE "InternalName", "{self.internal_name}"
            VALUE "LegalCopyright", "{self.legal_copyright}"
            VALUE "OriginalFilename", "{self.original_filename}"
            VALUE "ProductName", "{self.product_name}"
            VALUE "ProductVersion", "{self.product_version}"
        END
    END
    BLOCK "VarFileInfo"
    BEGIN
        VALUE "Translation", 0x409, 1200
    END
END
"""

def setup_logging(detailed=False):
    level = logging.DEBUG if detailed else logging.INFO
    logging.basicConfig(
        level=level,
        format=f"{Fore.CYAN}%(asctime)s {Style.BRIGHT}[%(levelname)s]{Style.RESET_ALL} %(message)s",
        datefmt="%Y%m%d%H%M%S"
    )
    logger = logging.getLogger()
    # 设置颜色
    logging.addLevelName(logging.INFO, f"{Fore.BLUE}INFO{Style.RESET_ALL}")
    logging.addLevelName(logging.ERROR, f"{Fore.RED}ERROR{Style.RESET_ALL}")
    logging.addLevelName(logging.DEBUG, f"{Fore.GREEN}DEBUG{Style.RESET_ALL}")
    return logger

def ensure_dirs():
    os.makedirs("hbindpy-build", exist_ok=True)
    os.makedirs("hbindpy-output", exist_ok=True)

def get_compiler(source_file):
    if source_file.endswith(".cpp") or source_file.endswith(".cxx"):
        return "g++"
    return "gcc"

def get_output_name(exe_mode=False):
    return "hbindpy.exe" if exe_mode else "hbindpy.pyd"

def run_command(cmd, detailed=False):
    """执行命令并捕获输出"""
    from subprocess import Popen, PIPE, STDOUT
    proc = Popen(cmd, stdout=PIPE, stderr=STDOUT, text=True)
    
    full_output = []
    while True:
        line = proc.stdout.readline()
        if not line and proc.poll() is not None:
            break
        if line:
            full_output.append(line)
            # 根据详细模式控制输出量
            if detailed or random.random() < 0.7:  # 70%输出概率
                level = logging.DEBUG if "error" in line.lower() else logging.INFO
                logging.log(level, line.strip())
    
    return proc.returncode, "".join(full_output)