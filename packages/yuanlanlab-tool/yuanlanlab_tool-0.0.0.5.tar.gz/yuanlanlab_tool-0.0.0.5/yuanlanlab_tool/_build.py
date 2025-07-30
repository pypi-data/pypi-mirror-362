import os
import time
import zipfile
import urllib.request
import importlib.util


class Build:
    def __init__(self, url, package_name='yuanlanlab_tool', max_retries=3, wait_seconds=2):
        self.url = url
        self.package_name = package_name
        self.max_retries = max_retries
        self.wait_seconds = wait_seconds

    def print_info(self, message):
        print(f'\033[94m{message}\033[0m')  # 蓝色

    def print_success(self, message):
        print(f'\033[92m{message}\033[0m')  # 绿色

    def print_warning(self, message):
        print(f'\033[93m{message}\033[0m')  # 黄色

    def print_error(self, message):
        print(f'\033[91m{message}\033[0m')  # 红色

    def download_file(self, download_path):
        headers = {'User-Agent': 'yuanlanlab-python'}

        for attempt in range(1, self.max_retries + 1):
            try:
                self.print_info(f'开始下载: {self.url}')
                req = urllib.request.Request(self.url, headers=headers)
                with urllib.request.urlopen(req) as response, open(download_path, 'wb') as out_file:
                    out_file.write(response.read())
                self.print_success('下载成功')
                return True
            except Exception as e:
                self.print_warning(f'下载失败 第 {attempt} 次: {e}')
                time.sleep(self.wait_seconds)
        return False

    def find_package_path(self):
        try:
            spec = importlib.util.find_spec(self.package_name)
            if spec and spec.submodule_search_locations:
                package_path = os.path.abspath(spec.submodule_search_locations[0])
                self.print_success(f'找到包路径: {package_path}')
                return package_path
            else:
                self.print_error(f'无法找到包: {self.package_name}')
                return None
        except Exception as e:
            self.print_error(f'查找包路径出错: {e}')
            return None

    def extract_zip(self, zip_file, target_dir):
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    file_name = file_info.filename

                    if os.path.isabs(file_name) or '..' in file_name:
                        self.print_warning(f'跳过可疑文件: {file_name}')
                        continue

                    target_path = os.path.join(target_dir, file_name)

                    if file_info.is_dir():
                        os.makedirs(target_path, exist_ok=True)
                    else:
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)
                        with open(target_path, 'wb') as f:
                            f.write(zip_ref.read(file_info))
            self.print_success(f'成功解压到: {target_dir}')
        except Exception as e:
            self.print_error(f'解压异常: {e}')

    def run(self):
        filename = os.path.basename(self.url)
        temp_zip_path = os.path.join(os.getcwd(), filename)

        if not self.download_file(temp_zip_path):
            self.print_error('所有尝试均失败，终止操作!')
            return

        target_path = self.find_package_path()
        if not target_path:
            self.print_error('找不到目标路径，终止操作!')
            return

        self.extract_zip(temp_zip_path, target_path)

        try:
            os.remove(temp_zip_path)
        except:
            pass


def build(url):
    builder = Build(url)
    builder.run()
