from app import app, seed_database
from app.models import db

from flask import render_template, render_template_string, redirect, make_response, request, url_for
from flask_jwt_extended import get_jwt_identity, create_access_token, verify_jwt_in_request
from functools import wraps
from hashlib import md5

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        with db() as (_, cur):
            query_c = cur.execute('SELECT * FROM category LIMIT 6;').fetchall()
            query_n = cur.execute('SELECT * FROM news;').fetchall()

        categories = [dict(row) for row in query_c]
        news_ = [dict(row) for row in query_n]

        return render_template(
            'index.html',
            categories=categories,
            news=news_
            )

    email = request.form.get('email')

    if email:
        with db() as (conn, cur):
            exists = cur.execute('SELECT * FROM subscribers WHERE email=?;', (email,)).fetchone()

            if not exists:
                cur.execute('INSERT INTO subscribers(email) VALUES(?)', (email,))

                conn.commit()

    return redirect(url_for('home'))
    

@app.route('/pesquisa')
def search():
    q: str = request.args.get('q', '')

    news_: list[dict] = []
    with db() as (_, cur):
        if q:
            query_n = cur.execute('SELECT * FROM news WHERE title LIKE ?;', (f'%{q}%',)).fetchall()

            news_ = [dict(row) for row in query_n]
        query_c = cur.execute('SELECT * FROM category LIMIT 6;').fetchall()

        categories = [dict(row) for row in query_c]


    return render_template(
        'busca.html', 
        categories=categories,
        news=news_,
        query=q
        )


@app.route('/categoria')
def category():
    c_id: int = request.args.get('id')

    if not c_id:
        return redirect(url_for('home'))

    with db() as (_, cur):
        query_c = cur.execute('SELECT * FROM category LIMIT 6;').fetchall()

        categories: list[dict[str, str]] = [dict(row) for row in query_c]

        category: dict[str, str] = cur.execute('SELECT * FROM category WHERE id=?;', (c_id,)).fetchone()

        query_n = cur.execute('SELECT * FROM news WHERE category=?;', (c_id,)).fetchall()
        news_: list[dict[str, str]] = [dict(row) for row in query_n]


    return render_template(
        'categoria.html', 
        categories=categories,
        category=category,
        news=news_
        )


@app.route('/newcat', methods=['POST'])
def newcat():
    title = request.form.get('title')
    if not title:
        return redirect(url_for('admin'))

    with db() as (conn, cur):
        exists = cur.execute('SELECT * FROM category WHERE title=?', (title,)).fetchone()
        if not exists:
            cur.execute('INSERT INTO category(title) VALUES(?);', (title,))
            conn.commit()

    return redirect(url_for('admin'))

@app.route('/delcat', methods=['GET'])
def delcat():
    id = request.args.get('id')
    if not id:
        return redirect(url_for('admin'))

    with db() as (conn, cur):
        cur.execute('DELETE FROM category WHERE id=?', (id,))

        conn.commit()

    return redirect(url_for('admin'))


@app.route('/noticia', methods=['GET', 'POST'])
def news():
    if request.method == 'GET':
        new_id: int = request.args.get('id')
        if not new_id:
            return redirect(url_for('home'))

        with db() as (_, cur):
            query_c = cur.execute('SELECT * FROM category LIMIT 6;').fetchall()

            categories: list[dict[str, str]] = [dict(row) for row in query_c]

            new = cur.execute(f'SELECT * FROM news WHERE id={new_id};').fetchone()

            if not new:
                return 'Notícia não encontrada', 404

        return render_template(
            'noticia.html',
            title=new['title'],
            author=new['author'],
            categories=categories
        )
    
    new_data: dict[str, str] = request.form.to_dict()

    with db() as (conn, cur):
        cur.execute('INSERT INTO news (title, body, author, category) VALUES(?, ?, ?, ?);', (new_data['title'], new_data['body'], new_data['author'], new_data['category']))

        conn.commit()

    return redirect(url_for('admin'))


