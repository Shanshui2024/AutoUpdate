import json

# 读取JSON文件
with open('version.json') as json_file:
    data = json.load(json_file)
    version = data.get('version', '0.0.0')

# 版本号递增逻辑，例如自动增加最后一位
version_parts = version.split('.')
version_parts[-1] = str(int(version_parts[-1]) + 1)
new_version = '.'.join(version_parts)

# 输出新版本号供后续步骤使用
print(new_version)
