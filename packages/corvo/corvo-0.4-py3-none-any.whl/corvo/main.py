from .lib.intelxapi import intelx
from .lib.leakParser import Leaks

from datetime import datetime as dt
from dateutil import relativedelta as rd
import os
import re
import sys
import json
import argparse
import configparser
from pathlib import Path
import time

KEY_PATH = os.path.join(os.path.expanduser("~"), '.corvo.ini')

def save_key(key:str) -> None:
    config = configparser.ConfigParser()
    config['API'] = {'key': key}
    with open(KEY_PATH, 'w') as configfile:
        config.write(configfile)

def get_key()->str:
    config = configparser.ConfigParser()
    try:
        config.read(KEY_PATH)
        key = config['API']['key']
        return key
    except Exception as err:
        return ''

def main():
    leakP = Leaks()
    key = get_key()
    key_exists = False
    if key or '-p' in sys.argv:
        key_exists = True

    date_exists = False
    if '-b' in sys.argv or '-a' in sys.argv:
        date_exists = True

    parser = argparse.ArgumentParser(description='A credential harvester, powered by the IntelX API.')

    parser.add_argument('-i', '--init', action='store_true', required=not key_exists, dest='init', help='First step. Save your IntelX credentials')

    parser.add_argument('-a', type=str, dest='after', required=date_exists, help="Date started to collecting infostealer leaks. Format: YYYY-MM-DD")
    parser.add_argument('-b', type=str, dest='before', required=date_exists, help="Date finished to collecting infostealer leaks. Format: YYYY-MM-DD")

    parser.add_argument('-p', dest='leak_path', help='Pass a path of leaks only of infostealers to be parsed, if you already download it.')
    parser.add_argument('-t', required=key_exists and  not '-f' in sys.argv, dest='term', help='The term (str) to be searched')
    parser.add_argument('-f', dest='filepath', required=key_exists and not '-t' in sys.argv, help='A config file with domains.')


    parser.add_argument('-r', dest='reduce_queries', action='store_true', help='Evade flow to reduce queries')
    parser.add_argument('-d', dest='debugger', action='store_true', help='More info for output, debugger')

    args = parser.parse_args()
    current_path = Path.cwd()
    corvo_path = current_path / 'leaks'

    if not args:
        exit()
    else:
        if args.init:
            key = input('Enter you intelx key:')
            save_key(key)
            print("Key saved")
            exit()    

        if not key and not '-p' in sys.argv:
            print("Run init command first - API key was not found or is not correct")
            exit()

        api_use = True
        if '-p' in sys.argv:
            api_use = False
        
        if api_use:
            x = intelx(key=key)
        
        date_after = ''
        date_before = ''
        if args.after:
            date_after = args.after + ' 00:00:00'
        if args.before:
            date_before = args.before + ' 23:59:59'
        
        domains = {}
        total_group_names = {}
        
        company_leak = []
        client_leak = []

        group_name_file = {
                        "info": ['info', 'system'], # 'system_info.txt', 'information.txt', 'userinformation.txt', 'system.txt'
                        "password": ["pass"] #'passwords.txt', "pass.txt"
                    }

        output = open('corvo.leaks', 'w')

        if args.leak_path: # Must exists term or a domain file
            if args.term:
                now = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
                domains.setdefault(now, [args.term])
            else:
                domains = leakP.read_domain_file(args.filepath)

            info_groups = {}
            for key, items in domains.items():
                if args.filepath:
                    print(key) # Domains key
                    word_len = len(key)
                    output.write(f"#" * (word_len + 6))
                    output.write('\n')
                    output.write(f"## {key} ##")
                    output.write('\n')
                    output.write(f"#" * (word_len + 6))
                    output.write('\n')

                if os.path.isdir(args.leak_path):
                    for (root,dirs,files) in os.walk(args.leak_path): 
                        for file in files:
                            file1 = open(os.path.join(root, file), "r")
                            file_content = file1.read()
                            header_file = file_content[:1000]
                            
                            group = leakP.check_group_name(header_file)
                            if group:
                                info_groups.setdefault(group,0)
                                info_groups[group] += 1
                            else:
                                info_groups.setdefault('unknown',0)
                                info_groups['unknown'] += 1


                            term_leaks = leakP.filter_domain_leak(file_content, items)

                            if not term_leaks:
                                output.write(f"Unknown pattern for file or no match: {file}\n")
                                term_leaks = {'company':[], 'client': []}
                                continue                 
                                
                            if args.debugger:
                                output.write(term_leaks)
                            
                            company_leak = [*company_leak, *term_leaks.get('company', [])]
                            client_leak = [*client_leak, *term_leaks.get('client', [])]

                            output.write(f'Company Leaks ({len(company_leak)}) - {items}\n')
                            if company_leak:
                                for item in company_leak:
                                    output.write(json.dumps(item))
                            output.write('\n')
                            output.write(f'Client Leaks ({len(client_leak)}) - {items}\n')
                            if client_leak:
                                for item in client_leak:
                                    output.write(json.dumps(item))
                            output.write('\n')
                output.write('\n')
                output.write(f"Grupos: {info_groups}")
            print('Check the result at corvo leaks file')
            exit()

        if args.term:
            result = x.search(term=args.term, datefrom=date_after, dateto=date_before, buckets=['leaks.logs'], maxresults=1000) 
            now = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
            domains.setdefault(now, [args.term])
        
        if args.filepath:
            if os.path.isfile(args.filepath):
                domains = leakP.read_domain_file(args.filepath)
            else:
                print("[-] No filepath finded")
                exit()
            
        for key, items in domains.items():
            if args.filepath:
                print(key) # Domains key
            word_len = len(key)
            output.write(f"#" * (word_len + 6))
            output.write('\n')
            output.write(f"## {key} ##")
            output.write('\n')
            output.write(f"#" * (word_len + 6))
            output.write('\n')

            domain_path = corvo_path / key
            if not Path.exists(domain_path):
                os.makedirs(domain_path)
            
            file_checked = []
            for term in items:
                result = x.search(term=term, datefrom=date_after, dateto=date_before, buckets=['leaks.logs'], maxresults=1000)
                if not result['records']:
                    ## WRITE OUTPUT ##
                    output.write(f'Company Leaks (0) - {term}\n')
                    output.write(f'Client Leaks (0) - {term}\n')
                    output.write('\n')
                    output.write(f'Total group names: None')
                    output.write('\n\n')
                    continue

                if args.debugger:
                    print(f"Total citations [{term}]: {len(result['records'])}")

                for item in result['records']:
                    filename = leakP.filter_filename(item['name'])
                    date = item['date']
                    bucket = item['bucket']
                    id = item['systemid']
                    storageID = item['storageid']
                    indexfile = item['indexfile']
                
                    tree = ""
                    if 'passwords' not in filename.lower() or 'pass' not in filename.lower():
                        if args.reduce_queries:
                            continue
                        if args.debugger:
                            print(f"Checking the {filename}::{id} tree")
                        tree = x.FILE_TREE_VIEW(indexfile, bucket)
                        result_tree = leakP.parser_tree_files(tree)
                        password_file = [{key: value} for key, value in result_tree.items() if 'password' in key.lower() and '-' not in key.lower()]
                        if password_file:
                            filename = leakP.filter_filename(list(password_file[0].keys())[0])
                            storageID = list(password_file[0].values())[0]
                            id = storageID
                            if args.debugger:
                                print(f"Find out the leaks file in the tree: {filename}::{id}")
                        else:
                            continue
                        

                    if args.debugger:
                        print(f"{date}::{filename}={id}")
                    
                    compose_filename = filename + '_' + id
                    abs_path = os.path.join(domain_path, compose_filename)
                    
                    if id in file_checked:
                        continue
                    file_checked.append(id)

                    x.FILE_READ(id, 0, bucket, abs_path)

                    try:
                        file_content = Path(abs_path).read_text()
                    except Exception as err:
                        print(f"Error at file: {id}")
                        print(err)

                    term_leaks = leakP.filter_domain_leak(file_content, [term])

                    if not term_leaks:
                        print(f"Unknown pattern for file: {id}")
                        term_leaks = {'company':[], 'client': []}                 
                        
                    if args.debugger:
                        print(term_leaks)
                    
                    company_leak = [*company_leak, *term_leaks.get('company', [])]
                    client_leak = [*client_leak, *term_leaks.get('client', [])]
                  
                    if not company_leak and not client_leak:
                        continue
                    
                    if filename.lower() in group_name_file:
                        file_group = [content for key, value in group_name_file.items() for item in value if item in content.lower()]
                        content = x.selectors(id, bucket)
                        
                        group_name = leakP.check_group_name(content)
                        if group_name:
                            total_group_names.setdefault(group_name, 0)
                            total_group_names[group_name] += 1
                            continue

                    else:
                        if not tree:
                            tree = x.FILE_TREE_VIEW(indexfile, bucket)
                        result_tree = leakP.parser_tree_files(tree)
                        tree_files = [{key: value} for key, value in result_tree.items() for key2, value2 in group_name_file.items() if key2 in key.lower() and '-' not in key.lower()]
                        
                        if tree_files:
                            for tree_item in tree_files:
                                for key, value in tree_item.items():
                                    content = x.selectors(value, bucket)
                                    group_name = leakP.check_group_name(content)

                                    if not group_name:
                                        result_file_tree = x.search(term=value, datefrom=date_after, dateto=date_before, buckets=['leaks.logs'], maxresults=20)
                                        time.sleep(1.5)
                                        try:
                                            file_tree_storageid = result_file_tree['records'][0]['storageid']
                                        except Exception as err:
                                            break
                                        file_fist_20_lines = x.FILE_PREVIEW(ctype=1, mediatype=24, format=0, sid=file_tree_storageid, bucket=bucket, lines=20 )
                                        group_name = leakP.check_group_name(file_fist_20_lines)
                                    
                                    if group_name:
                                        total_group_names.setdefault(group_name, 0)
                                        total_group_names[group_name] += 1
                                        break
                                if group_name:
                                    break
                        if not group_name:
                            total_group_names.setdefault('unknown', 0)
                            total_group_names['unknown'] += 1
                    
                    if args.debugger:
                        print(f"GroupName: {group_name}")

                ## WRITE OUTPUT ##
                output.write(f'Company Leaks ({len(company_leak)}) - {term}\n')
                if company_leak:
                    for item in company_leak:
                        output.write(json.dumps(item) + '\n')
                output.write('\n')
                output.write(f'Client Leaks ({len(client_leak)}) - {term}\n')
                if client_leak:
                    for item in client_leak:
                        output.write(json.dumps(item) + '\n')
                output.write('\n\n')
                output.write(f'Total group names: {total_group_names}')
                output.write('\n\n')
                print(f'Total group names: {total_group_names}')
                #print(f'Convert group names: {leakP.convert_group_names(total_group_names)}')
                company_leak = []
                client_leak = []
            
            total_group_names = {}
            

        print('Check the result at corvo.leaks file')

if __name__ == "__main__":
    main()