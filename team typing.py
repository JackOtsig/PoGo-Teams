import os, json, time, multiprocessing, sys
from collections import OrderedDict
dir_path = os.path.dirname(os.path.realpath(__file__))



def file_structure():
    os.chdir(dir_path)
    if not os.path.isdir(str(dir_path)+'\pogoteams'):
        os.mkdir('pogoteams')
    file_location = dir_path
    return file_location

def test_function(b):
    print(b)
    sys.stdout.flush()

def pokemon1f(pokemon1, pokemon_types, lock):
    teams_list = []
    for pokemon2 in range(pokemon1+1,len(pokemon_types)-1):
        if pokemon_types[pokemon2]['form'] != 'Normal' or pokemon1 == pokemon2:
            continue
        for pokemon3 in range(pokemon2+1,len(pokemon_types)):
            if pokemon_types[pokemon3]['form'] != 'Normal' or pokemon2 == pokemon3 or pokemon1 == pokemon3:
                continue
            teams_list.append([pokemon1,pokemon2,pokemon3])
            team_index = len(teams_list)
            table = [team_index,  pokemon_types[pokemon1]['pokemon_name'], pokemon_types[pokemon2]['pokemon_name'], pokemon_types[pokemon3]['pokemon_name']]
            index, pkm1, pkm2, pkm3 = table
            print('{:<12} {:<15} {:<15} {:<15}'.format(index, pkm1, pkm2, pkm3))
            sys.stdout.flush()
    lock.acquire()
    f = open('teamsraw.txt', 'a')
    for team in teams_list:
        u = json.dumps(team)
        f.write(u)
        f.write('\n')
        print(team)
    f.close()
    lock.release()

def get_teams(manager):
    global pokemon_types, start
    start = time.perf_counter()
    json_location = str(file_structure())+'\pogoteams'
    os.chdir(json_location)
    f = open('pokemon_types_revised.json', 'r')
    pokemon_types = json.load(f)
    thread_list = []
    teams_list = []
    index = 0
    l = manager.Lock()
    for i in range(len(pokemon_types)-2):
        if pokemon_types[i]['form'] != 'Normal':
            continue
        loop = True
        t = multiprocessing.Process(target=pokemon1f, args=(i, pokemon_types, l,))
        thread_list.append(t)
        while loop:
            try:
                multiprocessing.freeze_support()
                t.start()
                index += 1
                loop = False
            except:
                pass
    for thread in thread_list:
        thread.join()
    duration = time.perf_counter() - start 
    print('done ! finished in: '+ str(duration))

def teams_as_list():
    f = open(str(dir_path)+r'\pogoteams\teamsraw.txt')
    teams_list = []
    teams = f.read()
    teams = teams.split('\n')
    teams = teams[:-1]
    for team in teams:
        team = team[1:]
        team = team[:-1]
        team_final = ''
        for character in team:
            if not character == ' ':
                team_final += character
        team = team_final.split(',')
        teams_list.append(team)
    return teams_list

def team_types():
    team_types = []
    f = open(str(dir_path)+r'\pogoteams\pokemon_types_revised.json')
    pokemon_types = json.load(f)
    for team in teams_as_list():
        team_type_list = []
        for pokemon in team:
            team_type_list.append([pokemon, pokemon_types[int(pokemon)]['type']])
        team_types.append(team_type_list)
    return team_types

def process_team_types():
    team_types_full = team_types()
    teams_types = []
    for team in team_types_full:
        types = []
        types_final = []
        for pokemon in team:
            for item in pokemon[1]:
                types.append(item)
        for i in types:
            if i not in types_final:
                types_final.append(i)
                team_final = [team, types_final]
                teams_types.append(team_final)
    return teams_types
        
def get_strengths_and_weaknesses():
    team_types_list = process_team_types()
    f = open(str(dir_path)+r'\pogoapi\type_effectiveness.json')
    type_effect = json.load(f)
    for team in team_types_list:
        final_list = []
        for team_individual_type in team[1]:
            itype = team_individual_type
            for attacking_type in type_effect:
                type_effectiveness_per_type = attacking_type.get(team_individual_type)
            type_num = {itype:type_effectiveness_per_type}
            final_list.append(type_num)
            print(type_num)
                
                
    #index = 0
    # for team in team_types_list:
    #     team_final = []
    #     types = team[1]
    #     resistance = []
    #     weakness = []
    #     for team_individual_type in types:
    #         for defending_type in type_effect[team_individual_type]:
    #             if type_effect[team_individual_type].get(defending_type) > 1:
    #                 weakness.append(defending_type)
    #             if type_effect[team_individual_type].get(defending_type) < 1:
    #                 resistance.append(defending_type)
    #             else:
    #                 pass
    #         print('type done!')
    #     r_final = []
    #     w_final = []
    #     for i in resistance:
    #         if i not in r_final:
    #             r_final.append(i)
    #     for i in weakness:
    #         if i not in w_final and i not in r_final:
    #             w_final.append(i)
    #     print(index, team, 'team done!')
    #     index += 1
    #     team_append = [team, [r_final, w_final]]
    #     team_final.append(team_append)
    # for item in team_final:
    #     print(item)


        




def main():
    get_strengths_and_weaknesses()
    #manager = multiprocessing.Manager()
    #get_teams(manager)

if __name__ == '__main__':
    main()