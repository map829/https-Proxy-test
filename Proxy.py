import requests
import re
import numbers
import time
import sys
import logging

def country_choice ():
    country = input("In what country would you like to search for available proxy server (de, us)")
    country.lower()
    return country

def us_proxy ():
    us_proxy_site = 'https://www.us-proxy.org/'
    r_us_proxy = requests.get(us_proxy_site, timeout=5)
    proxies = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', r_us_proxy.text)
    port_dirty = re.findall('<td>[0-9]{1,5}[^.]<\/td>', r_us_proxy.text)
    port_str = ''.join(port_dirty)
    port = re.findall('[0-9]{1,5}', port_str)
    run_search(port, proxies)
    return

def de_proxy ():
    return

def run_search (port,proxies):
    logging.basicConfig(level=logging.DEBUG)
    count = 0
    target_site = "https://www.southwest.com/"
    for proxy in proxies:
        try:
            session_site = requests.session()
            session_request = session_site.get(target_site, proxies={"https": "https://" + proxy + ":" + port[count] })
            proxy_out = proxy
            port_out = " " + port[count]
            out_string = " " + str(session_request.status_code)
            file = open("proxies.txt", "a")
            file.write(proxy_out + port_out + out_string + '\n')
            print(target_site + " <-- " + proxy_out + port_out + out_string + '\n')
            session_request.close
        except requests.exceptions.RequestException as e:
            print(e)
        count += 1
        time.sleep(10)
    return

if __name__ == '__main__':

    country = country_choice()
    if  country == 'de':
        print('Germany')
        de_proxy()
    elif country == 'us':
        print('USA')
        us_proxy()
    else:
        print('no valid country input found') #bad input return missing