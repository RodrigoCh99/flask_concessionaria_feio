# Importando as bibliotecas:
from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL
from db import *
import os
from werkzeug.utils import secure_filename

# Instanciando o objeto Flask
app = Flask(__name__)

# definido o endereço em que as imagens serão salvas
UPLOAD_FOLDER = 'C://Users//Adm//PycharmProjects//projeto_site_concessionaria//static//images'

# configurando a pasta de upload a qual as imagens enviadas  pelo usuario serão armazenadas
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Instanciando o objeto MySQL
mysql = MySQL()

# Conectando MySQL ao Flask
mysql.init_app(app)

# Configuração do Banco de dados:
config(app)


# Rota para o index:
@app.route('/')
def index():
    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    return render_template('index.html', lista_carros_vip=get_base_vip(cursor), lista_carros_nor=get_base_nor(cursor))


# rota para a pagina de administração do superior
@app.route('/adm', methods=['GET','POST'])
def adm():
    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    # renderizando a pagina do administrador:
    return render_template('adm.html', lista_fun=get_fun(cursor), lista_car=get_carros(cursor), lista_vip=get_all_vips(cursor), lista_reservas=base_reservas(cursor))


# rota para a pagina do funcionario, com as reservas
@app.route('/funcionario')
def funcionario():

    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    # renderizando a pagina do funcionario:
    return render_template('funcionario.html', lista_reservas=base_reservas(cursor))


# rota para a pagina de login
@app.route('/login')
def login():
    return render_template('login.html')


# rota para entrar, seja como funcionario seja como administrador
@app.route('/entrar', methods=['GET','POST'])
def entrar():
    if request.method == 'POST':

        login = request.form.get('login')
        senha = request.form.get('senha')

        # Obtendo o cursor para acessar o BD
        conn, cursor = get_db(mysql)

        # VARIAVEL CONTENDO A RESPOSTA SE O LOGIN ESTÁ NA TABELA FUNCIONARIO:
        fun = get_idfun(cursor, login, senha)

        # VARIAVEL CONTENDO A RESPOSTA SE O LOGIN ESTÁ NA TABELA ADM:
        adm = get_idadm(cursor, login, senha)

        if fun is None:
            if adm is None:
                # Fechar o cursor
                cursor.close()
                # Fechar a conexao
                conn.close()
                return render_template('login.html', erro='Login/Senha não cadastrado!')

            else:

                return redirect(url_for('adm'))

        else:
            # Fechar o cursor
            cursor.close()
            # Fechar a conexao
            conn.close()
            return redirect(url_for('funcionario'))

    else:
        return render_template('index.html', erro='Método incorreto. Use POST!')


# rota para o formulario de adição de funcionario
@app.route('/form_func')
def form_func():
    return render_template('form_func.html')


# rota que adiciona o funcionario criado e retorna para a pagina do administrador
@app.route('/add_func', methods=['GET','POST'])
def add_func():

    novo_login = request.form.get('novo_login')
    nova_senha = request.form.get('nova_senha')

    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    # função que insere funcionario:
    add_new_func(conn, cursor, novo_login, nova_senha)

    return redirect(url_for('adm'))


# rota para remover um funcionario do banco de dados
@app.route('/deletar_func/<id>')
def deletar_func(id):

    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    # função para deletar funcionarios do banco de dados:
    del_func(conn, cursor, id)

    return redirect(url_for('adm'))


# rota para remover anuncio do banco de dados
@app.route('/deletar_anun/<id>/<img_name>')
def deletar_anun(id, img_name):
    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    # função para deletar funcionarios do banco de dados:
    del_anun(conn, cursor, id)

    # função para deletar a img da pasta static, como os dados não são relacionados ao banco de dados esta operação será realizada aqui mesmo
    os.remove(f'C://Users//Adm//PycharmProjects//projeto_site_concessionaria//static//images//{img_name}')
    return redirect(url_for('adm'))


# rota para o formulario de alteração de dados dos funcionarios
@app.route('/form_alter_func/<id>')
def form_alter_func(id):

    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    infos = info_func(cursor, id)

    return render_template('form_alter_func.html', informacoes=infos)


# rota para salvar as alterações nos dados do formulario
@app.route('/save_alter_func', methods=['POST'])
def save_alter_func():
    if request.method == 'POST':

        # Obtendo o cursor para acessar o BD
        conn, cursor = get_db(mysql)

        updated_login = request.form.get('updated_login')
        updated_senha = request.form.get('updated_senha')
        idfuncionario = request.form.get('idfuncionario')

        # função de alteração de senha:
        alter_func(conn, cursor, updated_login, updated_senha, idfuncionario)

        # redirecionamento para a função adm da rota adm
        return redirect(url_for('adm'))

    else:
        # redirecionamento para a função adm da rota adm
        return redirect(url_for('adm'))


# rota para adicionar um carro a lista de carros vips
@app.route('/add_vip/<id>/<estado>')
def add_vip(id, estado):
    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    saida = vip(conn, cursor, id, estado)
    if saida == None:
        return redirect(url_for('adm'))

    else:
        return render_template('erro.html', erro=saida)


# rota para o formulario de adição de carros
@app.route('/form_car')
def form_car():
    return render_template('form_car.html')


