from commands.create_db import create_tables, drop_table, drop_all_tables
from flask import Flask, Response, render_template
import core.db as db

app = Flask(__name__)
app.cli.add_command(create_tables)
app.cli.add_command(drop_table)
app.cli.add_command(drop_all_tables)


@app.route('/')
def index():
    return render_template('PoCs/index_poc.html')

# @app.route('/')
# def index():
#     return render_template('index.html')


# def __main__():
#     app.run(host='0.0.0.0', debug=True)
