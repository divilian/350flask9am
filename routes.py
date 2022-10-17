
from flask import render_template
from umm import uh
import sqlite3

@uh.route("/")
def functionname():
    conn = sqlite3.connect("bj.sqlite")
    cur = conn.cursor()
    cur.execute("select distinct flavorName from recipe order by flavorName")
    parker = cur.fetchall()
    return render_template("chooseflavor.html", flavors=parker)


