import re 
import configparser
import os

class Leaks:
    def __init__(self) -> None:
        pass

    def check_group_name(self, data):
        """
        Expected receive the output of selector in pages
        """
        count = 0 # Check if only exists one telegram link at the file
        group_name = ''
        telegram_url_pattern = r'(https?://)?t\.me/([A-Za-z0-9_+-]+)'

        if isinstance(data, list):
            for item in data:
                if item['type'] == 3:
                    matches = re.findall(telegram_url_pattern, item['selector'])
                    
                    if len(matches) == 1:
                        count += 1
                        group_name = matches[0][1]      

            if count == 1:
                return group_name
        elif isinstance(data, str):
            matches = re.findall(telegram_url_pattern, data)
            if len(matches) == 1:
                        count += 1
                        group_name = matches[0][1]      

            if count == 1:
                return group_name
            
            if not group_name:
                first_line = data.splitlines()[0]
                pattern_header_malwares = r'^[^a-zA-Z0-9]*\*{10,}[^a-zA-Z0-9]*$' # *******
                pattern_first_line = r' @([a-zA-Z0-9_-]+)' # search for ' @threat_Actor'
                pattern_telegram = r'Telegram: *@(\w+)'
                pattern_telegram_url = r' t.me\/([\w_-]+)'

                if re.match(pattern_header_malwares, first_line):
                    match = re.search(telegram_url_pattern, data)
                    match_telegram = re.search(pattern_telegram, data)

                    if match and match.group(2):
                        return match.group(2)
                    
                    elif match_telegram and match_telegram.group(1):
                        return match_telegram.group(1)

                match = re.search(pattern_first_line, first_line)
                if match and match.group(1):
                    return match.group(1)
        return None

    def convert_group_names(self, data:dict) -> dict:
        group_names = {
            '+IqEnwfj7CLU1Yjcy': 'RedLine',
            '+ll-i0WgcnqYwMjI0': 'Ottoman',
            'REDLINESELLER': 'RedLine',
            'OmegaCloud_FreeLogs': 'OmegaCloud',
            'Omega_Cloud_Admin': 'OmegaCloud'
        }
        new = {}

        for key, value in data.items():
            if key in group_names.keys():
                new.setdefault(group_names[key], 0)
                new[group_names[key]] += value
            else:
                new.setdefault(key, value)

        return new

    def replace_match(self, match):
        return match.group(1)

    def filter_filename(self, filename:str) -> str:
        """
        Remove whitespace and '/' 
        """
        filename = filename.strip().replace(' ', '')

        remove_char = ''
        if remove_char in filename:
            filename = filename.split(remove_char)[-1]

        if '/' in filename:
            filename = filename.split('/')[-1]
        if '\\' in filename:
            filename = filename.split('\\')[-1]
        return filename
    
    def filter_domain_leak(self, content:str, domains:list) -> dict:
        domains_match_company = []
        domains_match_client = []
        company_leak = []
        client_leak = []
        
        for domain in domains:
            pattern_password_01 = r'URL:\s([\S*]+).*?\nUsername:\s(\S*).*?\nPassword:\s([\S*]+).*?\nApplication:\s([\S*]+)'
            pattern_password_02 = r'browser:\s([\w ]+).*?\nprofile:\s([\w]+).*?\nurl:\s([\S*]+).*?\nlogin:\s([\S*]+).*?\npassword:\s([\S*]+)'
            pattern_password_03 = r'SOFT:\s([\S* ]+).*?\nURL:\s([\S*]+).*?\nUSER:\s([\S* ]+).*?\nPASS:\s([\S*]+)'
            pattern_password_04 = r'SOFT:\s([\S*]+).*?\nHost:\s([\S*]+).*?\nLogin:\s([\S*]+).*?\nPassword:\s([\S*]+)'
            pattern_password_05 = r'Browser:\s([\S*]+).*?\nUrl:\s([\S*]+).*?\nUsername:\s([\S*]+).*?\nPassword:\s([\S*]+)'

            matches_01 = re.findall(pattern_password_01, content, re.IGNORECASE)
            if matches_01:
                for match in matches_01:
                    url = match[0]
                    username = match[1]
                    password = match[2]
                    app = match[3]
                    
                    if domain in username.lower():
                        domains_match_company.append({'url': url, 'username': username, 'password': password, 'application': app})
                    elif domain in url.lower() or domain in app.lower():
                        domains_match_client.append({'url': url, 'username': username, 'password': password, 'application': app})
                company_leak = [*company_leak, *domains_match_company]
                client_leak = [*client_leak, *domains_match_client]
            matches_02 = re.findall(pattern_password_02, content, re.IGNORECASE)
            if matches_02:
                for match in matches_02:
                    browser = match[0]
                    profile = match[1]
                    url = match[2]
                    login = match[3]
                    password = match[4]
                    if domain in login.lower():
                        domains_match_company.append({'browser': browser, 'profile': profile, 'url': url, 'login': login, 'password': password})
                    elif domain in url.lower():
                        domains_match_client.append({'browser': browser, 'profile': profile, 'url': url, 'login': login, 'password': password})
                company_leak = [*company_leak, *domains_match_company]
                client_leak = [*client_leak, *domains_match_client]
            matches_03 = re.findall(pattern_password_03, content, re.IGNORECASE)
            if matches_03:
                for match in matches_03:
                    soft = match[0]
                    url = match[1]
                    user = match[2]
                    password = match[3]
                    if domain in user.lower():
                        domains_match_company.append({'soft': soft, 'url': url, 'username': user, 'password': password})
                    elif domain in soft.lower() or domain in url.lower():
                        domains_match_client.append({'soft': soft, 'url': url, 'username': user, 'password': password})
                company_leak = [*company_leak, *domains_match_company]
                client_leak = [*client_leak, *domains_match_client]
            matches_04 = re.findall(pattern_password_04, content, re.IGNORECASE)
            if matches_04:
                for match in matches_04:
                    soft = match[0]
                    host = match[1]
                    user = match[2]
                    password = match[3]
                    if domain in user.lower():
                        domains_match_company.append({'soft': soft, 'host': host, 'username': user, 'password': password})
                    elif domain in soft.lower() or domain in host.lower():
                        domains_match_client.append({'soft': soft, 'host': host, 'username': user, 'password': password})
                company_leak = [*company_leak, *domains_match_company]
                client_leak = [*client_leak, *domains_match_client]
            matches_05 = re.findall(pattern_password_05, content, re.IGNORECASE)
            if matches_05:
                for match in matches_05:
                    browser = match[0]
                    url = match[1]
                    user = match[2]
                    password = match[3]
                    if domain in user.lower():
                        domains_match_company.append({'browser': browser, 'url': url, 'username': user, 'password': password})
                    elif domain in url.lower():
                        domains_match_company.append({'browser': browser, 'url': url, 'username': user, 'password': password})
                company_leak = [*company_leak, *domains_match_company]
                client_leak = [*client_leak, *domains_match_client]
        if company_leak or client_leak:
            return {'company': domains_match_company, 'client': domains_match_client}
        return {}
    

    def parser_tree_files(self, tree_content) -> dict:
        did_pattern = r'<a[^>]*href="[^"]*did=([^"&]*)[^>]*>(.*?)</a>'
        matches = re.findall(did_pattern, tree_content)
        if matches:
            result_tree = {content: did for did, content in matches}
            return result_tree
        else:
            {}

    def read_domain_file(self, filepath:str) -> dict:
        domains = {}
        if os.path.exists(filepath):
            config = configparser.ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})
            config.read(filepath)

            filenames_domain = [x for x in config['DOMAINS']]
            for name in filenames_domain:
                list_items = [x for x in config['DOMAINS'][name].replace(' ', '').split(',')]
                domains.setdefault(name, list_items) 
            return domains