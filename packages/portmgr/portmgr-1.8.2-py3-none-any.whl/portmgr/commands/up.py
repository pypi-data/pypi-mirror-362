from portmgr import command_list, bcolors, runCompose

def func(action):
    directory = action['directory']
    relative = action['relative']

    res = runCompose(["up", "-d"])
    # p = subprocess.Popen(["docker-compose", "up", "-d"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # out, err = p.communicate()

    # if out != "":
       # print(out.decode("UTF-8"))

    if res != 0:
        print("Error creating " + relative + "!")
    
    # print(bcolors.FAIL + err.decode("UTF-8") + bcolors.ENDC)

    return 0

command_list['u'] = {
    'hlp': 'Create container',
    'ord': 'nrm',
    'fnc': func
}
