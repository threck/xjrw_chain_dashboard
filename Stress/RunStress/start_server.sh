export PYTHONPATH=/home/fangchao/xjrw_chain_dashboard
log=tmp/ws_server.log
rm -rf ${log}
nohup python ws_server.py &> ${log} &
echo ws_server_pid:$!