@app.route('/editnew', methods=['GET', 'POST'])
def edit_new():
    edit: dict[str, str] = request.form.to_dict()
    
    try:

        with db() as (conn, cur):
            cur.execute('UPDATE news SET title=?, body=?, author=? WHERE id=?', (edit['title'], edit['body'], edit['author'], edit['id']))

            conn.commit()

    except KeyError:
        return redirect(url_for('admin'))

    return redirect(url_for('admin'))


@app.route('/delnew')
def delnew():
    new_id = request.args.get('id')
    if not new_id:
        return redirect(url_for('admin'))

    with db() as (conn, cur):
        cur.execute('DELETE FROM news WHERE id=?;', (new_id,))

        conn.commit()

    return redirect(url_for('admin'))


@app.route('/sobre')
def about():
    with db() as (_, cur):
        query_c = cur.execute('SELECT * FROM category LIMIT 6;').fetchall()

    categories = [dict(row) for row in query_c]

    return render_template('sobre.html', categories=categories)

# ROTAS COM LOGIN REQUIRED

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except:
            return redirect(url_for('login'))

        user_id = get_jwt_identity()
        if not user_id:
            return redirect(url_for('home'))

        return f(*args, **kwargs)
    return wrapper


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    form = request.form.to_dict()

    with db() as (_, cur):
        user = cur.execute('SELECT * FROM users WHERE email=?;', (form['email'],)).fetchone()


    if user:
        if user['password'] == md5(form['password'].encode('utf-8')).hexdigest():
            response = make_response(redirect(url_for('admin')))
            response.set_cookie('token', create_access_token(identity=str(user['id'])))

            return response

    return render_template('login.html', erro=True)


@app.route('/admin')
@login_required
def admin():
    with db() as (_, cur):
        query_s = cur.execute('SELECT * FROM subscribers;').fetchall()
        query_c = cur.execute('SELECT * FROM category;').fetchall()
        query_n = cur.execute('SELECT n.*, c.title AS c_title FROM news n JOIN category c ON n.category=c.id;').fetchall()

    subscribers = [dict(row) for row in query_s]
    categories = [dict(row) for row in query_c]
    news_ = [dict(row) for row in query_n]

    template = open('app/templates/admin.html', 'r', encoding='utf-8').read()

    item: str = ''

    for new in news_:
        item += f'''
        <div class="data-item">
            <div>
                <strong> $TITLE$ </strong>
                <div class="data-meta">Categoria: <span style="color: var(--brand-highlight, #FF4D4D)">{ new['c_title'] }</span> | Autor: {new['author']}</div>
            </div>
            <div class="btn-group">
                <!-- Botão Visualizar passando os dados da notícia via atributos data-* -->
                <button class="btn btn-secondary btn-sm" 
                        data-id="{ new['id'] }" 
                        data-title="{ new['title'] }" 
                        data-cat="{ new['c_title'] }" 
                        data-author="{ new['author'] }" 
                        data-body="{ new['body'] }" 
                        onclick="openNewsModal(this)">Visualizar</button>
                <a href="{ url_for('delnew', id=new['id']) }" class="btn btn-danger" onclick="this.closest('.data-item').remove()">Apagar</a>
            </div>
        </div>
        '''.replace('$TITLE$', new['title'])

    template = template.replace('$ITEMS$', item)

    try:
        return render_template_string(
            template,
            subscribers=subscribers,
            categories=categories,
            news=news_
            )
    except:
        return redirect(url_for('reset_news'))


@app.route('/ctfemergency/resetnews') # Resetamos as news se o ssti ocasionar erro permanente no painel de admin
def reset_news():
    with db() as (conn, cur):
        cur.execute('DELETE FROM news');
        conn.commit()

    seed_database()

    return redirect(url_for('admin'))


@app.route('/logout')
@login_required
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('token', '')

    return response
