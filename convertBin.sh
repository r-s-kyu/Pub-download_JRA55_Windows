#/bin/bash

# ===========物理用読み込み=============
read kind

# =============定数定義==============
jsonData=`cat ./js/path_name.json`
sla='/'
dir=$(echo $jsonData | jq -r ".local.directory.download_GRIB")$sla
dir2=$(echo $jsonData | jq -r ".local.directory.local_BINARY")$sla
list="./text/daylist_$kind.txt"
var=anl_p125_$kind
var2=anl_p_$kind
kaku='.dat'
bin='.bin'

if [ ! -e $dir2 ];then
    mkdir $dir2
fi

while read line
do
    date=${line:0:-1}
    wgrib $dir$var'.'$date$kaku -d all -bin -nh -o $dir2$var2'.'$date$bin
    mv $dir$var'.'$date$kaku $dir$var2'.'$date
done < $list
