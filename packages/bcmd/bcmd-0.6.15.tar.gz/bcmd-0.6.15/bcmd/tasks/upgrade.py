from typing import Final

import typer
from beni import bcolor, btask, brun
from beni.bfunc import syncCall

app: Final = btask.app


@app.command()
@syncCall
async def upgrade(
    name: str = typer.Argument('bcmd', help='要更新的包名'),
):
    '使用 uv 官方源更新指定包到最新版本'
    cmd = f'uv tool install -U --index https://pypi.org/simple {name}'
    await brun.run(cmd)
    bcolor.printGreen('OK')