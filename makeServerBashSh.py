# %%
from os import mkdir, path
import json

kind, KIND, password, dir_user, remote_data_raid_path = input().split(' ')
daylist = f'./daylist_{kind}.txt' # サーバー上でのpath
dayMeansh = f'./dayMean_mv.sh'
server_mv_sh = f'./server_mv.sh' 

dir_user_binary = f'{dir_user}/BINARY/6hour'
dir_user_day = f'{dir_user}/BINARY/day'
dir_user_grib = f'{dir_user}/GRIB'

def makeSh(syear,eyear,f,f2,KIND,kind):
    if kind == 'tmp':
        kind2 = 'temp'
    else:
        kind2 = kind
    yearnum = eyear - syear
    for year in range(syear,syear+yearnum+1):
        var = f'/anl_p_{kind}'   
        var2 = f'/anl_p_{kind2}'   
        # dir_user_binary = f'/home/satake/data_raid/JRA55/BINARY/6hour'
        # dir_user_day = f'/home/satake/data_raid/JRA55/BINARY/day'
        # dir_user_grib = f'/home/satake/data_raid/JRA55/GRIB'
        data_raid_path_binary = f'{remote_data_raid_path}/{KIND}/BINARY/6hour'
        data_raid_path_day = f'{remote_data_raid_path}/{KIND}/BINARY/day'
        data_raid_path_grib = f'{remote_data_raid_path}/{KIND}/GRIB'
        dir_raid_binary = f'{data_raid_path_binary}/{str(year).zfill(4)}'
        dir_raid_grib = data_raid_path_grib
        if not path.exists(dir_raid_binary):
            f.write(f'\n')
            f.write(f'if [ ! -e ${dir_raid_binary} ];then\n')
            f.write(f'echo $password | sudo -S mkdir ${dir_raid_binary}\n')
            f.write(f'fi\n')
        f.write(f'\n')
        f2.write(f'\n')
        f.write(f'echo $password | sudo -S mv {dir_user_binary+var}.{str(year).zfill(4)}*.bin {dir_raid_binary} > /dev/null 2>&1'+'\n')
        f.write(f'echo $password | sudo -S mv {dir_user_grib+var}.{str(year).zfill(4)}* {dir_raid_grib} > /dev/null 2>&1'+'\n')
        f2.write(f'echo $password | sudo -S mv {dir_user_day+var2}.{str(year).zfill(4)}.bin {data_raid_path_day} > /dev/null 2>&1'+'\n')


with open(daylist, 'rt', encoding='utf-8') as r:
    dateslist = r.readlines()
r.close()
for dates in dateslist:
    dateslist[dateslist.index(dates)] = dates.rstrip()

syear = int(dateslist[0][:4])
eyear = int(dateslist[-1][:4])
f = open(server_mv_sh, 'wt', encoding='utf-8')
f2 = open(dayMeansh, 'wt', encoding='utf-8')

f.write(f'#!/bin/bash')
f.write(f'\n')
f.write(f'password="{password}"')

f2.write(f'#!/bin/bash')
f2.write(f'\n')
f2.write(f'password="{password}"')

makeSh(syear,eyear,f,f2,KIND,kind)
f.close()
f2.close()
