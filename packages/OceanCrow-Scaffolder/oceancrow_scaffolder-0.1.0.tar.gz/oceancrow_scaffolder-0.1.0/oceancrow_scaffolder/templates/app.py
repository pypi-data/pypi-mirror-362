from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from {project_name}!'

if __name__ == '__main__':
    app.run(debug=True)