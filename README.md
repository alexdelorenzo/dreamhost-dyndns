README
=======

Setup
-----------------

* Visit api.dreamhost.com and obtain a API key with ability to use the dns-* API

* Update `domains.csv` with the domain you wish to modify followed by the API key. Use a comma to separate the two values. No spaces.



Usage
-----------------

```
usage: update_ip.py [-h] [-f FILE] [-s SERVER] [-k KEY] [-ip IP ADDRESS]

Update your DreamHost DNS records.

optional arguments:
  -h, --help      show this help message and exit
  -f FILE         Comma-separated server/key file.
  -s SERVER       Server's domain name
  -k KEY          DreamHost API Key
  -ip IP ADDRESS  Desired A record value
```



I've provided a simple shell script that interfaces with `dhlib`. It has been deprecated by `update_ip.update_ip_csv` 
* Run `chmod +x run.sh` to make the script executable.
* Run `./run.sh` to update your DNS records : )



License
-----------------

All code, unless specified, is licensed under GPLv3. Copyright 2013 Alex DeLorenzo (alex@alexdelorenzo.info).

Thanks to [Laurens Simonis][1] for `dreampylib.py`. Copyright 2009 Laurens Simonis.
* Dreampylib is (c) 2009 by Laurens Simonis. Use it at your own risk, do with it whatever you like, but I am not responsible for whatever you do with it.

[1]: http://dreampylib.laurenssimonis.com/
