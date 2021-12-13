jsonData=`cat ./js/path_name.json`
password_path=$(echo $jsonData | jq -r ".local.file.password")
run_path=$(echo $jsonData | jq -r ".local.directory.run_path")
jsonDataPassword=`cat $password_path`
password=$(echo $jsonDataPassword | jq -r ".school_server.sudo")


echo $password
# cd $dir
# cd ../
