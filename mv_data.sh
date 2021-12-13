#!/bin/bash

read kind KIND password dir_user remote_data_raid_path

jsonData=`cat ./js/path_name.json`
server_data=$(echo $jsonData | jq -r ".remote.directory.user.server_file_path")

#以下は "ss" でssh接続できるようにしている。
ssh -t -t ss << END 
cd $server_data
echo $kind $KIND $password $dir_user $remote_data_raid_path | python makeServerBashSh.py
chmod 744 server_mv.sh
./server_mv.sh
exit
END
