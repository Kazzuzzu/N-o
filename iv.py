import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class TipoTransacao:
    DEPOSITO = "deposito"
    SAQUE = "saque"


    
def menu():
    menu ='''\n

    ===== MENU =====
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova Conta
    [5]\tListar Contas
    [6]\tNovo usuario
    [0]\tSair
    =>'''

    return  input(textwrap.dedent(menu))



def listar_contas(contas):
  for conta in contas:
    print(" " * 100)
    print(textwrap.dedent(str(conta)))



def filtrar_cliente(cpf, clientes):
  clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
  return clientes_filtrados[0] if clientes_filtrados else None

def depositar(clientes):
  cpf = input("Informe o seu CPF: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("\n@@@ Cliente não encontrado! @@@")
    return

  valor = float(input("Informe o valor a ser depositado: "))
  transacao = Depositar(valor)

  conta = recuperar_a_conta_do_cliente(cliente)
  if not conta:
    return

  cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
  cpf = input("Informe o seu CPF: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("\n@@@ Cliente não encontrado! @@@")
    return

  valor = float(input("Informe o valor a ser sacado: "))
  transacao = Saque(valor)

  conta = recuperar_a_conta_do_cliente(cliente)
  if not conta:
    return

  cliente.realizar_transacao(conta, transacao)

def extrato(clientes):
  cpf = input("Informe o seu CPF: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("\n@@@ Cliente não encontrado! @@@")
    return
  conta = recuperar_a_conta_do_cliente(cliente)
  if not conta:
    return

  print("\n@@@ Extrato Conta Corrente @@@")
  transacoes = conta.historico.transacoes

  extrato = ""

  if not transacoes:
    extrato = "Não foram realizadas movimentações."
  else:
    extrato = ""
    for transacao in transacoes:
      extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    

  print(extrato)
  print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
  print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")



def recuperar_a_conta_do_cliente(cliente):
  if not cliente.contas:
    print("\n@@@ Você não possui uma conta conosco! @@@")
    return


  return cliente.contas[0]

def criar_cliente(clientes):
  cpf = input("Informe o CPF: ")
  cliente = filtrar_cliente(cpf, clientes)

  if cliente:
    print("\n@@@ Já existe cliente com esse CPF! @@@")
    return


  nome = input("Informe o nome completo: ")
  data_nascimento = input("Informe sua data de nascimento (dia/mês/ano): ")
  endereco = input("Informe o endereço a qual reside (rua, N/ Bairro / Cidade / Estado): ")


  cliente = Fisico(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

  clientes.append(cliente)
  print("\n@@@ Cliente criado com sucesso! @@@")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, criação de conta encerrado! @@@")
        return
    
    conta = ContaCorrente.nova_conta(cliente = cliente, numero = numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\n@@@ Conta criada com sucesso! @@@")


#cliente, conta e cliente fisico



class Cliente:
    def __init__(self, endereço):
        self.contas = []
        self.endereço = endereço

    def realizar_transacao(self,conta, transacao):
      transacao.registrar(conta)

    def adicionar_conta(self, conta):
      self.contas.append(conta)


class Fisico(Cliente):
  def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
  def __init__(self, numero, cliente):
    self._saldo = 0
    self._numero = numero
    self._agencia = "0001"
    self._cliente = cliente
    self._historico = Historico()



  @classmethod
  def nova_conta(cls, cliente, numero):
    return cls(numero, cliente)

  @property
  def saldo(self):
    return self._saldo



  @property
  def numero(self):
    return self._numero

  @property
  def angencia(self):
    return self._agencia

  @property
  def cliente(self):
    return self._cliente

  @property
  def historico(self):
      return self._historico



  def sacar(self, valor):
    saldo = self.saldo
    excedendo_saldo = valor > saldo
    
    if excedendo_saldo:
        print("\n@@@ Não foi possivel realizar esta Operação. Saldo não suficiente. @@@")
        
    elif valor > 0:
        self._saldo -= valor
        print("\n@@@ Saque realizado com susseco. @@@")
        
    else:
        print("\n@@@ Não foi possivel realizar esta Operação. O valor não é valido. ")
        
    return False


  def depositar(self, valor):
    if valor > 0:
        self._saldo += valor
        print ("\n@@@ Deposito realizado. @@@")
        
    else:
        print("\n@@@ Não foi possivel realizar esta Operação. O valor não é valido. @@@")
        
    return True

class ContaCorrente(Conta):
  def __init__(self,numero, cliente, limite=500, limite_de_saque=3):
    super().__init__(numero, cliente)
    self._limite = limite
    self._limite_de_saque = limite_de_saque

  def sacar(self, valor):
    
    numero_de_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == TipoTransacao.SAQUE]) 
    excedendo_limite = valor > self._limite
    excedendo_saques = numero_de_saques >= self._limite_de_saque

    if excedendo_limite:
        print("\n@@@ Não foi possivel realizar esta Operação. O limite diario foi excedido. @@@")
    
    elif excedendo_saques:
        print("\n@@@ Não foi possivel realizar esta Operação. O limite de saque diario foi excedido. @@@")

    else:
      return super().sacar(valor)

    return False

  def __str__(self):
    return f"""\
            Agência:\t{self._agencia}  # Use _agencia instead of agencia
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
class Transacao(ABC):
  @property
  @abstractmethod
  def valor(self):
    pass

  def __init__(self, valor, tipo):
    self._valor = valor
    self._tipo = tipo

  @abstractmethod
  def registrar(self, conta):
    pass       

class Depositar(Transacao):
  def __init__(self, valor):
    super().__init__(valor, TipoTransacao.DEPOSITO)

  @property
  def valor(self):
    return self._valor

  def registrar(self, conta):
    e = conta.depositar(self.valor)

    if e:
      conta.historico.registrar_transacao(self)

class Historico:
  def __init__(self):
    self._transacoes = []  

  @property
  def transacoes(self):
    return self._transacoes

  def registrar_transacao(self, transacao):
    self._transacoes.append({
                             "tipo": transacao._tipo, 
                             "valor": transacao.valor,
                             "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"), 
    })


class Saque(Transacao):
  def __init__(self, valor):
    super().__init__(valor, TipoTransacao.SAQUE)

  @property
  def valor(self):
    return self._valor
  
  def registrar(self, conta):
    e = conta.sacar(self.valor)

    if e:
      conta.historico.registrar_transacao(self)



def main():
    clientes = []
    contas = []
    while True:
        opcao = menu()
        if opcao == '1': 
            depositar(clientes)

        elif opcao == '2':
            sacar(clientes)

        elif opcao == '3':
            extrato(clientes)

        elif opcao == '4':
          conta1 = len(contas) + 1
          criar_conta(conta1, clientes, contas)
            
        elif opcao == '5':
            listar_contas(contas)

        elif opcao == '6':
            criar_cliente(clientes)

        elif opcao == "0":
            break

        else:
            print("\n@@@ Não possivel realizar esta Operação, Seleciona novamente uma outra opção. @@@")

main()

























def main():


  while True:

    opcao = menu()




main()