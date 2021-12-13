#!/bin/bash

read kind KIND dir_user remote_data_raid_path

jsonData=`cat ./js/path_name.json`
server_data=$(echo $jsonData | jq -r ".remote.directory.user.server_file_path")

# サーバー上で1年分の1日平均データをまとめたファイルを作成
ssh -t -t ss << END
cd $server_data
echo $kind $KIND $dir_user $remote_data_raid_path | python makeDayMean.py
chmod 744 ./dayMean_mv.sh
./dayMean_mv.sh
exit
END
