# -*- coding: utf-8 -*-
from mcp.server.fastmcp import FastMCP
from pydantic import Field
import os
import logging
import dashscope
import psycopg2
logger = logging.getLogger('mcp')
settings = {
    'log_level': 'DEBUG'
}
# 初始化mcp服务
mcp = FastMCP('pg-metadata-mcp-server', log_level='ERROR', settings=settings)

pg_conn = None

read_tables_sql = '''
SELECT
  t1.table_name, t2.description
FROM (SELECT
  table_name,oid,a.table_schema
FROM information_schema.tables a
left join (select max(oid) oid,relname from pg_class group by relname) b on a.table_name=b.relname ) t1 
left join (select * from pg_description where objsubid = 0) t2 on t1.oid=t2.objoid
where table_schema = '%(table_schema)s' and t1.table_name  in (
'dim_spv_base_info_v',
'dim_repo_base_info_v',
'dim_dro_base_info_df',
'dim_spac_base_info_v',
'dim_spac_note_base_info_v',
'dws_instrument_captured_info_v',
'dws_account_position_info_v', 
'dws_spac_issue_info_v',
'dws_instrument_listing_info_v'
)
'''

read_table_columns_sql = '''
select t1.column_name,t1.data_type,t2.description
from 
(select a.table_name, a.column_name, data_type,
character_maximum_length,b.oid,a.dtd_identifier
from information_schema.COLUMNS a
left join (select max(oid) oid,relname from pg_class group by relname) b
on a.table_name=b.relname where table_schema = '%(table_schema)s'
) t1
LEFT JOIN (select * from pg_description) as t2 on t1.oid = t2.objoid  and cast(t1.dtd_identifier as bigint) = cast(t2.objsubid as bigint)
where t1.table_name = '%(table_name)s'
order by t1.dtd_identifier :: numeric;
'''

def init_pg_conn(host, port, user, password, dbname):
    global pg_conn
    try:
        if pg_conn is None:
            pg_conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                dbname=dbname
            )
            logger.info("创建pg链接成功")
    except Exception as e:
        logger.error(e)

@mcp.tool(name='pg指定schema下的所有表', description='根据输入的地址端口用户密码等信息获取数据库下所有的表')
def get_tables(table_schema:str = Field(description='表所属的schema')) -> dict:
    table_dict = {}
    global pg_conn
    init_pg_conn(os.getenv("PG_HOST"), os.getenv("PG_PORT"), os.getenv("PG_USER"), os.getenv("PG_PASSWORD"), os.getenv("PG_DBNAME"))
    cursor = pg_conn.cursor()
    cursor.execute(read_tables_sql %{'table_schema':table_schema})
    tables = cursor.fetchall()
    for table in tables:
        table_dict[table[0]] = table[1]
    return table_dict

@mcp.tool(name='pg指定表的字段详情', description='根据输入的表名获取数据库下指定表的详情')
def get_table_columns(table_schema:str = Field(description='表所属的schema'),table_name:str = Field(description='表名')) -> dict:
    column_dict = {}
    init_pg_conn(os.getenv("PG_HOST"), os.getenv("PG_PORT"), os.getenv("PG_USER"), os.getenv("PG_PASSWORD"),
                 os.getenv("PG_DBNAME"))
    cursor = pg_conn.cursor()
    cursor.execute(read_table_columns_sql %{'table_schema':table_schema,'table_name':table_name})
    columns = cursor.fetchall()
    for column in columns:
        column_dict[column[0]] = {
            'column_name':column[0],
            'data_type':column[1],
            'description':column[2]
        }
    return column_dict

@mcp.tool(name='在pg执行sql', description='根据输入的sql语句进行元数据库的读写')
def execute_sql(sql:str = Field(description='sql语句')) -> list:
    init_pg_conn(os.getenv("PG_HOST"), os.getenv("PG_PORT"), os.getenv("PG_USER"), os.getenv("PG_PASSWORD"),
                 os.getenv("PG_DBNAME"))
    cursor = pg_conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()
def run():
    mcp.run(transport='stdio')

if __name__ == '__main__':
    print(os.getenv("PG_HOST"))
    init_pg_conn(os.getenv("PG_HOST"), os.getenv("PG_PORT"), os.getenv("PG_USER"), os.getenv("PG_PASSWORD"), os.getenv("PG_DBNAME"))
    run()
