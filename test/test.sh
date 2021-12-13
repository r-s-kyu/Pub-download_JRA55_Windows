#!/bin/bash
# if [ ! -e $server_data_raid_path/GRIB ];then mkdir $server_data_raid_path/GRIB; fi


# checker=`python ./searchVersion.py`
# # echo $checker
# if $checker = "True" ; then
# b=ok
# else
# b=error
# fi

# echo $b

# echo 'finish program "JRA55Download_sendServer.sh"'

checker=`python ./driver/searchVersion.py`

