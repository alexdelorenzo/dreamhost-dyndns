import dreampylib
from pprint import pprint



def _connect(user='yourdomain.com', key='YOURKEYGOESHERE'):
	return dreampylib.DreampyLib(user, key)

connection = _connect()

	
def _cmd_dict_list():
	cmdDict = connection.api.list_accessible_cmds()
	cmdList = []
	for cmd in cmdDict:
		cmdList.append(cmd['cmd'])

	return cmdDict, cmdList

commands, cmdList = _cmd_dict_list()


def _please_print(cmdDict, keys):
        for key in keys:
		if key in cmdDict:
			print key, ": ", cmdDict[key]

def return_cmd_info(key=None):
	if key is None:
		key = raw_input('Fetch cmd info for: ')
 

	options =  ['cmd', 'order', 'args', 'optargs']

	find = []

	for cmd in commands:                                                        
		if cmd['cmd'] == 'dns-list_records':
			find = cmd		
	_please_print(find, options)

def search_cmds(string=None):
	if string is None:
		string = raw_input('Search cmds: ')

	new_list = []
	for cmd in cmdList:
		if string in cmd:
			new_list.append(cmd)
	
	pprint(new_list)
		
def print_help():
	print "Actions:"
	print "--> cmd_info"
	print "--> search_cmd"

def main():
	print_help()
	
	method = raw_input("Action: " )
	if method.lower() in "cmd_info":
		return_cmd_info()
	elif method.lower() in "search_cmds":
		search_cmds()

if __name__ is "__main__":
	main()
