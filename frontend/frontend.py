from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__, template_folder='templates', static_folder='staticFiles')
api_url = "http://localhost:8000/tasks"
app.secret_key = "secret"

@app.route('/')
def index():
    response = requests.get(api_url)
    tasks = response.json()
    return render_template('index.html', tasks=tasks)


@app.route('/task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    task = {"title": title, "description": description}
    response = requests.post(api_url, json=task)
    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        flash(response.json().get("detail", 'Error: Unable to add task. Please try again later.'), 'error')
        return redirect(url_for('index'))


@app.route('/task/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = requests.get(f"{api_url}/{id}").json()
    if request.method == 'POST':
        task["title"] = request.form['title']
        task["description"] = request.form['description']
        response = requests.put(f"{api_url}/{id}", json=task)
        if response.status_code == 200:
            return redirect(url_for('index'))
        else:
            flash(response.json().get("detail", 'Error: Unable to update task. Please try again later.'), 'error')
            return render_template('edit.html', task=task)
    return render_template('edit.html', task=task)


@app.route('/task/delete/<int:id>')
def delete_task(id):
    requests.delete(f"{api_url}/{id}")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
