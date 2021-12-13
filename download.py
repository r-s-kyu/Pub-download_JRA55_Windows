# %%
# download.py
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import os
import calendar
import time
import numpy as np
import json

options = webdriver.ChromeOptions()
options.add_argument('--headless') # ヘッドレスモード起動
options.add_argument('--lang=ja-JP')
driverURL = './driver/chromedriver.exe'
json_file = f'./js/path_name.json'
passdata = f'D:/textdata/passData.json'
download_directory = r'D:\data\JRA55\test_download\GRIB' #ここはwindowsのバックスラッシュのパスにしないとエラーになる
WebURL = f"https://data.diasjp.net/dl/storages/filelist/dataset:204/lang:ja"
WebURLja = f'https://auth.diasjp.net/cas/login?service=https://data.diasjp.net/dl/storages/filelist/dataset:204/lang:ja&locale=ja'
hourslist = [0,6,12,18]
startlist = [2021, 9, 1,0]
givenStartDate = str(startlist[0]).zfill(4)+str(startlist[1]).zfill(2)+str(startlist[2]).zfill(2)+str(startlist[3]).zfill(2)

# ======物理用読み込み========
kind = input()
ldlt = f'./text/lastDownloadDateTime_{kind}.txt'
daylist = f'./text/daylist_{kind}.txt'
misslist = f'./text/misslist_{kind}.txt'

# =========JRAログインID読み込み==========
json_open = open(json_file,'r')
pdata = json.load(json_open)
pass_json_file = pdata["local"]["file"]["password"]
pass_json_open = open(pass_json_file, 'r')
passdata = json.load(pass_json_open)
username = passdata["JRA_login"]["username"]
password = passdata["JRA_login"]["password"]
# print(username,password)

# ===========================================

def check6hourDateTime(ldate):
    # hourslist = [0,6,12,18]
    nyear = ldate[:4]
    nmon = ldate[4:6]
    nday = ldate[6:8]
    nhour = ldate[8:]
    if not int(ldate[8:])%6==0:
        print('適してない！')
    elif int(ldate[8:])==18:
        nhour = str(hourslist[0]).zfill(2)
        nday = str(int(ldate[6:8])+1).zfill(2)
        if int(ldate[6:8]) >= calendar.monthrange(int(ldate[:4]),int(ldate[4:6]))[1]:
            nday = str(1).zfill(2)
            nmon = str(int(ldate[4:6])+1).zfill(2)
            if int(ldate[4:6]) == 12:
                nmon = str(1).zfill(2)
                nyear = str(int(ldate[:4])+1)
    else:
        nhour = str(int(ldate[8:])+6).zfill(2)
    ndate = nyear+nmon+nday+nhour
    return ndate

def checkMinus6hourDateTime(ldate):
    nyear = ldate[:4]
    nmon = ldate[4:6]
    nday = ldate[6:8]
    nhour = ldate[8:]
    if not int(ldate[8:])%6==0:
        print('適してない！')
    elif int(ldate[8:])==0:
        nhour = str(hourslist[3]).zfill(2)
        nday = str(int(ldate[6:8])-1).zfill(2)
        if int(ldate[6:8]) == 1:
            nday = str(calendar.monthrange(int(ldate[:4]),int(ldate[4:6]))[1]).zfill(2)
            nmon = str(int(ldate[4:6])-1).zfill(2)
            if int(ldate[4:6]) == 1:
                nmon = str(12).zfill(2)
                nyear = str(int(ldate[:4])-1)
    else:
        nhour = str(int(ldate[8:])-6).zfill(2)
    pdate = nyear+nmon+nday+nhour
    return pdate    

def checkNextMonthFirstDateTime(ldate):
    nyear = ldate[:4]
    nmon = str(int(ldate[4:6])+1).zfill(2)
    nday = str(1).zfill(2)
    nhour = str(0).zfill(2)
    if ldate[4:6]==str(12).zfill(2):
        nmon = str(1).zfill(2)
        nyear = str(int(ldate[:4])+1).zfill(4)
    ndate = nyear+nmon+nday+nhour
    return ndate

def checkPrevMonthLastDateTime(ldate):
    pyear = ldate[:4]
    pmon = str(int(ldate[4:6])-1)
    pday = str(calendar.monthrange(int(pyear), int(pmon))[1])
    phour = str(18).zfill(2)
    if ldate[4:6]==str(1).zfill(2):
        pmon = str(12).zfill(2)
        pday = str(31).zfill(2)
        pyear = str(int(ldate[:4])-1).zfill(4)
    pdate = pyear+pmon+pday+phour
    return pdate

