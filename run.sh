while read line
do
	server=`echo $line | cut -d ',' -f1`
	key=`echo $line | cut -d ',' -f2`
	python update_ip.py $server $key
	echo; echo; echo
done < domains.csv

