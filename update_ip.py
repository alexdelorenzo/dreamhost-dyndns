import getip
import dreampylib
import csv

# one day, i'll wrap this up in a class.
## it's been a year, I'll never do it.
domain_file, delim = 'domains.csv', ','

# what kind of fool puts a mutable obj in global scope
# instead of passing it around / being competent?
# answer: me two years ago
to_be_culled = [] 

def _grab_ip():
	ipaddr = getip.get_external_ip()
	return ipaddr
 
def _connect_api(server, key):
	connection = dreampylib.DreampyLib(server, key)

	print("Connected to DH API: ", connection.IsConnected(), "(", server, ")")

	if connection.IsConnected() is False:
		print("Unable to connect. Check server name and API key values.")
		exit()

	return connection

def _to_be_culled(connection, record, value):
	to_be_culled.append((connection, record, value))

def _check_record(connection, server, ipaddr):
	records = connection.dns.list_records()
	
	if not len(records):
		return True

	for record in records:
		try:
			name, value = record['record'], record['value']
		except TypeError:
			print(records)
			return False
		else:
			if name == server and value == str(ipaddr):
				return False
			if name == server and value != str(ipaddr):
				_to_be_culled(connection, record, value)
				return True
			else:
				return True

def _check_result(result):
	successful = len(result) is 0
	no_such_zone = len(result) is 3 and result[2] == 'no_such_zone'
	up_to_date = (len(result) is 3 and \
		result[2] == 'record_already_exists_remove_first')

	if successful:
		print("Success")
	elif no_such_zone:
		print("\nPlease visit your Dreamhost control panel, go to ")
		print("Manage Domain and add an 'A' record of '0.0.0.0' ")
		print("and save. Then reload this script.")
		print("\nThis is an artifact of the DH API. Please email Dreamhost")
		print("if this is an inconvience (it is).")
	elif up_to_date:
		print("'A' record is up to date and points to your IP.")
	else:
		print(result)
	
	print("\n")

def update_ip(server=None, key=None, ipaddr=None, connection=None):
	if connection is None:
		if server is None:
			server = "yourdomain.com"
		if key is None: 
			key = "YOURKEYGOESHERE"
		connection = _connect_api(server, key)
	else:
		server = connection._user
		key = connection._key

	if ipaddr is None: 
		ipaddr = _grab_ip()
	
	print("-> Server: ", server, " Key: ", key, " IP: ", ipaddr)
	result = connection.dns.add_record(record=str(server), value=str(ipaddr), type="A")
	_check_result(result)

def update_via_csv(csvfile=None):
	if csvfile is None:
		csvfile = domain_file
	
	ipaddr, updateable_servers = _grab_ip(), list()

	with open(csvfile, 'r') as domain_csv:
		reader = csv.reader(domain_csv, delimiter=delim)

		for row in reader:
			server, key = row[0], row[1]
			connection = _connect_api(server, key)	
			updateable = _check_record(connection, server, ipaddr)

			if updateable:
				updateable_servers.append(connection)

	for connection in updateable_servers:
		update_ip(connection=connection)
	
	if to_be_culled:
		for connect, server, value in to_be_culled:
			connection.dns.remove_record(record=server, value=value, type='A')		

def main():
	import argparse

	parser = argparse.ArgumentParser(description="Update your DreamHost DNS records.")
	parser.add_argument(
				'-f', 
				dest='file',
			    	nargs=1,
			   	metavar='FILE', 
			    	type=str, 
			    	help='Comma-separated server/key file.',
			   	default=domain_file  )
	
	parser.add_argument(
				'-s', 
				dest='server', 
				nargs=1, 
				metavar='SERVER', 
				type=str, 
				help="Server's domain name"  )

	parser.add_argument(
				'-k',
				dest='key', 
				nargs=1, 
				metavar='KEY', 
				type=str, 
				help= "DreamHost API Key"  )
	parser.add_argument(
				'-ip', 
				dest='ip', 
				nargs=1, 
				metavar='IP ADDRESS', 
				type=str, 
				help="Desired A record value"  )

	a = parser.parse_args()
	
	args = a.server, a.key, a.ip
	
	manual_update =  all(arg is not None for arg in args)

	insufficient_values_passed = any(arg is not None for arg in args)
	
	if manual_update:
		update_ip(server=a.server[0], key=a.key[0], ipaddr=a.ip[0])
	elif insufficient_values_passed:
		print("Please specify all values: server, key, and IP address")
	else:
		update_via_csv(csvfile=a.file)

			
if __name__ == '__main__':
	main()
