from flask import Flask, render_template, request, redirect, flash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'não_era_para_estar_aqui'

livros = []
livros= [
    {     'codigo': 0,
          'titulo': 'um titulo ',
          'autor' : 'autor',
          'ano': 1908,
          'emprestado': False,
          'devolver': '--/--/----'
     }
]
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html', livros=livros)

@app.route('/adicionar_livro', methods=['GET', 'POST'])
def adicionar_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        codigo = len(livros)
        devolver = "--/--/----"
        emprestado = False
        livro = {
            'codigo ': codigo,
            'titulo': titulo,
            'autor': autor,
            'ano' : ano,
            'emprestado': emprestado,
            'devolver': devolver
        }
        livros.append(livro)
        flash(f'Livro {titulo} adicionado com sucesso!')
        return redirect('/catalogo')
    else:
        return render_template('/adicionar_livro.html')

@app.route('/editar_livro/<int:codigo>', methods=['GET', 'POST'])
def editar_livro(codigo):
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        livros[codigo] = [codigo, titulo, autor, ano]
        flash(f'Livro {titulo} atualizado com sucesso!')
        return redirect('/catalogo')
    else:
        livro = livros[codigo]
        return render_template('editar_livro.html', livro=livro)

@app.route('/emprestar/<int:codigo>')
def emprestar(codigo):
    for livro in livros:
        if livro['codigo'] == codigo:
            livro['emprestado'] = True
            devolver = (datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y')
            livro['devolver'] = devolver
            return redirect('/catalogo')
        else:
            return redirect('/catalogo')

@app.route('/devolver/<int:codigo>')
def devolver(codigo):
    for livro in livros:
        if livro['codigo'] == codigo:
            devolucao = datetime.strptime(livro['devolver'], "%Y-%m-%d")
            dias = (datetime.now() - devolucao).days
            print(dias)


@app.route('/apagar_livro/<int:codigo>')
def apagar_livro(codigo):
    del livros[codigo]
    flash(f'Livro excluído com sucesso !')
    return redirect('/catalogo')

if __name__ == '__main__':
    app.run(debug=True)