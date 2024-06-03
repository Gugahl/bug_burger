import os
lista_comidas = {'x-tudo':[0, 10], 'x-presuntão':[2, 40], 'x-bacon':[4, 15], 'x-monster':[6, 20]} #num 1 = pos no arquivo, num 2 = valor da comida
fim = False
while fim == False:
    pedidos = []

    while True:
        quantidade = input('\nquantos pedidos são?\n')
        if quantidade.isnumeric():
            quantidade = int(quantidade)
            if quantidade > 0:
                break
            else:
                print('quantidade inválida!')
        else:
            print('quantidade inválida!')

    quant_rest = quantidade
    while quant_rest > 0:
        pedido = input('\ndigite o pedido: ')
        if pedido in lista_comidas:
            pos_ordem = lista_comidas.get(pedido)[0]
            file_estoque = open('projeto/comidas.txt', 'r')
            quant_comid = file_estoque.read()[pos_ordem:pos_ordem+2] #verifica a quantidade no estoque
            file_estoque.close()
            if quant_comid[0] == '0': #remover o 0 do começo da quantidade pra não dar erro (tipo se for 01, daria erro)
                quant_comid = quant_comid[1]
            if int(quant_comid) != 0:
                quant_rest += -1
                pedidos.append(pedido)
            else:
                print('não há mais no estoque')
        else:
            print('pedido inválido!')

    valor_ordem = 0
    x = 0
    for i in pedidos:
        valor_ordem += lista_comidas.get(pedidos[x])[1] #verificando valor de cada produto
        x += 1
    print(f'\n\no valor da ordem do cliente é de R$ {valor_ordem},00')
    while True:
        pagamento = input('digite o valor do pagamento do cliente: ')
        if pagamento.isnumeric():
            pagamento = int(pagamento)
            if pagamento >= valor_ordem:
                print(f'pagamento realizado!\no troco é de R$ {pagamento-valor_ordem},00')
                break

    fim = input('deseja realizar outro pedido? S/N\n')
    while True:
        if fim == 'S' or fim == 's':
            break
        if fim == 'N' or fim == 'n':
            fim = True
            print('fim de programa')
            break

#partes que faltam: diminuir a quantidade dentro do estoque sempre que realizar um pedido; opção de adicionar algo no estoque