process_nu=${1}
export PYTHONPATH=/home/fangchao/xjrw_chain_dashboard

mkdir -p tmp
log=tmp/ws_client_pid.log
[ -f ${log} ] && rm -rf ${log}

# run client with b chain
nohup python ws_client.py 1 &> tmp/ws_client_1.log &
echo "b chain client number: 1"

# run client without b chain
if [ ${process_nu} -ge 2 ]; then
for ((i=2;i<=${process_nu};i++))
do
nohup python ws_client.py 0 &> tmp/ws_client_${i}.log &
echo $! >> ${log}
done

echo "without b chain client start pid:"
cat ${log}
echo "without b chain client number: $(wc -l ${log})"
fi