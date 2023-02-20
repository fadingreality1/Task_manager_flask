from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone, timedelta


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://newuser:password@127.0.0.1/Adventure'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Adventure(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    time = db.Column(db.String(200), default = datetime.utcnow)


@app.route('/',  methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        adventure = Adventure(title = title, desc = desc) 
        db.session.add(adventure)
        db.session.commit()
        
    alladventures = Adventure.query.all()
    return render_template('index.html',alladventures = alladventures)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        task = Adventure.query.filter_by(sno = sno).first()
        task.title = title
        task.desc = desc 
        db.session.add(task)
        db.session.commit()
        return redirect('/')
    updated = Adventure.query.filter_by(sno = sno).first()
    return render_template('update.html', task = updated)
    
    
@app.route('/delete/<int:sno>')
def delete(sno):
    Adventure.query.filter_by(sno=sno).delete()
    db.session.commit()
    return redirect('/')
    

if __name__ == "__main__":
    # ? app.app_context() is necessarry as without it, table won't be created
    with app.app_context():
        db.create_all()
        app.run(debug=True)