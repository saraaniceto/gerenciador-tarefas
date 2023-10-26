from flask import Flask, render_template, request, url_for
import datetime

app = Flask(__name__)

tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route("/add_task", methods=["POST"])
def add_task():
    task = request.form['task']
    deadline = request.form['deadline']
    priority = request.form['priority']
    task_dados = {
        'task': task,
        'deadline': deadline,
        'priority': priority,
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

@app.route('/remove_task', methods=['POST'])
def remove_task():
    #Pega o valor do index pelo botão
    removed_task = int(request.form.get('remove_task'))
    #
    for i, task in enumerate(tasks):
        if tasks.index(task) == removed_task:            
            del tasks[i]
            print(tasks)
            break    

    return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
