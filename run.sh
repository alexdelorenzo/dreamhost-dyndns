ip=`python getip.py`
while read line
do
	server=`echo $line | cut -d ',' -f1`
	key=`echo $line | cut -d ',' -f2`
	python update_ip.py -s $server -k $key -ip $ip
done < domains.csv

