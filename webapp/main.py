from flask import Flask, render_template, Markup
from birdnet_scanner import db_query
import datetime


app = Flask(__name__)


@app.route("/birdids")
def top_ids():
    log = '/home/neil/app.log'
    with open(log, 'w') as fh:
        df_top_ids = db_query.top_ids()
        html_top = Markup(df_top_ids.to_html())

        df_last_24 = db_query.top_ids_last_24h()
        if len(df_last_24) == 0:
            html_24 = 'No birds seen in the last 24h'
        else:
            html_24 = Markup(df_last_24.to_html())
        fh.write(str(datetime.datetime.now()))

        return render_template('summary_tables.html', table_all_time=html_top, table_last_24h=html_24)


@app.after_request
def apply_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


if __name__ == "__main__":
    app.run(host='127.0.0.1')

