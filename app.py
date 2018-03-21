from flask import Flask
import flask
import time
import subprocess
app = Flask(__name__)

@app.route("/")
def main():
    return '''<h1>Load testing control center</h1>
        <form action="/activate" method="post">
            <input type="submit" value="Activate">
            '''

@app.route("/activate", methods=["POST"])
def index():
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
