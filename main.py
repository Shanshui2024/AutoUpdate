import requests , asyncio , json , time , warnings , tempfile , os , urllib , urllib.request , ssl , colorama, shutil
from bs4 import BeautifulSoup
from tqdm.rich import tqdm as tqdm_rich 
from tqdm import TqdmExperimentalWarning

colorama.init()
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
GRAY = '\033[90m'
RESET = '\033[0m'
ssl._create_default_https_context = ssl._create_unverified_context
folder_path = tempfile.gettempdir() + '\\Download\\'


async def download_with_rich_progressbar(url, path,keywords,name):
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(path + keywords[0]):
        print (f'{RED}[ERROR]{RESET} >>> 文件{path + keywords[0]}已存在！')
        return
    with urllib.request.urlopen(url) as response, open(path + keywords[0], 'wb') as out_file:
        file_size = int(response.info().get('Content-Length', -1))
        if file_size == -1:
            out_file.write(response.read())
        else:
            chunk_size = 1024
            num_bars = file_size // chunk_size
            warnings.simplefilter("ignore", TqdmExperimentalWarning)
            progress = tqdm_rich(total=num_bars, unit='MB', unit_scale=True , desc=f'{BLUE}[INFO]{RESET} >>> 正在下载{name}...',unit_divisor=1024)
            while True:
                data = response.read(chunk_size)
                if not data:
                    break
                out_file.write(data)
                progress.update(1)

    progress.close()
async def download_json(url, path):
    with urllib.request.urlopen(url) as response, open(path + '\\software.json', 'wb') as out_file:
        file_size = int(response.info().get('Content-Length', -1))
        if file_size == -1:
            out_file.write(response.read())
        else:
            chunk_size = 1024
            num_bars = file_size // chunk_size
            warnings.simplefilter("ignore", TqdmExperimentalWarning)
            progress = tqdm_rich(total=num_bars, unit='MB', unit_scale=True , desc=f'{BLUE}[INFO]{RESET} >>> 正在下载软件目录...',unit_divisor=1024)
            while True:
                data = response.read(chunk_size)
                if not data:
                    break
                out_file.write(data)
                progress.update(1)


async def find_link(url, keywords):
    response = requests.get(url)
    url_text = BeautifulSoup(response.text, 'html.parser')
    
    for link in url_text.find_all('a', href=True):
        for keyword in keywords:
            if keyword in link.get('href'):
                time.sleep(0.3)
                if link.get('href') == "//dl.360safe.com/360zip_setup.exe" or link.get('href') == '//dl.360safe.com/drvmgr/guanwang__360DrvMgrInstaller_beta.exe':
                    print(f'{GRAY}[DEBUG] >>> 获取到下载' + keyword + '的链接：' + "https:" + link.get('href'))
                    return "https:" + link.get('href')
                return link.get("href")
    
    return None  # 如果没有找到合适的链接，则返回 None

async def dir_prepare(file):
    if not os.path.exists(file):
        os.makedirs(file)
        print (f'{GRAY}[DEBUG] >>> 工作目录创建完成')
    else:
        print (f'{GRAY}[DEBUG] >>> 工作目录已存在')

