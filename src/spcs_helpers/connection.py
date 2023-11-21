import os
import argparse
import snowflake.connector
from snowflake.snowpark import Session

def get_params():
    SNOWFLAKE_HOST = os.getenv('SNOWFLAKE_HOST')
    SNOWFLAKE_PORT = os.getenv('SNOWFLAKE_PORT')
    SNOWFLAKE_PROTOCOL = os.getenv('SNOWFLAKE_PROTOCOL')
    SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
    SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
    SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA')

    parser = argparse.ArgumentParser()
    parser.add_argument('--host_ip', help='Snowflake host ip', default=SNOWFLAKE_HOST)
    parser.add_argument('--host_port', help='Snowflake host port',default=SNOWFLAKE_PORT)
    # parser.add_argument('--protocol', help='protocol', default=SNOWFLAKE_PROTOCOL)
    parser.add_argument('--protocol', help='protocol', default='https')
    parser.add_argument('--username', help='snowflake user name', default='NONE')
    parser.add_argument('--password', help='snowflake password', default='NONE')
    parser.add_argument('--account', help='account used to connect to Snowflake', default=SNOWFLAKE_ACCOUNT)
    parser.add_argument('--warehouse', help='warehouse to use for running queries', default='wh_xs')
    parser.add_argument('--database', help='database to insert data to', default=SNOWFLAKE_DATABASE)
    parser.add_argument('--schema', help='schema to insert data to', default=SNOWFLAKE_SCHEMA)
    return vars(parser.parse_args())

def get_token():
    with open('/snowflake/session/token', 'r') as f:
        return f.read()

def connection() -> snowflake.connector.SnowflakeConnection:
    args = get_params()
    if 'NONE' == args['username']:
        token = get_token()
        creds = {
            'host': args['host_ip'],
            'port': args['host_port'],
            'protocol': args['protocol'],
            'account': args['account'],
            'authenticator': "oauth",
            'token': token,
            'warehouse': args['warehouse'],
            'database': args['database'],
            'schema': args['schema'],
            'client_session_keep_alive': True
        }
    else:
        creds = {
            'account': args['account'],
            'user': args['username'],
            'password': args['password'],
            'warehouse': args['warehouse'],
            'database': args['database'],
            'schema': args['schema'],
            'client_session_keep_alive': True
        }
    connection = snowflake.connector.connect(**creds)
    return connection

def session() -> Session:
    return Session.builder.configs({"connection": connection()}).create()
