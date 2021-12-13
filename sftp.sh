#!/bin/bash

# ===========物理用読み込み=============
read kind KIND

# =============定数定義==============
filename1='anl_p_'
dot='.'
dotbin='.bin'
dottxt='.txt'
jsonData=`cat ./js/path_name.json`
server_file_path=$(echo $jsonData | jq -r ".remote.directory.user.server_file_path")
download_GRIB=$(echo $jsonData | jq -r ".local.directory.download_GRIB")
local_BINARY=$(echo $jsonData | jq -r ".local.directory.local_BINARY")
server_data_raid_path=$(echo $jsonData | jq -r ".remote.directory.user.server_data_raid_path")

# =============sftp送信===================
ssh ss -t -t << END
if [ ! -e $server_data_raid_path/BINARY ];then mkdir $server_data_raid_path/BINARY; fi
if [ ! -e $server_data_raid_path/BINARY/6hour ];then mkdir $server_data_raid_path/BINARY/6hour; fi
if [ ! -e $server_data_raid_path/BINARY/day ];then mkdir $server_data_raid_path/BINARY/day; fi
if [ ! -e $server_data_raid_path/GRIB ];then mkdir $server_data_raid_path/GRIB; fi
exit
END


sftp ss << END
cd $server_file_path
put makeServerBashSh.py
put makeDayMean.py
lcd ./text
put daylist_$kind$dottxt
lcd $local_BINARY
cd $server_data_raid_path/BINARY/6hour
put $filename1$kind$dot*$dotbin
lcd $download_GRIB
cd $server_data_raid_path/GRIB
put $filename1$kind$dot*
exit
END

# echo Ive just come back now !!!
