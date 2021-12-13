#!/bin/bash
jsonData=`cat ./js/path_name.json`
password_path=$(echo $jsonData | jq -r ".local.file.password")
dir_user=$(echo $jsonData | jq -r ".remote.directory.user.server_data_raid_path")
remote_data_raid_path=$(echo $jsonData | jq -r ".remote.directory.data_raid.data_raid_path")
run_path=$(echo $jsonData | jq -r ".local.directory.run_path")
jsonDataPassword=`cat $password_path`
password=$(echo $jsonDataPassword | jq -r ".school_server.sudo")
# dir_user_grib = f'{pdata["remote"]["directory"]["user"]["server_data_raid_path"]}/GRIB'
# remote_data_raid_path = f'{pdata["remote"]["directory"]["data_raid"]["data_raid_path"]}'

declare -A name
name=(["hgt"]="HGT" ["tmp"]="T" ["ugrd"]="U" ["vgrd"]="V")
bin='.bin'
checker=`python ./driver/searchVersion.py`

# echo $checker
if ! $checker ; then
    echo "Error:missmatch driverVersion!"
    echo "Error:must change driverVersion or browserVersion!!!"
    echo 
else
    for small in ${!name[@]} 
    do
        kind=$small
        KIND=${name[$kind]}
        # ダウンロードリストをもとにローカルでJRA55をダウンロードする
        cd $run_path
        echo 'start download data'
        echo $kind | python download.py
        echo 'finish download data'
        echo ' '

        # grib形式のファイルをバイナリーに変える
        echo "start change from .dat to .bin"
        echo $kind | ./convertBin.sh
        echo "finish ./convertBin"
        echo " "

        # ローカルからサーバー（ユーザー下）にファイル移動用シェルスクリプトとダウンロードデータをsftp送信
        echo 'start sftp '
        echo $kind $KIND | ./sftp.sh
        echo 'finish sftp '
        echo " "

        # サーバ側で、ローカルからsftp送信したデータをユーザー下からdata_raid下に移動するシェルスクリプト作成
        # サーバー上でdata_raidにデータ移動
        echo "start make 'server_mv.sh' and 'dayMean_mv.sh'"
        echo 'start mv directory in school server'
        echo $kind $KIND $password $dir_user $remote_data_raid_path | ./mv_data.sh
        echo "finish make 'server_mv.sh' and 'dayMean_mv.sh'"
        echo 'finish mv directory in school server'
        echo " "

        # # サーバー上で1年分の1日平均データをまとめたファイルを作成
        echo 'start make and mv Yeardata in school server'
        echo $kind $KIND $dir_user $remote_data_raid_path | ./makeAndMv_dayMean.sh
        echo 'finish make and mv Yeardata in school server'
        echo " "

        # ローカル側のデータの消去
        echo "start remove download data in local"
        cd d:
        cd ./data/JRA55/test_download/BINARY/6hour
        rm anl_p_*
        cd ../../GRIB
        rm anl_p_*
        echo "finish remove download data in local"
        echo " "

        # 作業完了
        echo finish $kind !
        echo " "
    done
fi

echo 
echo "============================================"
echo "============================================"
echo 'finish program "JRA55Download_sendServer.sh"'
echo "============================================"
echo "============================================"