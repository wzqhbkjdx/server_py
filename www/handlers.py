#!/usr/bin/env python
# coding=utf-8

#' url handlers '

import re, time, json, logging, hashlib, base64, asyncio

from aiohttp import web

from apis import APIValueError, APIResourceNotFoundError, APIError

from coroweb import get, post
from models import User, Comment, Blog, next_id, DeviceInfo, Remain
from config import configs
import random

#@get('/')
#async def index(request):
#    users = await User.findAll()
#    return {
#        '__template__' : 'test.html',
#        'users': users
#    }


@get('/')
def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna alique.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time()-7200)
    ]
    return {
        '__template__':'blogs.html',
        'blogs':blogs
    }

@get('/api/users')
async def api_get_users():
    users = await User.findAll(orderBy='created_at desc')
    for u in users:
        u.passwd = '******'
    return dict(user=users)


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')
COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def user2cookie(user, max_age):
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

async def cookie2user(cookie_str):
    if not cookie_str:
        return None
    try:
        L = cookie_str.splite('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

@get('/register')
def register():
    return {
        '__template__':'register.html'
    }

@get('/register3')
def register3():
    return {
        '__template__':'register3.html'
    }


@get('/signin')
def signin():
    return {
        '__template__':'signin.html'
    }

@get('/remain')
async def get_remain():
    max_id =  await Remain.selectMaxId('id')
    m = 0
    for k, v in max_id.items():
        m = int(v) 
        print('max: %s'% m)
    rd = random.randint(1, m)
    result = await Remain.findSpecItem('id', rd)
    return result['num']


    
@post('/api/users')
async def api_register_user(*, email, name, passwd):
    print('save users')
    if not name or not name.strip():
        print('name is not right')
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        print('email is not right')
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        print('passwd is not right')
        raise APIValueError('passwd')
    users = await User.findAll('email=?', [email])
    if len(users) > 0:
        print('email is already in use')
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@post('/api/di')
async def add_device_info(*, density, dpi, scaleDensity,
                         bestProvider): 
    print('density: %s' % density)
    print('add deviceInfo: %s' % dpi)
    print('scaleDensity: %s' % scaleDensity)
    print('bestProvider: %s' % bestProvider)
    #uid = next_id()
    di = DeviceInfo( 
                    density=float(density),
                    dpi = float(dpi),
                    scaleDensity = float(scaleDensity),
                    bestProvider = bestProvider
                   ) 
    rows = await di.save()
    return rows

