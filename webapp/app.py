from flask import Flask
from views import *

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True  # 自动刷新

app.add_url_rule("/", "index", index_page, methods=["POST", "GET"])
app.add_url_rule("/kg_big", "kg_big", kg_big, methods=["POST", "GET"])
app.add_url_rule("/kg_file", "kg_file", kg_file, methods=["POST", "GET"])
app.add_url_rule("/others", "others", others)

if __name__ == '__main__':
    app.run(threaded=False)
