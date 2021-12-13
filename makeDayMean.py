# %%

import numpy as np
import os
from datetime import date
import calendar
import json


kind, KIND, dir_user, remote_data_raid_path = input().split(' ')
if kind == 'tmp':
    kind2 = 'temp'
else:
    kind2 = kind

nx, ny ,nz = 288, 145, 37

daylist = f'./daylist_{kind}.txt'
savefolder = f'{dir_user}/BINARY/day/'
# savefolder = f'/home/satake/data_raid/JRA55/BINARY/day/'
if not os.path.exists(savefolder):
    os.mkdir(savefolder)

with open(daylist, 'rt', encoding='utf-8') as r:
    dateslist = r.readlines()
r.close()
for dates in dateslist:
    dateslist[dateslist.index(dates)] = dates.rstrip()

syear = int(dateslist[0][:4])
eyear = int(dateslist[-1][:4])


def dateChangedaynum(datetime):
    nday = (date(int(datetime[:4]),int(datetime[4:6]),int(datetime[6:8]))
           -date(int(datetime[:4]),1,1)).days + 1 
    return nday

def daynumChangeDate(year,nday):
    month = 1
    while nday > dateChangedaynum(f'{year}{str(month).zfill(2)}{calendar.monthrange(year,month)[1]}'):
        month += 1
    if month == 1:
        day = nday
    else:    
        day = nday - dateChangedaynum(f'{year}{str(month-1).zfill(2)}{calendar.monthrange(year,month-1)[1]}')
    return month, day


for year in range(syear,eyear+1):
    dataraid = f'{remote_data_raid_path}/{KIND}/BINARY/6hour/{year}'
    print(f'make dayMeanfile in {year}')

    if year%4==0:
        yearlength = 366
    else:
        yearlength = 365
    data_4d = np.zeros((yearlength,nz,ny,nx),dtype=np.float32)
    karilist = np.array([],dtype=np.int32)
    misslist = np.array([],dtype=np.int32)
    nday = 1
    # kariday = 0
    while nday<=yearlength:
        try:
            # print(nday)
            month, day = daynumChangeDate(year,nday)
            # print(month,day)
            for hour in range(0,19,6):
                dates = f'{str(year).zfill(4)}{str(month).zfill(2)}{str(day).zfill(2)}{str(hour).zfill(2)}'
                # print(dates)
                savefile = f'{dataraid}/anl_p_{kind}.{dates}.bin'
                input_data = open(savefile, 'rb')
                data = np.fromfile(input_data,dtype='<f').reshape(37,145,288)
                data_4d[nday-1] += data
            kariday = nday
            nday += 1
            print(f'kariday:{kariday}')
            # continue
        except:
            if nday == 1:
                kariday = 1
            misslist = np.append(misslist,nday)
            nday += 1
            print(f'misslist {year}d{nday}')
            # continue

    misslist = misslist[~(misslist>kariday)]
    fmonth, fday = daynumChangeDate(year,1)
    emonth, eday = daynumChangeDate(year,kariday)

    print(f'exist from {year}{str(fmonth).zfill(2)}{str(fday).zfill(2)} to {year}{str(emonth).zfill(2)}{str(eday).zfill(2)}')
    if not len(misslist)==0:
        print('miss dates are')
        for day in misslist:
            mmo, mda = daynumChangeDate(year,day)
            print(f'{mmo}/{mda}/{year}')
    else:
        print(f'There is no miss day in the range')

    data_4d = data_4d/4.
    data_4d = data_4d[:,::-1]
    yearfile = f'{savefolder}anl_p_{kind2}.{year}.bin'
    with open(yearfile,'wb') as wb:
        for l in range(yearlength):
            for k in range(nz):
                dint = data_4d[l,k].T.byteswap(inplace=True)
                b = dint.tobytes('F')
                wb.write(b)
    wb.close()
    print(f'make "anl_p_{kind}.{year}.bin" file')

