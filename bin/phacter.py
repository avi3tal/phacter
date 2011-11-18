#!/usr/bin/python
import sys
import urllib
import httplib
import phacter

def updateFacts(self):
    f = self.getFacts()
    url = f['dealeraddress']
    params = urllib.urlencode(self.getFacts())
    headers = { "Content-type" : "application/x-www-form-urlencoded",
                "Accept" : "text/plain" }
    conn = httplib.HTTPConnection(url)
    conn.request('POST','/index.php',params,headers)
    response = conn.getresponse()
    print response.status,response.reason
    data = response.read()
    conn.close
    return data
        


def main():
    if len(sys.argv) == 1:
        for fact in phacter.facts:
            print fact
    else:
        print getattr(phacter, sys.argv[1])
    
if __name__ == '__main__':
    main()
