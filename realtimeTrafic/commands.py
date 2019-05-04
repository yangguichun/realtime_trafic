from realtimeTrafic import app, db
from realtimeTrafic.models import User, Authority, Role
from realtimeTrafic.models import DrivePath, Traffic
from realtimeTrafic.crawler import readTrafficFromBaidu
import click
import schedule
from datetime import datetime
import time


def crawlOnePath(path):
    click.echo('{} 开始抓取路径 {} 数据...'.format(datetime.now(), path.name))
    rtPath = readTrafficFromBaidu(path)
    if rtPath is None:
        return

    db.session.add(rtPath)
    db.session.commit()
    click.echo('{} 抓取路径 {} 完成'.format(datetime.now(), path.name))
    return True


def do_crawl():
    click.echo('{} ----开始新的一轮----'.format(datetime.now()))
    try:
        paths = DrivePath.query.all()
        for path in paths:
            # 如果查询失败了，就重试下
            if not crawlOnePath(path):
                crawlOnePath(path)
  
    except Exception as e:
        print('{} 轮询失败，发生异常...'.format(datetime.now()))
        print(str(e))

@app.cli.command()
def startcrawl():
    do_crawl()
    schedule.every(5).minutes.do(do_crawl)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.cli.command()
def testbaidu():
    yinquan = '22.64558,114.03252'
    kanghesheng = '22.56815,113.95864'
    shoumai = '22.54045,113.95185'
    xiasha = '22.53475,114.03233'
    path = DrivePath(name='银泉>康和盛', origin = yinquan, dest = kanghesheng)
    rtPath = readTrafficFromBaidu(path)
    if rtPath:
        print(rtPath.to_json())


@app.cli.command()
@click.argument('name')
@click.argument('origin')
@click.argument('dest')
def add(name, origin, dest):
    path = DrivePath(name = name, origin = origin, dest = dest)
    db.session.add(path)
    db.session.commit()
    click.echo('成功添加了路径 ' + name)


@app.cli.command()
def init():
    yinquan = '22.64558,114.03252'
    kanghesheng = '22.56815,113.95864'
    shoumai = '22.54045,113.95185'
    xiasha = '22.53475,114.03233'
    paths = []
    paths.append(DrivePath(name='银泉>康和盛', origin = yinquan, dest = kanghesheng))
    paths.append(DrivePath(name='银泉>首迈', origin = yinquan, dest = shoumai))
    paths.append(DrivePath(name='康和盛>银泉', origin = kanghesheng, dest = yinquan))
    paths.append(DrivePath(name='首迈>银泉', origin = shoumai, dest = yinquan))
    paths.append(DrivePath(name='下沙>康和盛', origin = xiasha, dest = kanghesheng))
    paths.append(DrivePath(name='康和盛>下沙', origin = kanghesheng, dest = xiasha))
    for path in paths:
        db.session.add(path)

    db.session.commit()
    click.echo('初始化完成.')

@app.cli.command()
def read():
    paths = DrivePath.query.all()
    for path in paths:
        click.echo(path.to_json())
    click.echo('读取路径完成.')


@app.cli.command()
@click.argument('name')
@click.argument('pwd')
def adduser(name, pwd):
    roles = Role.query.all()
    user = User(name=name, password=pwd, lastLogintime=datetime.now())
    user.roles = roles
    db.session.add(user)
    db.session.commit()


@app.cli.command()
def inituser():
    r1 = Role(name = '游客')
    db.session.add(r1)
    db.session.commit()

@app.cli.command()
def readuser():
    users = User.query.all()
    for u in users:
        print('----user----')
        print(u.to_json())
        for r in u.roles:
            print('----role----')
            print(r.to_json())
            print('----auths----')
            for a in r.authorities:
                print(a.to_json())

@app.cli.command()
def readrole():
    roles = Role.query.all()
    for r in roles:
        print(r.to_json())

@app.cli.command()
def read_auth_from_role():
    role = Role.query.first()
    for a in role.authorities:
        print(a.to_json())