# rota para adicionar o carro novo ao banco de dados e sua foto a pasta static
@app.route('/add_car', methods=['GET', 'POST'])
def add_car():

    # Verificação do metodo:
    if request.method == 'POST':

        # Obtendo o cursor para acessar o BD
        conn, cursor = get_db(mysql)

        # conn, cursor, modelo, marca, ano, preco, vip, img
        modelo = request.form.get('modelo')
        marca = request.form.get('marca')
        ano = request.form.get('ano')
        preco = request.form.get('preco')

        print(f'modelo: {modelo}, marca: {marca}, ano:{ano}, preco:{preco}')
        # verifica se tem a parte file no request
        if 'img' not in request.files:
            # print('o arquivo não foi encontrado')
            return render_template('index.html')

        # pega o arquivo
        arquivo = request.files['img']

        # se o usuario nao selecionar o arquivo
        # o browser manda um arquivo sem nome
        if arquivo.filename == '':
            # print('Arquivo sem nome')
            return render_template('index.html')

        else:
            # armazenando o nome do arquivo em uma variavel:
            img_name = secure_filename(arquivo.filename)
            arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename))
            # print(f'O nome do arquivo é: {img_name}')

            # print(f'modelo: {modelo}, marca: {marca}, ano:{ano}, preco:{preco}, vip: {vip}, nome da img: {img_name}')
            add_new_car(conn, cursor, modelo, marca, ano, preco, img_name)

            return redirect(url_for('adm'))



@app.route('/form_alter_car/<id>')
def alter_car(id):

    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    lista_infos = info_car(cursor, id)

    return render_template('form_alter_car.html', informacoes=lista_infos)


@app.route('/save_alter_car', methods=['POST'])
def save_alter():
    if request.method == 'POST':

        # Obtendo o cursor para acessar o BD
        conn, cursor = get_db(mysql)

        # requisita informações enviadas pelo formulario:
        modelo = request.form.get('novo_modelo')
        marca = request.form.get('nova_marca')
        ano = request.form.get('novo_ano')
        preco = request.form.get('novo_preco')
        id = request.form.get('idcarro')
        nome_antigo = request.form.get('nome_antigo')


        # tratando informações:
        if 'img' not in request.files:
            print(f'IMG não encontrada')

        # pega o arquivo
        arquivo = request.files['img']



        # se o usuario nao selecionar o arquivo
        # o browser manda um arquivo sem nome
        if arquivo.filename == '':

            # altera apenas as informações que não são ligadas a img
            alter_carro(conn, cursor, modelo, marca, ano, preco, nome_antigo, id)

            # redireciona para a rota adm
            return redirect(url_for('adm'))

        else:
            novo_nome = secure_filename(arquivo.filename)

            # salvando o novo arquivo na pasta das imagens
            arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename))

            # alterando as informações
            alter_carro(conn, cursor, modelo, marca, ano, preco, novo_nome, id)

            # apagando a img anterior:
            os.remove(f'C://Users//Adm//PycharmProjects//projeto_site_concessionaria//static//images//{ nome_antigo }')

            # redireciona para a rota adm
            return redirect(url_for('adm'))

@app.route('/detalhes/<id>')
def detalhar_anuncio(id):

    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    detalhe = info_car(cursor, id)
    print(f'O detalhes do carro são: {detalhe}')

    return render_template('detalhe.html', detalhes=detalhe)


@app.route('/form_comprador/<id>')
def comprador(id):

    # redireciona para o formulario de reservado carro em que o comprador se cadastra
    return render_template('form_comprador.html', id_do_carro=id)


@app.route('/save_reserva', methods=['POST'])
def salvar_reserva():

    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    # requisita informações enviadas pelo formulario:
    nome = request.form.get('nome_comprador')
    cpf = request.form.get('cpf_comprador')
    idcarro = request.form.get('id_carro')


    carro = info_car(cursor, idcarro)


    # verificação para se ocorrer de uma carro vip ser comprado ele pare de ser vip!
    if carro[6] == 'S':

        # função que inverte o estado do carro:
        vip(conn, cursor, idcarro, carro[6])

        # função que insere o comprador no banco de dados:
        insert_compra(conn, cursor, nome, cpf, idcarro)

        # função que altera o estado do carro o deixando como reservado
        reservar_carro(conn, cursor, idcarro)

        # função que redireciona parao o index
        return redirect('/')

    else:
        # função que insere o comprador no banco de dados:
        insert_compra(conn, cursor, nome, cpf, idcarro)

        # função que altera o estado do carro o deixando como reservado
        reservar_carro(conn, cursor, idcarro)

        # função que redireciona parao o index
        return redirect('/')

@app.route('/vender_reserva/<id_carro>')
def venda_do_carro(id_carro):

    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    # função que retorna informações sobre o carro que se possui o id
    informacao = info_car(cursor, id_carro)

    # função que utiliza a lib os para remover imagens do static de acordo com o nome retornnado
    os.remove(f'C://Users//Adm//PycharmProjects//projeto_site_concessionaria//static//images//{informacao[7]}')

    # função que remove tanto o comprador quanto o carro do banco de dados:
    del_reserva(conn, cursor, id_carro)

    return redirect('/funcionario')


@app.route('/pesquisar', methods=['GET','POST'])
def pesquisar():

    pesquisa = request.form.get('pesquisa')

    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    lista_de_carros = search_car(cursor, pesquisa)

    return render_template('index.html', lista_carros_vip=lista_de_carros)






# Rodando a app
if __name__ == '__main__':
    app.run(debug=True)


