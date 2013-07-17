import getip
import dhlib
import csv

domain_file = 'domains.csv'
delim = ','

def _grab_ip():
	ipaddr = getip.get_external_ip()
	return ipaddr
 
def _connect_api(server, key):
	connection = dhlib._connect(server, key)
	print "Connected to DH API: ", connection.IsConnected(), "(", server, ")"
	if connection.IsConnected() is False:
		print "Not able to connect. Check your server name and API key values"
		exit()
	return connection

def _check_record(connection, server, ipaddr):
	records = connection.dns.list_records()
	for record in records:
		if record['zone'].strip() == str(server) and record['value'].strip() == str(ipaddr):
			return False
		if record['zone'].strip() == str(server) and record['value'].strip() != str(ipaddr):
			return True
def _check_result(result):
	print result
	if result[2] == 'no_such_zone':
		print "Please visit your Dreamhost control panel, go to Manage Domain and add an 'A' record of '0.0.0.0' and save. Then reload this script."
		print "\nThis is an artifact of the DH API. Please email them if this is an inconvience"
	elif result[2] == 'record_already_exists_remove_first':
		print "'A' record is up to date and points to your IP.\n"
	else:
		print result

def update_ip(server=None, key=None, ipaddr=None, connection=None):
	if server is None:
		server = "yourdomain.com"
	if key is None: 
		key = "YOURKEYGOESHERE"
	if ipaddr is None: 
		ipaddr = _grab_ip
	if connection is None:
		connection = _connect_api(server, key)	
		

	print "Server: ", server, " Key: ", key
	print "Externel IP: ", ipaddr


	result = connection.dns.add_record(record=str(server), value=str(ipaddr), type="A")
	_check_result(result)

def update_via_csv(csvfile=None):
	if csvfile is None:
		csvfile = domain_file
	
	
	updateable_servers = {}

	with open(domain_file, 'r') as domain_csv:
		reader = csv.reader(domain_csv, delimiter=delim)
		for row in reader:
			server, key = row[0], row[1]
			connection, ipaddr = _connect_api(server, key), _grab_ip()	
			updateable = _check_record(connection, server, ipaddr)
			if updateable is True:
				updateable_servers[str(server)] = key

	domain_csv.close()
	for server, key in updateable_servers.iteritems():
		update_ip(server, key, ipaddr)

def main():
	import argparse
	parser = argparse.ArgumentParser(description="Update your DreamHost DNS records.")
	parser.add_argument('-f', 
			    nargs=1,
			    metavar='FILE', 
			    type=str, 
			    help='Comma-separated server/key file.',
			    default='domains.csv',
			    dest='file')
	
	parser.add_argument('-s', dest='server', nargs=1, metavar='SERVER', type=str, help="Server's domain name")
	parser.add_argument('-k', dest='key', nargs=1, metavar='KEY', type=str, help= "DreamHost API Key")
	parser.add_argument('-ip', dest='ip', nargs=1, metavar='IP ADDRESS', type=str, help="Desired A record value")
	a = parser.parse_args()
	
	if a.server is not None and a.key is not None and a.ip is not None:
		update_ip(server=a.server[0], key=a.key[0], ipaddr=a.ip[0])
	elif a.server is not None or a.key is not None or a.ip is not None:
		print "Please specify a server, key, and IP address value"
	else:
		update_via_csv(csvfile=a.file)

			
if __name__ == "__main__":
	main()
