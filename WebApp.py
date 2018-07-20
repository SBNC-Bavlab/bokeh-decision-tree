from flask import Flask, render_template, request

from bokeh.embed import server_document
from bokeh.server.server import Server
from tornado.ioloop import IOLoop

from Decision_Tree.Plot.decision_tree import create_figure
app = Flask(__name__)


def modify_doc(doc):
    # Create the plot
    plot = create_figure()
    print("here234")
    # Embed plot into HTML via Flask Render
    doc.add_root(plot)

@app.route('/q', methods=['GET'])
def shut():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("index.html", script=script, template="Flask")


def bk_worker():
    server = Server({'/bkapp': modify_doc}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])
    server.start()
    server.io_loop.start()


from threading import Thread
Thread(target=bk_worker).start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(port=8000)
