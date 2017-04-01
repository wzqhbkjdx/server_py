#!/usr/bin/env python3
# coding=utf-8

import asyncio, logging
import aiomysql
import os


create_table = ['create table if not exists %s (',
    'id integer not null primary key,' , 
    'idenf varchar(50) not null,' ,
    'phoneNo varchar(100) not null,',
    'create_time datetime not null,',
    'update_time timestamp not null,' ,
    'status integer not null,' ,
    'last_date date,',
    'reach_date date,',
    'done_date varchar(2000)'
') engine=innodb default charset=utf8']



def log(sql, args=()):
    logging.info('SQL: %s' % sql)

async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host = kw.get('get', 'localhost'),
        port = kw.get('get', 3306),
        user = kw['user'],
        password = kw['password'],
        db = kw['db'],
        charset=kw.get('charset', 'utf-8'),
        autocommit=kw.get('autocommit',True),
        maxsize = kw.get('maxsize', 10),
        minsize = kw.get('minsize', 1),
        loop = loop
        )

async def get_pool(loop):
    global __pool
    __pool = await aiomysql.create_pool(host='localhost', port=3306, user='root', password='', db = 'awesome', loop=loop)
    #logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), level=logging.info)
    #logging.debug('create dbconn')    
    print('create dbconn')


async def select(sql, args, size=None):
    log(sql, args)
    global __pool 
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql.replace('?', '%s'), args or ())
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
        logging.info('rows returned: %s' % len(rs))
        await conn.commit()
        return rs
    
async def execute(sql, args, autocommit=True):
    log(sql)
    global __pool
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
                
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            print(e)
            if not autocommit:
                await conn.rollback()
            raise
        print("affected: %s" % affected)
        return affected


def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ','.join(L)


class Field(object):

    def __init__(self, name, column_type, primary_key, default):   
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)

class StringField(Field):

    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)

class BooleanField(Field):

    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)

class IntegerField(Field):

    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)


class FloatField(Field):

    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)


class TextField(Field):

    def __init__(self, name=None,default=None):
        super().__init__(name, 'text', False, default)


class ModelMetaclass(type):
    
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, tableName))
        #print('found model: %s (table: %s)' % (name, tableName))
        mappings = dict()
        fields = [] 
        primary_key = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info(' found mapping: %s ==> %s' % (k, v))

                print('found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    if primary_key:
                        raise StandardError('Duplicate primary key for field: %s'  % k)
                    primary_key = k
                else:
                    fields.append(k)

        if not primary_key:
            raise StandardError('primary key not found.')

        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '%s' %  f, fields))
        attrs['__mappings__'] = mappings
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primary_key
        attrs['__fields__'] = fields
        attrs['__select__'] = 'select %s, %s from %s' % (primary_key, ', '.join(escaped_fields),tableName)
        attrs['__insert__'] = 'insert into %s(%s, %s) values (%s)' % (tableName, ','.join(escaped_fields), primary_key, create_args_string(len(escaped_fields) + 1))
        attrs['__delete__'] = 'delete from %s where %s=?' % (tableName, primary_key)
        attrs['__delete_by_id__'] = 'delete from %s where id=?' % tableName
        attrs['__select_max_id__'] = 'select max(id) from %s' % tableName
        attrs['__select_random__'] = 'select * from %s order by rand() limit 1' % tableName
        attrs['__select_all__'] = 'select * from %s' % tableName;

        attrs['__update__'] = 'update %s set %s where %s=?' % (tableName, ', '.join(map(lambda f: '%s=?' % f, fields)), primary_key)
        attrs['__update_by_id__'] = 'update %s set %s where %s=?' % (tableName, ', '.join(map(lambda f: '%s=?' % f, fields)), 'id')
        attrs['__create_table__'] = ''.join(create_table)
        attrs['__select_date__'] = 'select count(*) from %s where date(%s) = date(now())'
        attrs['__select_spec_date__'] = 'select count(*) from %s where date(%s) = date(?)'
        attrs['__select_by_table__'] = 'select * from %s where %s = %s'
        attrs['__select_by_table_limit__'] = 'select * from %s where date(%s) = date(now()) and status = %s order by rand() limit %s'
        attrs['__select_by_table_limit_date__'] = 'select * from %s where date(%s) = date(?) and status = %s order by rand() limit %s'
        attrs['__select_by_table_remain__'] = 'select * from %s where status = %s and date(last_date) >= date(now()) and date(reach_date) < date(now()) order by rand() limit 1;'
        attrs['__select_by_table_remain_phoneNo__'] = 'select * from %s where status = %s and phoneNo = ? and date(last_date) >= date(now()) and date(reach_date) < date(now()) order by rand() limit 1;'

        attrs['__insert_by_table__'] = 'insert into %s(%s, %s) values (%s)' % ('%s', ','.join(escaped_fields), primary_key, create_args_string(len(escaped_fields) + 1))
        attrs['__update_by_table__'] = 'update %s set %s where %s=?' % ('%s', ', '.join(map(lambda f: '%s=?' % f, fields)), primary_key)

        return type.__new__(cls, name, bases, attrs)
        

