import dashscope
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from nlp import indicates_switch_tutor
from systemMessage import Tutor
from switchTextbook import switchTextbook
from dashscope import Generation
from openai import OpenAI



class Base(DeclarativeBase):
    pass

completions = []

teaching_style=''

current_textbook='3rd-grade'

dashscope.api_key = 'sk-92606777cb7748e8916082663128fe09'

model=''

client=OpenAI()






app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    init = db.Column(db.String)
    content = db.Column(JSON)

history_viewing=History()
with app.app_context():
    db.create_all()



def add_message(role, message):
    completion = {'role': role, 'content': message}
    completions.append(completion)






def genRes(message,model):
    if model=='qwen':
        response = Generation.call("qwen2-72b-instruct",
                                    messages=message,
                                    result_format='message',  # 设置输出为'message'格式

                                    )

        return response.output.choices[0]['message']['content']
    elif model=='gpt':

        response=client.chat.completions.create(model='gpt-4o',messages=message)
        return response.choices[0].message.content





@app.route('/')
def welcome():
    return render_template('index.html',teaching_style=teaching_style)

@app.route('/dialogue', methods=['POST'])
def chat():

    global history_viewing

    add_message('user', request.form.get('question'))
    abstract = datetime.now().strftime("%Y-%m-%d %H:%M")
    if model=='gpt':
        assistant_response = genRes(completions,'gpt')
    else:
        assistant_response = genRes(completions,'qwen')

    add_message('assistant', assistant_response)
    history = History(init=abstract, content=completions)
    db.session.add(history)
    db.session.commit()
    histories=History.query.order_by(desc(History.id)).all()

    history_viewing=history


    return render_template('dialogue.html', completions=[completion for completion in completions if completion['role']!='system'], histories=histories)

@app.route('/dialogue/continue', methods=['POST'])
def continued():


    global completions
    global current_textbook
    global teaching_style


    completions=history_viewing.content
    if switchTextbook(request.form.get('message')) in ['1st-grade','2nd-grade','3rd-grade','4th-grade','5th-grade','6th-grade']:

        print('textbook changed')
        current_textbook=switchTextbook(request.form.get('message'))
        if teaching_style=='humorous':
            add_message('system', Tutor(style='humorous',grade=current_textbook).load_tutor())
        elif teaching_style=='passionate':
            add_message('system', Tutor(style='passionate',grade=current_textbook).load_tutor())
        elif teaching_style=='creative':
            add_message('system', Tutor(style='creative',grade=current_textbook).load_tutor())

    if indicates_switch_tutor(request.form.get('message'))=='humorous':
        print('switched to humorous')
        add_message('system',Tutor(style='humorous',grade=current_textbook).load_tutor())
        teaching_style='humorous'
    elif indicates_switch_tutor(request.form.get('message'))=='passionate':
        print('switch to passionate')
        add_message('system',Tutor(style='passionate',grade=current_textbook).load_tutor())
        teaching_style='passionate'
    elif indicates_switch_tutor(request.form.get('message'))=='creative':
        print('switch to creative')
        add_message('system',Tutor(style='creative',grade=current_textbook).load_tutor())
        teaching_style='creative'

    add_message('user', request.form.get('message'))
    histories = History.query.order_by(desc(History.id)).all()
    if model=='gpt':
        assistant_response = genRes(completions,'gpt')
    else:
        assistant_response = genRes(completions,'qwen')

    add_message('assistant', assistant_response)

    with app.app_context():
        modified_item=History.query.get_or_404(history_viewing.id)
        modified_item.content=[message for message in completions]
        db.session.flush()
        db.session.commit()

    return render_template('dialogue.html', completions=[completion for completion in completions if completion['role']!='system'], histories=histories)

@app.route('/save_record',methods=['POST'])
def saveRecord():


    completions.clear()

    return redirect(url_for('welcome'))


@app.route('/display_history',methods=['POST'])
def displayHistory():

    global history_viewing
    history_id=request.form.get('history_id')
    history=History.query.get_or_404(history_id)
    histories = History.query.order_by(desc(History.id)).all()

    history_viewing=history
    return render_template('dialogue.html',completions=[content for content in history.content if content['role']!='system'],histories=histories)

@app.route('/style_selection',methods=['POST'])
def selectStyle():
    global teaching_style
    if 'humorous' in request.form:
        add_message('system',Tutor(style='humorous',grade=current_textbook).load_tutor())
        teaching_style="humorous"
    elif 'passionate' in request.form:
        add_message('system',Tutor(style='passionate',grade=current_textbook).load_tutor())
        teaching_style="passionate"
    else:
        add_message('system',Tutor(style='creative',grade=current_textbook).load_tutor())
        teaching_style="creative"


    return render_template('index.html',teaching_style=teaching_style,model=model)

@app.route('/model_selection',methods=['POST'])
def selectModel():
    global model
    if 'gpt' in request.form:
        model='gpt'
    elif 'qwen' in request.form:
        model='qwen'
    print(model)
    return render_template('index.html', model=model,teaching_style=teaching_style)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
