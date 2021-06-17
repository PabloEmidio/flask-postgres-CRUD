from datetime import datetime

from flask import Flask, request, render_template, redirect

from project.db.access_database import AccessDataBase

def init_app(app: Flask):
    
    @app.route('/')
    def index():
        return redirect('messages/')

    @app.route('/messages/', methods=['GET'])
    def get_messages():
        dbobj = AccessDataBase()
        messages = dbobj.get_data()
        return render_template('index.html', messages=messages)
    
    @app.route('/message/create/', methods=['GET', 'POST'])
    def insert_message():
        if request.method == 'POST':
            message_json = {}
            message_json['message_title'] = request.form['title']
            message_json['author_name'] = request.form['author']
            message_json['message_text'] = request.form['message']
            message_json['creation_date'] = str(datetime.now().date())
            dbobj = AccessDataBase()
            dbobj.write_data(message_json)
            create_now = dbobj.get_data()[-1][0]
            return redirect(f'/message/{create_now}')
        else:
            return render_template('create.html')
        
    @app.route('/message/update/<int:message_id>/', methods=['GET', 'POST'])
    def update_message(message_id):
        dbobj = AccessDataBase()
        message = dbobj.get_data(message_id)
        if request.method == 'POST':
            message_json = {}
            message_json['message_title'] = request.form['title']
            message_json['author_name'] = request.form['author']
            message_json['message_text'] = request.form['message']
            if not message_json['message_title'] and \
                not message_json['author_name'] and \
                not message_json['message_text']:
                return render_template('update.html', messages=message, blank=True)
            if message_json['message_title']:
                args = ['message_title', message_json['message_title']]
                dbobj.update(message_id, args)
            if message_json['author_name']:
                args = ['author_name', message_json['author_name']]
                dbobj.update(message_id, args)
            if message_json['message_text']:
                args = ['message_text', message_json['message_text']]
                dbobj.update(message_id, args)
            return redirect(f'/message/{message_id}/')
        else:
            return render_template('update.html', messages=message) if message else 'Not Found', 404
            # return render_template('index.html')
    
    @app.route('/message/<int:message_id>/', methods=['GET', 'POST'])
    def access_or_delete_message(message_id):
        dbobj = AccessDataBase()
        if request.method == 'POST':
            dbobj.remove_data(message_id)
            return redirect('/messages/')
        else:
            message = dbobj.get_data(message_id)
            return render_template('index.html', messages=message) if message else 'Not Found', 404