def makeMonthList(mDatesList,sdate):
    mDatesList = np.array(mDatesList)
    moList = np.array([],dtype=np.int32)
    monthList = np.array([],dtype=np.int32)
    for i in range(len(mDatesList)):
        mo = int(mDatesList[i][4:6])
        monthList = np.append(monthList,mo)
        if i == 0:
            moList = np.append(moList,mo)
        elif mo > moList[-1]:
            moList = np.append(moList,mo)
    ex_moList = []
    moDateList = []
    for mo in moList:
        data = mDatesList[monthList==mo]
        moDateList.append(data)

    if len(ex_moList) == 0:
        ex_missbool = False
    else:
        ex_missbool = True
    return ex_missbool, moList, moDateList

def BrowserSearchfiles(driver,sdate,kind):
    print(f'今から{sdate[:6]}で検索するよ！')
    path_box = driver.find_element_by_id("StorageDirectory")
    path_words = f"/jra55/Hist/Daily/anl_p125/{sdate[:6]}"
    path_box.clear()
    path_box.send_keys("".join(path_words))
    search_box = driver.find_element_by_id("StorageQueryText")
    search_words = f"{kind}.{sdate[:6]}"
    search_box.clear()
    search_box.send_keys("".join(search_words))

    dropdown = driver.find_element_by_id('StorageSearchMode')
    select = Select(dropdown)
    select.select_by_index(1)  # 2番目のoptionタグを選択状態に

    # ファイルを絞り検索
    driver.find_element_by_xpath("//input[@value='ファイル検索']").click()
    print(f'検索完了！')

def hourNumCheck(sdate):
    n = 1
    while True:
        if sdate[8:]==str(hourslist[n-1]).zfill(2):
            hour = n
            break
        
        elif n>4:
            print(f'n={n} , hours break!! つまりerror!!!!')
            break
        n += 1
    return hour


def missDownload(driver,kind,totalnum, ex_missbool, moList, moDateList,ml):
    # 欠損リストmlから欠損日の月をまとめたリストを作成
    scount = 0
    if ex_missbool == True:
        for mo in moList:
            BrowserSearchfiles(driver, moDateList[mo][0],kind)
            missnum = 0
            tagnum = 2
            while True:
                try:
                    tagDate = driver.find_element_by_xpath(f'//*[@id="StorageFileForm"]/table/tbody/tr[{tagnum}]/td[2]/a').get_attribute('textContent')[-11:-1]
                except:
                    while True:
                        if missnum > len(moDateList[mo]):
                            break
                        ml.write(moDateList[mo][missnum])
                        missnum += 1
                    break
                if int(tagDate[6:])< int(moDateList[mo][missnum][6:]):
                    tagDate += 1
                elif int(tagDate[6:]) == int(moDateList[mo][missnum][6:]):
                    scount += 1
                    # 1つ目のURLをクリック
                    driver.find_element_by_xpath(f'//*[@id="StorageFileForm"]/table/tbody/tr[{tagnum}]/td[2]/a').click() # 2番目のtrから抽出
                    # 次のタブに切り替え
                    driver.switch_to.window(driver.window_handles[totalnum + scount])
                    # 利用規約に同意してダウンロード
                    driver.find_element_by_xpath(f'//*[@id="content"]/div[1]/span/form/input').click()
                    # 最初のタブに切り替え
                    driver.switch_to.window(driver.window_handles[0])
                    # タグの抽出
                    print(tagDate)
                    tagnum += 1
                    missnum += 1
                elif int(tagDate[6:]) > int(moDateList[mo][missnum][6:]):
                    ml.write(moDateList[mo][missnum]+'\n')
                    missnum +=1

                if missnum > len(moDateList[mo]):
                    break


    totalnum += scount
    return ml, totalnum

