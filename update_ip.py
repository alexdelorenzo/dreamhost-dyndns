import getip
import dhlib

def update_ip(server=None, key=None):
	if server is None:
		server = "yourdomain.com"
	if key is None: 
		key = "YOURKEYGOESHERE"

	print "Server: ", server, " Key: ", key

	ipaddr = getip.get_external_ip()
	print "Externel IP: ", ipaddr

	connection = dhlib._connect(server, key)
	print "Connected to DH API: ", connection.IsConnected()

	result = connection.dns.add_record(record=str(server), value=str(ipaddr), type="A")
	print "Result: ", result

def main():
	import sys
	print "Args: ", str(sys.argv)
	update_ip(str(sys.argv[1]), str(sys.argv[2])) if len(sys.argv) is 3 else update_ip()


if __name__ == "__main__":
	main()
