from typing import List, Tuple, Union, Any, Dict

class VersionInfo:
    """版本信息结构，包含所有可自定义字段
    
    参数:
        major: 主版本号 (默认: 1)
        minor: 次版本号 (默认: 0)
        micro: 修订版本号 (默认: 0)
        build: 构建号 (默认: 0)
        file_version: 文件版本字符串 (格式: "1.2.3.4") (默认: 自动生成)
        product_version: 产品版本字符串 (默认: 同file_version)
        company_name: 公司名称 (默认: "hbindpy")
        file_description: 文件描述 (默认: "hbindpy Generated Application")
        internal_name: 程序内部名 (任务管理器显示名称) (默认: "hbindpy_app")
        legal_copyright: 版权信息 (默认: "Copyright (C) hbindpy")
        original_filename: 原始文件名 (默认: "hbindpy.exe")
        product_name: 产品名称 (默认: "hbindpy Application")
    """
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
    ) -> None: ...
    
    def to_version_numbers(self) -> str:
        """返回逗号分隔的版本号 (格式: "major,minor,micro,build")"""
        ...
    
    def to_rc_data(self) -> str:
        """生成Windows资源文件内容"""
        ...

def setup(
    sources: List[str] = ...,
    include_dirs: List[str] = ...,
    library_dirs: List[str] = ...,
    libraries: List[str] = ...,
    define_macros: List[Union[Tuple[str, str], str]] = ...,
    extra_compile_args: List[str] = ...,
    extra_link_args: List[str] = ...,
    std: str = ...,
    version: str = ...,
    version_info: Union[Dict, VersionInfo] = ...,
    # 新增参数
    debug: bool = ...,
    optimize: str = ...,
    warnings: bool = ...,
    static: bool = ...,
    threading: bool = ...,
    exceptions: bool = ...,
    rtti: bool = ...,
    pic: bool = ...,
    verbose: bool = ...,
    compiler_args: List[str] = ...,
    runtime_library_dirs: List[str] = ...,
    icon = ...,
    noconsole: bool = ...,
    **kwargs: Any
) -> Any:
    """
    配置构建参数
    
    参数:
        icon: exe图标
        sources: 源文件列表 (必需)
        include_dirs: 头文件搜索路径
        library_dirs: 库文件搜索路径
        libraries: 链接的库名称 (不带lib前缀)
        define_macros: 预定义宏 (可以是字符串或(name, value)元组)
        extra_compile_args: 额外编译选项
        extra_link_args: 额外链接选项
        std: C++标准版本 (例如: 'c++17', 'c++20')
        version: 模块版本字符串
        version_info: 详细版本信息 (字典或VersionInfo对象)
        debug: 是否包含调试信息 (默认: False)
        optimize: 优化级别 ('O0', 'O1', 'O2', 'O3', 'Os') (默认: 'O2')
        warnings: 是否启用警告 (默认: True)
        static: 是否静态链接 (默认: False)
        threading: 是否启用多线程支持 (默认: True)
        exceptions: 是否启用异常处理 (默认: True)
        rtti: 是否启用运行时类型信息 (默认: True)
        pic: 是否生成位置无关代码 (默认: True)
        verbose: 是否显示详细编译过程 (默认: False)
        compiler_args: 额外编译器参数 (对应-p选项)
        runtime_library_dirs: 运行时库搜索路径
        **kwargs: 其他关键字参数 (用于未来扩展)
        
    返回:
        配置对象 (BuildConfig实例)
    """
    ...