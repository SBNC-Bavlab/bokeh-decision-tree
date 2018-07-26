from flask import Flask, render_template, request

from bokeh.embed import server_document
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from threading import Thread

from Decision_Tree.Plot.decision_tree import create_figure
app = Flask(__name__)


def modify_doc(doc):
    # Create the plot
    plot = create_figure()
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
    server = Server({'/bkapp': modify_doc}, io_loop=IOLoop(), allow_websocket_origin=["localhost:5000"])
    server.start()
    server.io_loop.start()


Thread(target=bk_worker).start()

if __name__ == '__main__':
    app.run()
