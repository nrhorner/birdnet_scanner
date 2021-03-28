from flask import Flask, render_template, Markup
from birdnet_scanner import db_query


app = Flask(__name__)

@app.route("/")
def top_ids():

    df_top_ids = db_query.top_ids()
    html_top = Markup(df_top_ids.to_html())

    df_last_24 = db_query.top_ids_last_24h()
    if len(df_last_24) == 0:
        html_24 = 'No birds seen in the last 24h'
    else:
        html_24 = Markup(df_last_24)

    return render_template('summary_tables.html', table_all_time=html_top, table_last_24h=html_24)


if __name__ == "__main__":
    app.run(host='127.0.0.1')

