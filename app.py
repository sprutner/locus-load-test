from flask import Flask, request
import flask
import time
import subprocess
import boto3
app = Flask(__name__)

@app.route("/")
def main():
    return '''<h1>Load testing control center</h1>
        <form action="/activate" method="post">
            Target URL: <input type="text" name="url"><br>
            Number of users: <input type="text" name="users"<br>
            Hatch rate (users spawned per second): <input type="text" name="hatchrate"<br>
            Run Time (e.g. 1h30m): <input type="text" name="runtime"<br>
            <input type="submit" value="Activate">
            '''

@app.route("/activate", methods=["POST"])
def index():
    url = request.form.get('url')
    users = request.form.get('users')
    hatchrate = request.form.get('hatchrate')
    runtime = request.form.get('runtime')

    from sqs import sendMessage
    sendMessage('{"url": "%s", "users": "%s", "hatchrate": "%s", "runtime": "%s"}' % (url, users, hatchrate, runtime))

    def inner():
        proc = subprocess.Popen(
            ['python autoscale.py'],             #call something with a lot of output so we can see it
            shell=True,
            universal_newlines=True,
            stdout=subprocess.PIPE
        )

        for line in iter(proc.stdout.readline,''):
            time.sleep(1)                           # Don't need this just shows the text streaming
            yield line.rstrip() + '<br/>\n'

    return flask.Response(inner(), mimetype='text/html')  # text/html is required for most browsers to show th$
    # import autoscale

if __name__ == "__main__":
    app.run()
