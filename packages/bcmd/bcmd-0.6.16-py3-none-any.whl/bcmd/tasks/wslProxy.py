from typing import Final

import pyperclip
import typer
from beni import bcolor, btask
from beni.bfunc import syncCall, textToAry

app: Final = btask.newSubApp('WSL2 代理服务')


@app.command()
@syncCall
async def linux(
    port: int = typer.Argument(15236, help="代理服务器端口"),
):
    '生成终端设置代理服务器的命令'
    ip = "$(ip route | grep default | awk '{print $3}')"
    lineAry = textToAry(f'''
        export HTTP_PROXY=http://{ip}:{port}
        export HTTPS_PROXY=http://{ip}:{port}
        export ALL_PROXY=http://{ip}:{port}
        curl https://google.com.hk
    ''')
    msg = '\r\n' + '\n'.join(lineAry) + '\n'
    pyperclip.copy(msg.strip() + '\n')
    bcolor.printMagenta(msg)
    bcolor.printYellow('已复制，可直接粘贴使用')


@app.command()
@syncCall
async def windows(
    port: int = typer.Argument(15236, help="代理服务器端口"),
    off: bool = typer.Option(False, '--off', help='关闭代理'),
):
    '设置防火墙以及端口转发'

    firewallName = 'Allow Veee from WSL'

    if not off:
        template = f'''
        New-NetFirewallRule -DisplayName "{firewallName}" -Direction Inbound -Action Allow -Protocol TCP -LocalPort {port} -RemoteAddress 172.0.0.0/8 -Profile Any
        netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport={port} connectaddress=127.0.0.1 connectport={port}
        netstat -ano | findstr :{port} | findstr 0.0.0.0
        '''
    else:
        template = f'''
        netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport={port}
        Remove-NetFirewallRule -DisplayName "{firewallName}"
        '''
    lineAry = textToAry(template)
    msg = '\r\n' + '\n'.join(lineAry) + '\n'
    pyperclip.copy(msg.strip() + '\n')
    bcolor.printMagenta(msg)
    if not off:
        bcolor.printYellow('开启防火墙以及端口转发')
    else:
        bcolor.printYellow('关闭防火墙以及端口转发')
    bcolor.printYellow('已复制，可直接粘贴使用')