async def file_prepare(file):
    if not os.path.exists(file):
        await download_json('https://static.shanshui.site/class/software.json',folder_path)
        if os.path.exists(file):
            print (f'{GREEN}[SUCCESS]{RESET} >>> 下载程序准备完成')
            return True
        else:
            print (f'{RED}[ERROR]{RESET} >>> 下载失败，请检查目录或手动下载文件：https://static.shanshui.site/class/software.json')
            return False
    else:
        with open(file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            software_list = data['software_list']
            software_names = [software['name'] for software in software_list]
        print(f'{GRAY}[DEBUG] >>> JSON软件信息如下：' + str(software_names))
        if software_names[0] == '微信':
            print (f'{GREEN}[SUCCESS]{RESET} >>> 下载程序准备完成')
            return True
        else:
            print (f'{GRAY}[DEBUG] >>> 文件失效，正在重新下载...')
            await download_json('https://static.shanshui.site/class/software.json',folder_path)
            if os.path.exists(file):
                print (f'{GREEN}[SUCCESS]{RESET} >>> 下载程序准备完成')
                return True
            else:
                print (f'{RED}[ERROR]{RESET} >>> 下载失败，请检查目录或手动下载文件：https://static.shanshui.site/class/software.json')
                return False


async def main():
    global folder_path
    print (f'{GRAY}[DEBUG] >>> 检查目录...')
    time.sleep(0.3)
    await dir_prepare(folder_path)
    time.sleep(0.3)
    print (f'{GRAY}[DEBUG] >>> 文件下载目录：{folder_path}')
    time.sleep(0.3)
    print (f'{BLUE}[INFO]{RESET} >>> 正在检查下载页面及关键词...')
    time.sleep(0.3)
    result_software = await file_prepare(folder_path + 'software.json')
    time.sleep(0.3)
    if result_software:
        print (f'{BLUE}[INFO]{RESET} >>> 文件检查结束...')
    else:
        print (f'{RED}[ERROR]{RESET} >>> 文件下载/检查失败，请手动下载，程序将在3秒后退出...')
        time.sleep(3)
        exit()
    with open(folder_path + 'software.json', 'r', encoding='utf-8') as f:
        data = json.load(f)['software_list']
        for item in data:
            url = item['download_url']
            keywords = item['keywords']
            name = item['name']
            if ".exe" in url or "WindowsActive.cmd" in url:
                await download_with_rich_progressbar(url, folder_path, keywords,name)
            else:
                link = await find_link(url,keywords)
                await download_with_rich_progressbar(link, folder_path, keywords,name)
    time.sleep(0.3)
    print (f'{BLUE}[INFO]{RESET} >>> 下载完成')
    print(f'{BLUE}[INFO]{RESET} >>> 正在安装微信......')
    print(f'{GRAY}[DEBUG] >>> 测试位置：start /wait {os.path.join(folder_path, 'WeChatSetup.exe')} /S')
    os.system(f'start /wait {folder_path + 'WeChatSetup.exe'} /S')
    print(f'{BLUE}[INFO]{RESET} >>> 正在下载钉钉（主软件，请手动安装新下载的文件）......')
    os.system(f'start /wait {folder_path + 'DingTalk.exe'}')
    print(f'{BLUE}[INFO]{RESET} >>> 正在安装360极速浏览器......')
    os.system(f'start /wait {folder_path + '360csex_setup.exe'} --silent-install=3_1_1')
    print(f'{BLUE}[INFO]{RESET} >>> 正在安装360压缩......')
    os.system(f'start /wait {folder_path + '360zip_setup.exe'} /S')
    print(f'{BLUE}[INFO]{RESET} >>> 正在安装360驱动......')
    os.system(f'start /wait {folder_path + 'guanwang__360DrvMgrInstaller_beta.exe'} /S')
    print(f'{BLUE}[INFO]{RESET} >>> 正在安装鸿合视频展台......')
    os.system(f'start /wait {folder_path + 'HiteCamera.exe'} /SILENT')
    print(f'{BLUE}[INFO]{RESET} >>> 正在安装鸿合i学驱动......')
    os.system(f'start /wait {folder_path + 'HiteiStudy.exe'} /SILENT')
    print(f'{BLUE}[INFO]{RESET} >>> 正在安装希沃白板5......')
    os.system(f'start /wait {folder_path + 'Seewo.exe'} /S')
    print(f'{BLUE}[INFO]{RESET} >>> 正在安装希沃白板插件......')
    os.system(f'start /wait {folder_path + '插件-PC假装是一体机.exe'} /S')
    print(f'{BLUE}[INFO]{RESET} >>> 正在安装WPS Office......')
    os.system(f'"{folder_path + 'WPS Office.exe"'} /S -agreelicense') 
    print(f'{YELLOW}[WARNING]{RESET} >>> 请注意，WPS Office的安装程序是分离的，所以安装需要近3-5分钟甚至更久，直到WPS主进程打开，否则最好不要擅自关闭操作系统')
    print(f'{BLUE}[INFO]{RESET} >>> 正在激活操作系统......（请手动介入激活程序）')
    os.system(f'start /wait {folder_path + 'WindowsActive.cmd'}')
    print(f'{BLUE}[INFO]{RESET} >>> 程序将在5秒后清理工作目录，请注意文件是否仍在使用...')
    time.sleep(5)
    try:
        shutil.rmtree(folder_path)
        print(f'{GREEN}[SUCCESS]{RESET} >>> 工作目录清理完成')
    except OSError as e:
        print(f'{RED}[ERROR]{RESET} >>> 删除文件夹 {folder_path} 失败：{e}，请手动删除')
    print(f'{BLUE}[INFO]{RESET} >>> 程序将在约30秒后退出，您也可以立即退出...')
    time.sleep(30)
asyncio.run(main())
