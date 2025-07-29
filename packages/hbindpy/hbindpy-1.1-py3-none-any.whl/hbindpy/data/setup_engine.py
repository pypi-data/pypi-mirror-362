import os
import logging
import sys
import subprocess
import shutil
import zipfile
import tempfile
import ssl
import hashlib
import glob
from .utils import run_command, get_compiler, get_output_name, VersionInfo

# 禁用SSL验证（仅用于下载MinGW）
ssl._create_default_https_context = ssl._create_unverified_context

# MinGW下载配置
MINGW_URL = "https://github.com/niXman/mingw-builds-binaries/releases/download/13.1.0-rt_v11-rev1/x86_64-13.1.0-release-win32-seh-msvcrt-rt_v11-rev1.7z"
MINGW_SHA256 = "9c3e9d5a5b5f5b5c5e5d5a5b5f5b5c5e5d5a5b5f5b5c5e5d5a5b5f5b5c5e5d5a5b"

def ensure_mingw():
    """确保MinGW已下载并解压"""
    # 计算项目根目录和mingw根目录
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    mingw_root = os.path.join(project_root, "mingw_64")
    
    # 1. 检查MinGW是否已存在
    if os.path.exists(os.path.join(mingw_root, "bin", "g++.exe")):
        logging.info("MinGW already exists, skipping download")
        return mingw_root
    
    # 2. 检查本地是否有mingw_64.zip文件
    local_zips = glob.glob(os.path.join(project_root, "mingw_64*.zip"))
    if local_zips:
        local_zip = local_zips[0]  # 使用第一个找到的zip文件
        logging.info(f"Found local MinGW zip: {local_zip}")
        
        # 解压本地zip文件
        logging.info("Extracting local MinGW zip...")
        try:
            with zipfile.ZipFile(local_zip, 'r') as zip_ref:
                zip_ref.extractall(project_root)
            
            # 检查解压后的目录
            extracted_dirs = [
                d for d in os.listdir(project_root)
                if os.path.isdir(os.path.join(project_root, d)) 
                and "mingw" in d.lower()
            ]
            
            if extracted_dirs:
                extracted_dir = os.path.join(project_root, extracted_dirs[0])
                if os.path.exists(os.path.join(extracted_dir, "bin", "g++.exe")):
                    # 重命名解压后的目录
                    os.rename(extracted_dir, mingw_root)
                    logging.info(f"MinGW successfully extracted from local zip to {mingw_root}")
                    return mingw_root
                else:
                    logging.warning("Extracted directory does not contain g++.exe")
            else:
                logging.warning("No valid MinGW directory found in zip")
        except Exception as e:
            logging.error(f"Failed to extract local MinGW zip: {str(e)}")
    
    # 3. 如果本地没有zip文件，则下载MinGW
    logging.info("MinGW not found, downloading...")
    
    try:
        # 尝试导入tqdm和requests
        from tqdm.rich import tqdm
        import requests
    except ImportError:
        logging.info("Required packages not found. Installing tqdm and requests...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm", "requests"])
        from tqdm.rich import tqdm
        import requests
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "mingw.7z")
    
    try:
        # 下载MinGW
        response = requests.get(MINGW_URL, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        # 使用tqdm.rich显示下载进度
        with open(zip_path, 'wb') as f:
            with tqdm(
                total=total_size, 
                unit='B', 
                unit_scale=True, 
                desc="Downloading MinGW",
                bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
            ) as pbar:
                for data in response.iter_content(chunk_size=1024):
                    f.write(data)
                    pbar.update(len(data))
        
        # 验证文件完整性
        with open(zip_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        if file_hash != MINGW_SHA256:
            raise ValueError(f"Downloaded file hash mismatch: {file_hash} != {MINGW_SHA256}")
        
        # 解压MinGW
        logging.info("Extracting MinGW...")
        with tqdm(
            total=100, 
            desc="Extracting MinGW", 
            bar_format="{desc}: {percentage:3.0f}%|{bar}| [{elapsed}<{remaining}]"
        ) as pbar:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # 获取文件总数用于进度更新
                file_list = zip_ref.infolist()
                total_files = len(file_list)
                
                for i, file_info in enumerate(file_list):
                    zip_ref.extract(file_info, project_root)
                    
                    # 更新进度条（每10个文件更新一次）
                    if i % 10 == 0:
                        pbar.update(10 * (i / total_files))
            
            pbar.update(100)  # 确保进度条完成
        
        # 重命名解压后的目录
        extracted_dir = os.path.join(project_root, "mingw64")
        if os.path.exists(extracted_dir) and not os.path.exists(mingw_root):
            os.rename(extracted_dir, mingw_root)
        
        logging.info(f"MinGW successfully installed at {mingw_root}")
        return mingw_root
    
    except Exception as e:
        logging.error(f"Failed to download and extract MinGW: {str(e)}")
        # 清理临时文件
        if os.path.exists(zip_path):
            os.remove(zip_path)
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise
    
    finally:
        # 确保清理临时文件
        if os.path.exists(zip_path):
            os.remove(zip_path)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

def compile_py_to_exe(config, exe_name):
    """使用PyInstaller将Python脚本编译为独立EXE"""
    # 确保输出目录存在
    output_dir = "hbindpy-output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取当前脚本目录以定位默认图标
    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_icon = os.path.join(current_dir, "_image", "icon.ico")
    
    # 确保MinGW已安装
    mingw_root = ensure_mingw()
    
    build_dir = "hbindpy-build"
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    
    icon_file = config.icon if config.icon else default_icon
    if os.path.exists(icon_file):
        logging.info(f"Using icon: {icon_file}")
        # 检查图标修改时间
        icon_mtime = os.path.getmtime(icon_file)
        if hasattr(config, '_last_icon_mtime') and config._last_icon_mtime != icon_mtime:
            logging.info("Icon file changed, forcing rebuild")
            shutil.rmtree(build_dir, ignore_errors=True)
        config._last_icon_mtime = icon_mtime
    else:
        logging.warning(f"Icon file not found: {icon_file}")

    version_info_args = []
    if config.version_info and sys.platform == "win32":
        # 创建临时版本资源文件
        resource_file = os.path.join("hbindpy-build", "version.rc")
        os.makedirs(os.path.dirname(resource_file), exist_ok=True)
        with open(resource_file, "w", encoding="utf-8") as f:
            f.write(config.version_info.to_rc_data())
        
        # 编译资源文件
        windres_path = os.path.join(mingw_root, "bin", "windres.exe")
        res_file = os.path.join("hbindpy-build", "version.res")
        res_cmd = [windres_path, "-i", resource_file, "-o", res_file]
        
        logging.info("Compiling version resource for EXE")
        res_code, res_output = run_command(res_cmd, config.verbose)
        if res_code != 0:
            logging.error("Failed to compile resource file")
            logging.error(res_output)
            return res_code
        
        # 添加版本文件参数
        version_info_args = ["--version-file", res_file]
    
    # 构建PyInstaller命令
    cmd = [
        "pyinstaller",
        "--onefile",
        "--distpath", output_dir,
        "--workpath", "hbindpy-build",
        "--specpath", "hbindpy-build",
        "--name", os.path.splitext(exe_name)[0]  # 去掉.exe后缀
    ]
    
    # 添加版本信息参数
    cmd.extend(version_info_args)
    
    # 添加图标参数（如果可用）
    if config.icon:
        cmd.extend(["--icon", config.icon])
    elif os.path.exists(default_icon):
        cmd.extend(["--icon", default_icon])
    
    # 添加控制台参数
    if config.noconsole:
        cmd.append("--noconsole")
    
    # 添加源文件
    cmd.append(config.sources[0])
    
    # 执行PyInstaller命令
    logging.info("Starting PyInstaller compilation")
    
    try:
        # 直接使用subprocess.run以便实时输出
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # 实时输出处理
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                logging.info(line.strip())
        
        return_code = process.poll()
        if return_code == 0:
            logging.info(f"PyInstaller compilation successful! Output: {os.path.join(output_dir, exe_name)}")
        else:
            logging.error(f"PyInstaller failed with code {return_code}")
        return return_code
        
    except Exception as e:
        logging.error(f"PyInstaller execution failed: {str(e)}")
        return 1

class BuildConfig:
    """编译配置容器"""
    def __init__(self):
        self.sources = []
        self.include_dirs = []
        self.library_dirs = []
        self.libraries = []
        self.define_macros = []
        self.extra_compile_args = []
        self.extra_link_args = []
        self.std = "c++17"
        self.version = "1.0.0"
        self.version_info = VersionInfo()
        # 新增参数
        self.debug = False
        self.optimize = "O2"
        self.warnings = True
        self.static = False
        self.threading = True
        self.exceptions = True
        self.rtti = True
        self.pic = True
        self.verbose = False
        self.compiler_args = []  # -p参数对应的额外编译器参数
        self.runtime_library_dirs = []
        # 新增EXE参数
        self.icon = None       # EXE图标路径
        self.noconsole = False  # 是否隐藏控制台窗口

def setup(**kwargs):
    """配置构建参数"""
    import warnings
    warnings.filterwarnings("ignore")
    config = BuildConfig()
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
        elif key == "version_info":
            if isinstance(value, dict):
                config.version_info = VersionInfo(**value)
            elif isinstance(value, VersionInfo):
                config.version_info = value
    return config

def build(config, detailed=False, exe_mode=False):
    """执行编译过程"""
    # 检查是否是Python脚本
    if config.sources and config.sources[0].endswith('.py'):
        return compile_py_to_exe(config, get_output_name(True))
    
    # 1. 确定编译器
    compiler_name = get_compiler(config.sources[0]) if config.sources else "g++"
    
    # 确保MinGW已安装
    mingw_root = ensure_mingw()
    compiler_path = os.path.join(mingw_root, "bin", compiler_name + ".exe")
    
    # 2. 构建编译命令
    cmd = [compiler_path]
    if not exe_mode:
        cmd.append("-shared")
    
    # 添加标准
    if config.std:
        cmd.extend(["-std", config.std])
    
    # 包含目录
    for inc in config.include_dirs:
        cmd.extend(["-I", inc])
    
    # 库目录
    for libdir in config.library_dirs:
        cmd.extend(["-L", libdir])
    
    # 链接库
    for lib in config.libraries:
        cmd.extend(["-l", lib])
    
    # 宏定义
    for macro in config.define_macros:
        if isinstance(macro, tuple):
            cmd.append(f"-D{macro[0]}={macro[1]}")
        else:
            cmd.append(f"-D{macro}")
    
    # 新增参数处理
    if config.debug:
        cmd.append("-g")
    if config.optimize:
        cmd.append(f"-{config.optimize}")
    if config.warnings:
        cmd.append("-Wall")
    if config.static:
        cmd.append("-static")
    if config.threading:
        cmd.append("-pthread")
    if not config.exceptions:
        cmd.append("-fno-exceptions")
    if not config.rtti:
        cmd.append("-fno-rtti")
    if config.pic:
        cmd.append("-fPIC")
    if config.verbose:
        cmd.append("-v")
    
    # 运行时库目录
    for rpath in config.runtime_library_dirs:
        cmd.append(f"-Wl,-rpath,{rpath}")
    
    # 额外参数（包括-p参数）
    cmd.extend(config.extra_compile_args)
    cmd.extend(config.compiler_args)
    
    # 源文件
    cmd.extend(config.sources)
    
    # 输出设置
    output_dir = "hbindpy-output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, get_output_name(exe_mode))
    cmd.extend(["-o", output_file])
    
    # 3. 处理版本信息（生成资源文件）
    resource_file = None
    if exe_mode and config.version_info:
        try:
            # 生成资源文件
            resource_file = os.path.join("hbindpy-build", "version.rc")
            os.makedirs(os.path.dirname(resource_file), exist_ok=True)
            with open(resource_file, "w", encoding="utf-8") as f:
                f.write(config.version_info.to_rc_data())
            
            # 编译资源文件
            windres_path = os.path.join(mingw_root, "bin", "windres.exe")
            res_file = os.path.join("hbindpy-build", "version.res")
            res_cmd = [windres_path, "-i", resource_file, "-o", res_file]
            
            logging.info("Compiling version resource")
            res_code, res_output = run_command(res_cmd, detailed)
            if res_code != 0:
                logging.error("Failed to compile resource file")
                logging.error(res_output)
                return res_code
            
            # 添加资源文件到链接
            cmd.append(res_file)
            
        except Exception as e:
            logging.error(f"Resource compilation failed: {str(e)}")
    
    # 4. 执行编译
    logging.info(f"Starting build with {compiler_name}")
    returncode, output = run_command(cmd, detailed)
    
    if returncode == 0:
        logging.info(f"Build successful! Output: {output_file}")
    else:
        logging.error(f"Build failed with code {returncode}")
        logging.error(output)
    
    return returncode