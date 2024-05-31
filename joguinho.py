inimigos = {'minion 1':[50, 10], 'minion 2':[100, 5], 'boss 1':[200, 20], 'minion 3':[10, 100], 'boss 2':[1000, 1]}
player = {'mago':[240, 35], 'guerreiro':[400, 25], 'ladino':[200, 20]}
ini1 = 'minion 1'
ini2 = 'boss 1'
ini3 = 'minion 2'
def batalha():
    if hp1 > 0: 
        print('\n\n\n',ini1,'\nATK = ',atk1,'\nHP = ',hp1,'\n', sep='')
    else:
        print('\n\n\n',ini1,'\nMorto\n', sep='')
    if hp2 > 0: 
        print(ini2,'\nATK =',atk2,'\nHP =',hp2,'\n')
    else:
        print(ini2,'\nInimigo morto\n')
    if hp3 > 0: 
        print(ini3,'\nATK =',atk3,'\nHP =',hp3,'\n\n\n')
    else:
        print(ini3,'\nInimigo morto\n')
    if hp > 0:
        print(classe,'\nATK =',atk,'\nHP =',hp,'\n')
    else:
        print('Você foi \nderrotado(a)\n')

esc = False
while not esc:
    atk1 = inimigos.get(ini1)[1]
    hp1 = inimigos.get(ini1)[0]
    pos1 = True
    atk2 = inimigos.get(ini2)[1]
    hp2 = inimigos.get(ini2)[0]
    pos2 = True
    atk3 = inimigos.get(ini3)[1]
    hp3 = inimigos.get(ini3)[0]
    pos3 = True

    while True:
        classe = input('\nescolha sua classe (mago, guerreiro, ladino)\n')
        if classe in player.keys():
            break
    atk = player.get(classe)[1]
    hp = player.get(classe)[0]

    while True:
        batalha()
        if pos1 == False and pos2 == False and pos3 == False:
            break
        if hp <= 0:
            break

        while True:
            alvo = input('digite a posição que deseja atacar (1, 2 ou 3)\n')
            if alvo.isnumeric():
                alvo = int(alvo)
            if alvo == 1 and pos1 == True:
                hp1 += -atk
                break
            elif alvo == 2 and pos2 == True:
                hp2 += -atk
                break
            elif alvo == 3 and pos3 == True:
                hp3 += -atk
                break
            else:
                print('alvo inexistente')
        if classe == 'ladino':
            while True:
                print('ataque extra de ladino')
                alvo = input('digite a posição que deseja atacar (1, 2 ou 3)\n')
                if alvo.isnumeric():
                    alvo = int(alvo)
                if alvo == 1 and pos1 == True:
                    hp1 += -atk
                    break
                elif alvo == 2 and pos2 == True:
                    hp2 += -atk
                    break
                elif alvo == 3 and pos3 == True:
                    hp3 += -atk
                    break
                else:
                    print('alvo inexistente')

        if hp1 <= 0:
            pos1 = False
        if hp2 <= 0:
            pos2 = False
        if hp3 <= 0:
            pos3 = False
        if pos1 == True:
            hp += -atk1
        if pos2 == True:
            hp += -atk2
        if pos3 == True:
            hp += -atk3

    print('\n\n\n\n','você ganhou' if hp >= 0 else 'você perdeu', sep='')
    while True:
        esc = input('deseja continuar jogando? S/N\n')
        if esc == 'N':
            esc = True
            break
        if esc == 'S':
            break