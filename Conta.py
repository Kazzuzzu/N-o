import textwrap



#novo usuário
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o seu nome completo: ")
    data_nascimento = input("Informe a sua data de nascimento (dia/mês/ano): ")
    endereco = input("Informe o endereço (Rua, numero - bairro - cidade/sigla do estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("===== Usuário criado com sucesso! =====")
    
    
    
# filtrar usuario
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None
       
    
    
    
#nova conta
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, portanto a criação de conta será encerrada! @@@")
    
    
#Listar contas

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

        
             


#depósito
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor 
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n===== Depósito realizado com sucesso! =====")
    
    else:
        print("\n@@@ Impossivel realizar a operação, o valor informado não é valido. @@@")
        
    return saldo, extrato
        
              

#saque
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor >saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >=limite_saques
    
    
    if excedeu_saldo:
        print("\n@@@ Impossivel realizar a operação, você não tem saldo em conta suficiente. @@@")
        
    elif excedeu_limite:
        print("\n@@@ Impossivel realizar a operação, o valor do saque solicitado excede o limite! @@@")
        
    elif excedeu_saques:
        print('\n@@@ Impossivel realizar a operação, você já realizou o numero maximo de saques permitido! @@@')
        
        
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n===== Saque realizado com sucesso! =====")
        
        
    else:
        print("\n@@@ Impossivel realizar a operação, o valor informado não é valido. @@@")
        
    return saldo, extrato
    
    

# extrato
def exibir_extrato(saldo, /, *, extrato):
    print("\n ====== EXTRATO ======")
    print("Não foram realizadas movimentações na conta." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("========================")
     
    
# menu
def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """

    
    
    return input(textwrap.dedent(menu))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()