def oneMonthDownload(driver,sdate,kind,totalnum, dl, ml):
    # ダウンロードページでファイル検索
    BrowserSearchfiles(driver,sdate,kind)
    hour = hourNumCheck(sdate)
    snum = (int(sdate[6:8])-1)*4 + hour # snum=1はおのずとsdateと同義
    fnum = snum
    print(f'最初のsnum番号は{snum}')
    # next = True
    while True:
        try:
            # 1つ目のURLをクリック
            driver.find_element_by_xpath(f'//*[@id="StorageFileForm"]/table/tbody/tr[{snum+1}]/td[2]/a').click() # 2番目のtrから抽出
            # 次のタブに切り替え
            driver.switch_to.window(driver.window_handles[totalnum + snum+1-fnum])
            # 利用規約に同意してダウンロード
            driver.find_element_by_xpath(f'//*[@id="content"]/div[1]/span/form/input').click()
            # 最初のタブに切り替え
            driver.switch_to.window(driver.window_handles[0])
            # タグの抽出
            aTag = driver.find_element_by_xpath(f'//*[@id="StorageFileForm"]/table/tbody/tr[{snum+1}]/td[2]/a')
            DateTime = aTag.get_attribute('textContent')[-11:-1]
            dl.write(DateTime+'\n')
            print(DateTime)
            if snum == 1:
                if not DateTime==sdate:
                    ml.write(sdate+'\n')
                
            if snum > 1:
                oneBefore_Tag = driver.find_element_by_xpath(f'//*[@id="StorageFileForm"]/table/tbody/tr[{snum}]/td[2]/a')
                oneBefereDate = oneBefore_Tag.get_attribute('textContent')[-11:-1]

                if not check6hourDateTime(oneBefereDate) == DateTime:
                    missDate = check6hourDateTime(oneBefereDate)
                    while True:
                        if missDate == DateTime:
                            break
                        ml.write(missDate+'\n')
                        missDate = check6hourDateTime(missDate)

            if DateTime[6:]==f'{calendar.monthrange(int(DateTime[:4]),int(DateTime[4:6]))[1]}18':
                # print("Let's go next month!")
                finalDateTime = DateTime
                next = True
                # snum += 1 # while外に出た時のsnumの数合わせのため
                print(f'{kind}.{finalDateTime[:6]}は終わったから、翌月もいけるとこまでいくよ！')
                totalnum += snum + 1 -fnum
                break
            snum += 1
        except:
            if snum == 1: # 月初めちょうどからファイルがない時（昨月末でちょうどで終わってるとき）
                finalDateTime = checkPrevMonthLastDateTime(sdate)
                print(f'って言ったそばから {kind}.{finalDateTime[:6]}は、まだ１つもダウンロードできるファイルがなかったぞ')
            else:    
                finalaTag = driver.find_element_by_xpath(f'//*[@id="StorageFileForm"]/table/tbody/tr[{(snum-1)+1}]/td[2]/a')
                finalDateTime = finalaTag.get_attribute('textContent')[-11:-1]
                print(f'{kind}.{finalDateTime}までファイルをダウンロードしたぞ！')
            next = False
            break
    return next, finalDateTime, totalnum, dl, ml


if not os.path.exists(ldlt):
    print('最新の日付がわからないので、指定した日から最新の更新日までのファイルをダウンロードします。')
    psdate = checkMinus6hourDateTime(givenStartDate)
    sdate = givenStartDate

else:
    with open(ldlt,'rt',encoding='utf-8') as r:
        startDateTime = r.readline().rstrip()
        latestDateTime = r.readline().rstrip()
        if startDateTime == '':
            print('最新の日付がわからないので、指定した日から最新の更新日までのファイルをダウンロードします。')
            psdate = checkMinus6hourDateTime(givenStartDate)
            sdate = givenStartDate
        else:
            print(f'既存するダウンロードリストから、未更新のものをダウンロードしていきます。')
            psdate = latestDateTime
            sdate = check6hourDateTime(latestDateTime)
    r.close()

print(f'今回は{kind}.{sdate}からダウンロードを始めます。')
        
# ダウンロード先のフォルダーを決める
prefs = {"download.default_directory" : download_directory}
options.add_experimental_option("prefs",prefs)
options.add_argument('--ignore-certificate-errors') #SSLエラー対策
driver = webdriver.Chrome(driverURL, chrome_options = options)
# グーグルを開く
driver.get(WebURL)

# ログイン
username_box = driver.find_element_by_id("username")
# search_words = username
username_box.send_keys("".join(username))

password_box2 = driver.find_element_by_id("password")
# search_words2 = password
password_box2.send_keys("".join(password))
driver.find_element_by_xpath("//input[@value='ログイン']").click()
# driver.find_element_by_xpath("//input[@value='LOGIN']").click()


totalnum = 0 # totalnumはブラウザのタブ番号を記録するための変数
next = True # oneMonthDownloadをループするかの判断変数
finalDateTime=''
if os.path.exists(misslist):
    with open(misslist, 'rt',encoding='utf-8') as rml:
        mDatesList = rml.readlines()
    rml.close()
    for dates in mDatesList:
        mDatesList[mDatesList.index(dates)] = dates.rstrip()
    # print(mDatesList)
    # 欠損リストが存在するときだけ、欠損日のデータを検索、ダウンロード
    ml = open(misslist, 'wt', encoding='utf-8')
    if not len(mDatesList)==0:
        ex_missbool, moList, moDateList = makeMonthList(mDatesList,sdate)
        ml, totalnum = missDownload(driver,kind,totalnum, ex_missbool, moList, moDateList,ml)
else:
    ml = open(misslist, 'wt', encoding='utf-8')

dl = open(daylist, 'wt', encoding='utf-8')
while next == True:
    next, finalDateTime, totalnum, dl, ml = oneMonthDownload(driver,sdate,kind,totalnum,dl,ml)
    if next == False:
        break
    else:
        sdate = checkNextMonthFirstDateTime(sdate)
dl.close()
ml.close()
time.sleep(3)

if psdate == finalDateTime:
    print(f'って書いてはいるけど実は')
    print(f'今回は新しいデータがまだ更新されてなかったから何もダウンロードしてないぞ!!')

with open(ldlt,'wt',encoding='utf-8') as f:
    f.write(f'{psdate}' + '\n')
    f.write(f'{finalDateTime}' + '\n')
f.close()

driver.quit()
print(f'finish "download.py"')
