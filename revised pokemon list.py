import os, json
dir_path = str(os.path.dirname(os.path.realpath(__file__)))

def file_structure():
    os.chdir(dir_path)
    file_location = dir_path
    return file_location

def main():
    os.chdir(dir_path+'\pogoapi')
    f = open('pokemon_types.json','r')
    pokemon_types = json.load(f)
    f.close()
    pokemon_list = []
    for pokemon in pokemon_types:
        if pokemon['form'] == 'Normal':
            pokemon_list.append(pokemon)
            print(pokemon['pokemon_name'])
    os.chdir(dir_path+'\pogoteams')
    f = open('pokemon_types_revised.json', 'w')
    u = json.dumps(pokemon_list)
    f.write(u)
    print('done!')
    f.close()

if __name__ == '__main__':
    main()