from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

tasks = []

@app.route('/')
def setup():
    return render_template('setup.html')

@app.route("/board", methods=["POST"])
def index():
    board = request.form['board']
    board_title = board.capitalize()

    return render_template('index.html', tasks=tasks, board_title=board_title)

@app.route("/add_task", methods=["POST"])
def add_task():
    task = request.form['task']
    deadline = request.form['deadline']
    priority = request.form['priority']
    task_dados = {
        'task': task,
        'deadline': deadline,
        'priority': priority,
        'done': False
    }
    #Delimita o prazo de acordo com a prioridade
    deadlines = {
        'High': 0,
        'Medium': 5,
        'Low': 15
    }
    #Encontra o tempo restante para fazer a tarefa
    today = datetime.date.today()
    format_deadline = datetime.datetime.strptime(deadline, '%Y-%m-%d').date()
    time_left = (format_deadline - today).days
    #Verifica se o prazo é compatível com a prioridade
    message = ''
    if time_left >= deadlines[priority]:
        tasks.append(task_dados)
    else:
        message = 'Aumente a prioridade ou extenda o prazo.'

    return render_template('index.html', tasks=tasks, message=message)

@app.route('/check_task', methods=['POST'])
def check_task():
    checked_task = int(request.form.get('check'))
    for i, task in enumerate(tasks):
        state = tasks[i]['done']
        if tasks.index(task) == checked_task:         
            if state == False:
                tasks[i]['done'] = True
                print('Task is done')
            else:
                tasks[i]['done'] = False
                print('Task is pending')

    return redirect('/')

@app.route('/remove_task', methods=['POST'])
def remove_task():
    #Pega o valor do index pelo botão
    removed_task = int(request.form.get('remove'))
    for i, task in enumerate(tasks):
        if tasks.index(task) == removed_task:            
            del tasks[i]
            print('Task removed')
            break    

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
