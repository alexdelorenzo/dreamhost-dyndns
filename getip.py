import re
import urllib

def get_external_ip():
    site = urllib.urlopen("http://checkip.dyndns.org/").read()
    grab = re.findall('\d{2,3}.\d{2,3}.\d{2,3}.\d{2,3}', site)
    address = grab[0]
    return address

def main():
	print get_external_ip()

if __name__ == "__main__":
	main()
