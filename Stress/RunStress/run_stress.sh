bash start_server.sh
sleep 1s
bash start_client_multi.sh 4
sleep 1s
echo "logs dir: tmp/"
echo "logs file: $(ls -l tmp|awk -F' ' '{print $9}')"