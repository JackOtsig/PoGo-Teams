import urllib.request
import json
import os
import argparse as arg

parser = arg.ArgumentParser()
parser.add_argument('-s', help='specifies that you are merely starting a container(don\'t use with -c)', type=str)
args = parser.parse_args()

def file_structure():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    if not os.path.isdir('pogoapi'):
        os.mkdir('pogoapi')
    file_location = dir_path + '\pogoapi'
    return file_location



def get_data():
    os.chdir(file_structure())
    with urllib.request.urlopen('http://pogoapi.net/api/v1/api_hashes.json') as url:
        data = json.loads(url.read().decode())
    return data

def get_single_data(file):
    os.chdir(file_structure())
    with urllib.request.urlopen('http://pogoapi.net/api/v1/'+str(file)) as url:
        print(file, 'found!')
        data = json.loads(url.read().decode())
        f = open(str(file), 'w')
        u = json.dumps(data)
        f.write(u)
        f.close()

def index_dict_lol():
    os.chdir(file_structure())
    data = get_data()
    for item in data:
        print(item)
        with urllib.request.urlopen('http://pogoapi.net/api/v1/'+str(item)) as url:
            z = json.loads(url.read().decode())
            f = open(str(item), 'w')
            u = json.dumps(z)
            f.write(u)
            f.close()



def main():
    if args.s:
        get_single_data(args.s)
    else:
        index_dict_lol()
    print('done!')

if __name__ == "__main__":
    main()