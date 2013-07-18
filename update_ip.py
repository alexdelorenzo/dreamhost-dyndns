import getip
import dhlib
import csv

domain_file = 'domains.csv'
delim = ','
to_be_culled = []

def _grab_ip():
	ipaddr = getip.get_external_ip()
	return ipaddr
 
def _connect_api(server, key):
	connection = dhlib._connect(server, key)
	print "Connected to DH API: ", connection.IsConnected(), "(", server, ")"
	if connection.IsConnected() is False:
		print "Not able to connect. Check your server name and API key values."
		exit()

	return connection

def _to_be_culled(connection=None, record=None, value=None):
	if record is None or value is None or connection is None:
		culling_inevitable = True if len(to_be_culled) is 0 else False
		return culling_inevitable
	else:
		to_be_culled.append((connection, record, value))

def _check_record(connection, server, ipaddr):
	records = connection.dns.list_records()

	no_records = True if len(records) is 0 else False	
	
	if no_records:
		return True

	for record in records:
		try:
			name, value = record['record'], record['value']
		except TypeError:
			print records
		else:
			if name == server and value == str(ipaddr):
				return False
			if name == server and value != str(ipaddr):
				_to_be_culled(connection, record, value)
				return True
			else:
				return True

def _check_result(result):
	if len(result) is 0:
		print "Success"		
	elif len(result) is 3 and result[2] == 'no_such_zone':
		print "\nPlease visit your Dreamhost control panel, go to " 
		print "Manage Domain and add an 'A' record of '0.0.0.0' "
		print "and save. Then reload this script."
		print "\nThis is an artifact of the DH API. Please email Dreamhost"
		print "if this is an inconvience (it is)."
	elif len(result) is 3 and result[2] == 'record_already_exists_remove_first':
		print "'A' record is up to date and points to your IP."
	else:
		print result
	
	print "\n"

def update_ip(server=None, key=None, ipaddr=None, connection=None):
	if server is None:
		server = "yourdomain.com"
	if key is None: 
		key = "YOURKEYGOESHERE"
	if ipaddr is None: 
		ipaddr = _grab_ip()

	if connection is not None:
		server = connection._user
		key = connection._key
	else:
		connection = _connect_api(server, key)	
		

	print "-> Server: ", server, " Key: ", key, " IP: ", ipaddr

	result = connection.dns.add_record(record=str(server), value=str(ipaddr), type="A")
	_check_result(result)

def update_via_csv(csvfile=None):
	if csvfile is None:
		csvfile = domain_file
	
	updateable_servers = []

	with open(domain_file, 'r') as domain_csv:
		reader = csv.reader(domain_csv, delimiter=delim)

		for row in reader:
			server, key = row[0], row[1]
			connection, ipaddr = _connect_api(server, key), _grab_ip()	
			updateable = _check_record(connection, server, ipaddr)

			if updateable is True:
				updateable_servers.append(connection)
				

	domain_csv.close()

	for connection in updateable_servers:
		update_ip(connection=connection)
	
	if _to_be_culled() is True:
		for tup in to_be_culled:
			connection, server, value = tup
			connection.dns.remove_record(record=server, value=value, type='A')
		
def main():
	import argparse
	parser = argparse.ArgumentParser(description="Update your DreamHost DNS records.")
	parser.add_argument('-f', 
			    nargs=1,
			    metavar='FILE', 
			    type=str, 
			    help='Comma-separated server/key file.',
			    default=domain_file,
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
