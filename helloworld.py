# coding=utf-8
# 上面的程式內容編碼必須在程式的第一或者第二行才會有作用

################# (1) 模組導入區
# 導入 cherrypy 模組, 為了在 OpenShift 平台上使用 cherrypy 模組, 必須透過 setup.py 安裝
import cherrypy
# 導入 Python 內建的 os 模組, 因為 os 模組為 Python 內建, 所以無需透過 setup.py 安裝
import os

################# (2) 廣域變數設定區
# 確定程式檔案所在目錄, 在 Windows 下有最後的反斜線
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
# 設定在雲端與近端的資料儲存目錄
if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示程式在雲端執行
    download_root_dir = os.environ['OPENSHIFT_DATA_DIR']
    data_dir = os.environ['OPENSHIFT_DATA_DIR']
else:
    # 表示程式在近端執行
    download_root_dir = _curdir + "/local_data/"
    data_dir = _curdir + "/local_data/"

'''以下為近端 input() 與 for 迴圈應用的程式碼, 若要將程式送到 OpenShift 執行, 除了採用 CherryPy 網際框架外, 還要轉為 html 列印
# 利用 input() 取得的資料型別為字串
toprint = input("要印甚麼內容?")
# 若要將 input() 取得的字串轉為整數使用, 必須利用 int() 轉換
repeat_no = int(input("重複列印幾次?"))
for i in range(repeat_no):
    print(toprint)
'''

################# (3) 程式類別定義區
# 以下改用 CherryPy 網際框架程式架構
# 以下為 Hello 類別的設計內容, 其中的 object 使用, 表示 Hello 類別繼承 object 的所有特性, 包括方法與屬性設計
class Hello(object):

    # Hello 類別的啟動設定
    _cp_config = {
    'tools.encode.encoding': 'utf-8',
    'tools.sessions.on' : True,
    'tools.sessions.storage_type' : 'file',
    'tools.sessions.locking' : 'explicit',
    # session 以檔案儲存, 而且位於 data_dir 下的 tmp 目錄
    'tools.sessions.storage_path' : data_dir+'/tmp',
    # session 有效時間設為 60 分鐘
    'tools.sessions.timeout' : 60
    }

    # 以 @ 開頭的 cherrypy.expose 為 decorator, 用來表示隨後的成員方法, 可以直接讓使用者以 URL 連結執行
    @cherrypy.expose
    # index 方法為 CherryPy 各類別成員方法中的內建(default)方法, 當使用者執行時未指定方法, 系統將會優先執行 index 方法
    # 有 self 的方法為類別中的成員方法, Python 程式透過此一 self 在各成員方法間傳遞物件內容
    def index(self, toprint="Hello World!"):
        return toprint

################# (4) 程式啟動區
# 配合程式檔案所在目錄設定靜態目錄或靜態檔案
application_conf = {'/static':{
        'tools.staticdir.on': True,
        # 程式執行目錄下, 必須自行建立 static 目錄
        'tools.staticdir.dir': _curdir+"/static"},
        '/downloads':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/downloads"},
        '/images':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/images"}
    }

if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示在 OpenSfhit 執行
    application = cherrypy.Application(Hello(), config=application_conf)
else:
    # 表示在近端執行
    cherrypy.quickstart(Hello(), config=application_conf)

