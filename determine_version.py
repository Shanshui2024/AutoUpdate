import json

def determine_version():
    with open('version.json', 'r') as file:
        data = json.load(file)
        current_version = data['version']
        # 执行版本更新计算逻辑
        parts = current_version.split('.')
        new_version = f"{parts[0]}.{parts[1]}.{int(parts[2])+1}"
        return new_version

new_version = determine_version()
print(new_version)
