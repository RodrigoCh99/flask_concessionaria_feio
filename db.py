# Importando biblioteca para manipulação de Banco de Dados:
from flaskext.mysql import MySQL
import os


# função para configurar o acesso ao banco
def config(app):
    # Configurando o acesso ao MySQL
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'concessionaria'


# funação que retorna a conexão e o cursor:
def get_db(mysql):
    # Obtendo a concxão para acessar o BD
    conn = mysql.connect()
    # Obtendo o cursor para acessar o BD
    cursor = conn.cursor()
    # retornando a conexão e o cursor:
    return conn, cursor


# função que retorna se o login enviado está na tabela adm, caso esteja retorna seu ID
def get_idadm(cursor, login, senha):
    # Executar o sql
    cursor.execute(f'select idadministrador from administrador where login = "{login}" and senha = "{senha}"')

    # Recuperando o retorno do BD
    idadm = cursor.fetchone()

    # Retornar o idlogin
    return idadm


# função que retorna se o login enviado está na tabela funcionario, caso esteja retorna seu ID
def get_idfun(cursor, login, senha):
    # Executar o sql
    cursor.execute(f'select idfuncionario from funcionario where login = "{login}" and senha = "{senha}"')

    # Recuperando o retorno do BD
    idfun = cursor.fetchone()

    # Retornar o idlogin
    return idfun


# função que retorna a lista de funcionarios do banco de dados
def get_fun(cursor):
    # Executar o sql
    cursor.execute(f'select idfuncionario, login, senha from funcionario')

    # Recuperando o retorno do BD
    lista_fun = cursor.fetchall()

    # retorna a lista de funcionarios:
    return lista_fun


# função que retorna a lista de carros do banco de dados
def get_carros(cursor):
    # Executar o sql
    cursor.execute(f'select * from carros where vip = "N" and reservado = "N"; ')

    # Recuperando o retorno do BD
    lista_car = cursor.fetchall()

    # retorna a lista de funcionarios:
    return lista_car


# função que adiciona um novo funcionario ao banco de dados
def add_new_func(conn, cursor, novo_login, nova_senha):
    # Executar o sql
    cursor.execute(f'INSERT INTO `concessionaria`.`funcionario` (`login`, `senha`) VALUES ("{novo_login}", "{nova_senha}");')

    # efetivar adição
    conn.commit()


# função que deleta o funcionario do Banco de Dados
def del_func(conn, cursor, id):
    # Executar o SQL
    cursor.execute(f'DELETE from funcionario WHERE idfuncionario = { id }')

    # efetivar exclusão
    conn.commit()


# função que deleta o anuncio do Banco de Dados
def del_anun(conn, cursor, id):
    # Executar o SQL
    cursor.execute(f'DELETE from carros WHERE idcarros = { id }')

    # efetivar exclusão
    conn.commit()


# função que altera os dados do funcionario
def alter_func(conn, cursor, updated_login, updated_senha, id):
    cursor.execute(f'UPDATE funcionario SET login = "{updated_login}", senha ="{updated_senha}" WHERE idfuncionario= { id }')
    # print(f'novo login: {updated_login}, nova senha: {updated_senha} no id: {id}')
    # efetivar alteração
    conn.commit()


# função que pega informações do funcionario para preencher formulario
def info_func(cursor, id):
    cursor.execute(f'select * from funcionario where idfuncionario = { id }')

    # Recuperando o retorno do BD
    dados = cursor.fetchone()

    print(dados)

    return dados


# função que altera o estado do carro, seta se ele é ou não VIP
def vip(conn, cursor, id, estado):
    cursor.execute('select * from carros where vip = "S";')
    quantidade = cursor.fetchall()
    print(f'Quantidade: {quantidade}')

    if estado == 'N':
        if len(quantidade) < 10:
            cursor.execute(f'UPDATE carros SET vip= "S" WHERE idcarros={ id }')
            # efetivar alteração
            conn.commit()

        else:
            erro = 'A lista vip está cheia! remova um carro para adicionar este!'
            return erro

    elif estado == 'S':
        cursor.execute(f'UPDATE carros SET vip= "N" WHERE idcarros= { id }')
        # efetivar alteração
        conn.commit()