class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    async def findAll(cls, where=None, args=None, **kw):
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = await select(' '.join(sql), args)
        return [cls(**r) for r in rs]
        #return rs
    
    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        sql = ['select %s _num_ from %s' % (selectField, cls.__table__)]
        print('select %s _num_ from %s' % (selectField, cls.__table__))
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    @classmethod
    async def find(cls, pk):
        rs = await select('%s where %s=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        print('%s where %s=?' % (cls.__select__, cls.__primary_key__))
        if len(rs) == 0:
            return None
        return cls(**rs[0])
        #return rs

    @classmethod
    async def findById(cls, id):
        #print('findByid: ' %  id)
        rs = await select('%s where %s=?' % (cls.__select_all__, 'id'), [id], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])


    @classmethod
    async def findSpecItem(cls, sp, num):
        rs = await select('%s where %s=?' % (cls.__select__, sp), [num], 1)
        print('%s where %s=?' % (cls.__select__, cls.__primary_key__))
        if len(rs) == 0:
            return None
        return rs[0]

    @classmethod
    async def findSpecCls(cls, sp, num):
        rs = await select('%s where %s=?' % (cls.__select__, sp), [num], 1)
        print('%s where %s=?' % (cls.__select__, cls.__primary_key__))
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    @classmethod
    async def selectSpecItem(cls, sp, num):
        rs = await select('%s where %s=?' % (cls.__select_all__, sp), [num], 1)
        print('%s where %s=?' % (cls.__select_all__, sp))
        if len(rs) == 0:
            return None
        return rs[0]

    @classmethod
    async def selectSpecCls(cls, sp, num):
        rs = await select('%s where %s=?' % (cls.__select_all__, sp), [num], 1)
        print('%s where %s=?' % (cls.__select_all__, sp))
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    @classmethod
    async def selectByTable(cls, tab_name, id, id_value):
        rs = await select(cls.__select_by_table__ % (tab_name, id, id_value), [], 1)
        print(cls.__select_by_table__ % (tab_name, id, id_value))
        if(len(rs) == 0):
            return None
        return cls(**rs[0])

    @classmethod
    async def selectByTableLimit(cls, tab_name, date_name, status, limit):
        rs = await select(cls.__select_by_table_limit__ % (tab_name, date_name, status, limit), [], 0)
        print(cls.__select_by_table_limit__ % (tab_name, date_name, status, limit))
        if(len(rs) == 0):
            return None
        return [cls(**r) for r in rs]

    @classmethod
    async def selectByTableLimitDate(cls, tab_name, date_name, status, limit, cre_date):
        rs = await select(cls.__select_by_table_limit_date__ % (tab_name, date_name, status, limit), [cre_date], 0)
        logging.debug(cls.__select_by_table_limit_date__ % (tab_name, date_name, status, limit))
        print(cls.__select_by_table_limit_date__ % (tab_name, date_name, status, limit))
        if(len(rs) == 0):
            return None
        return [cls(**r) for r in rs]


    @classmethod
    async def selectByTableForRemain(cls, tab_name, status):
        rs = await select(cls.__select_by_table_remain__ % (tab_name, status), [], 1)
        print(cls.__select_by_table_remain__ % (tab_name, status))
        if(len(rs) == 0):
            return None
        return cls(**rs[0])

    @classmethod
    async def selectByTableForRemainPhoneNo(cls, tab_name, status, phoneNo):
        rs = await select(cls.__select_by_table_remain_phoneNo__ % (tab_name, status), [phoneNo], 1)
        print(cls.__select_by_table_remain_phoneNo__ % (tab_name, status))
        if(len(rs) == 0):
            return None
        return cls(**rs[0])


    @classmethod
    async def selectMaxId(cls, sp):
        rs = await select(cls.__select_max_id__,[])
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    @classmethod
    async def selectRandom(cls):
        rs = await select(cls.__select_random__,[])
        if len(rs)==0:
            return None
        return cls(**rs[0])

    @classmethod
    async def selectAll(cls):
        rs = await select(cls.__select_all__, [])
        if len(rs) == 0:
            return None
        return [cls(**r) for r in rs]


    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        print(args)
        print(self.__insert__)
        rows = await execute(self.__insert__, args, False)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)
        return rows

    async def saveByTable(self, tab_name):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        print(args)
        print(self.__insert__)
        rows = await execute(self.__insert_by_table__ % tab_name, args, False)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)
        return rows

    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        print("update agrs: %s" % args)
        print("update self update: %s" % self.__update__)
        rows = await execute(self.__update__, args, False)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)
        return rows

    async def update_by_table(self, tab_name):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        print("update agrs: %s" % args)
        print("update self update: %s" % self.__update__)
        rows = await execute(self.__update_by_table__ % tab_name, args, False)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)
        return rows

    async def update_by_id(self, id):
        args = list(map(self.getValue, self.__fields__))
        args.append(id)
        print('update_by_id args: %s'%  args)
        rows = await execute(self.__update_by_id__, args, False)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)
        return rows

    async def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = await execute(self.__delete__, args, False)
        if rows != 1:
            logging.warn('failed to remove by primary key: affected rows: %s' % rows)
        return rows

    @classmethod
    async def deleteById(cls, id):
        rows = await execute(cls.__delete_by_id__, [id], False)
        print('delete rows: %s' % rows)
        if rows != 1:
            logging.warn('failed to remove by primary key: affected rows: %s' % rows)
        return rows

    @classmethod
    async def createTable(cls, tab_name):
        rows = await execute(cls.__create_table__ % tab_name, [], False)
        # print('create table row: %s' % rows)

    @classmethod
    async def selectDate(cls, tab_name):
        counts = await select(cls.__select_date__ % (tab_name, 'create_time'), [])
        # print('select counts %s' % counts)
        return counts[0]['count(*)']

    @classmethod
    async def selectSpecDate(cls, tab_name, cre_date):
        counts = await select(cls.__select_spec_date__ % (tab_name, 'create_time'), [cre_date])
        # print('select counts %s' % counts)
        return counts[0]['count(*)']