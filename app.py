from flask import Flask, render_template, request,\
 redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text # Raw SQLを安全に実行するために必要

app = Flask(__name__)

# --- SQLAlchemy Database Configuration ---
"""
 '<databaseの種類＞+<ドラバの種類＞://
\<user>:<password>@<host>/<db_name>' 
"""
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://kadai1-3:7777@localhost/TEST'
#改行には、\


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    データの新規登録と更新を行うルート。
    """
    if request.method == 'POST':

        name = request.form['name']

        record_id = request.form.get('id')

        
        if record_id:
            # UPDATE
            sql = text("UPDATE tests SET name = :name WHERE id = :id")
            db.session.execute(sql, \
{'name': name, 'id': record_id})
        else:
            # INSERT
            sql = text("INSERT INTO tests (name) VALUES (:name)")
            db.session.execute(sql, {'name': name})
        
        db.session.commit() # 変更をデータベースに保存
        return redirect(url_for('sub'))

    else: # GET
        record = None
        record_id = request.args.get('id')
        if record_id:
            # SELECT
            sql = text("SELECT * FROM tests WHERE id = :id")
            result = db.session.execute(sql, {'id': record_id}).fetchone()
            if result:
                # SQLAlchemy 2.0では結果がKeyedTupleで返るので辞書に変換
                record = dict(result._mapping)

        return render_template('index.html', record=record)


@app.route('/sub')
def sub():
    """
    データベース内の全データを表示する一覧ページ。
    """
    sql = text("SELECT * FROM tests ORDER BY created_at DESC")
    result = db.session.execute(sql).fetchall()
    # 結果を辞書のリストに変換
    records = [dict(row._mapping) for row in result]
    return render_template('sub.html', records=records)


@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    """
    指定されたIDのデータを削除する。
    """
    sql = text("DELETE FROM tests WHERE id = :id")  
    db.session.execute(sql, {'id': record_id})
    db.session.commit()
    return redirect(url_for('sub'))
if __name__ == '__main__':
   # python3 app.py で実行してください
    app.run(debug=True)