# funçãp para adicionar carros:
def add_new_car(conn, cursor, modelo, marca, ano, preco, img):
    # Executar o sql
    cursor.execute(f'INSERT INTO carros ( modelo, marca, ano, reservado, preco, vip, img) VALUES ( "{ modelo }", "{ marca }", "{ano}", "N", "{ preco }", "N", "{ img }" )')
    # print(f'os dados dentro do banco são: "{ modelo }", "{ marca }", "{ano}", "N", "{ preco }", "{ vip }", "{ img }" ')
    # efetivar adição
    conn.commit()


# funçãoque retorna todos os carros com a vriavel vip = S:
def get_all_vips(cursor):
    # Executando o sql:
    cursor.execute(f'select idcarros, modelo, marca, ano, preco, vip, img from carros where vip = "S" and reservado = "N" ')
    # Recuperando o retorno do BD
    lista_vips = cursor.fetchall()

    print(f'lista vip: {lista_vips}')

    # Retornar o idlogin
    return lista_vips


# função que pega informações basicas dos carros vips:
def get_base_vip(cursor):
    # Executando o sql:
    cursor.execute(f'select idcarros, modelo, preco, img from carros where vip = "S" and reservado = "N"')

    # Recuperando o retorno do BD
    base_vips = cursor.fetchall()

    # Retorna a lista com informações basicas
    return base_vips


def get_base_nor(cursor):
    # Executando o sql:
    cursor.execute(f'select idcarros, modelo, preco, img from carros where vip = "N" and reservado = "N"')

    # Recuperando o retorno do BD
    base_nor = cursor.fetchall()

    # Retorna a lista com informações basicas
    return base_nor


# função que retona todas as informações de um carro a pertir do id:
def info_car(cursor, id):
    cursor.execute(f'select * from carros where idcarros = { id }')

    # Recuperando o retorno do BD
    carro = cursor.fetchone()

    print(carro)

    return carro


# função que altera informações do carro:
def alter_carro(conn, cursor, modelo, marca, ano, preco, img_name, id):
    cursor.execute(f'UPDATE `concessionaria`.`carros` SET `modelo`="{modelo}", `marca`="{marca}", `ano`={ano}, `preco`={preco}, `img`="{img_name}" WHERE `idcarros`={ id };')

    # efetivar alteração
    conn.commit()


# função que insere o comprador no banco de dados:
def insert_compra(conn, cursor, nome, cpf, idcarro):
    cursor.execute(f'INSERT INTO concessionaria. comprador (nome, cpf, idcarro) VALUES ( "{nome}", "{cpf}", {idcarro}  );')

    conn.commit()


# função que torna o carro reservado:
def reservar_carro(conn, cursor, idcarro):
    cursor.execute(f'UPDATE concessionaria. carros SET reservado ="S" WHERE idcarros={ idcarro }')

    conn.commit()


# função que pega todas as reservas feitas no banco de dados
def base_reservas(cursor):
    cursor.execute('SELECT carros.idcarros, comprador.nome, comprador.cpf, carros.modelo, carros.marca, carros.preco From comprador, carros WHERE comprador.idcarro = carros.idcarros')

    lista_anuncios = cursor.fetchall()

    print(lista_anuncios)

    return lista_anuncios


# função que vende os carros
def del_reserva(conn, cursor, idcarro):

    # executa o comando no MySQL
    cursor.execute(f'DELETE carros.*, comprador.* FROM carros, comprador WHERE carros.idcarros = { idcarro } and comprador.idcarro = { idcarro }')

    # efetiva as mudanças
    conn.commit()


def search_car(cursor, modelo):
    cursor.execute(f'SELECT idcarros, modelo, preco , img from carros WHERE modelo LIKE "%{modelo}%" ')

    # Recuperando o retorno do BD
    lista_pesquisa = cursor.fetchall()

    print(f'A lista de pesquisa resultou: {lista_pesquisa}')

    return lista_pesquisa




