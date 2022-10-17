
from flask import render_template, request, redirect, url_for
from umm import uh
import sqlite3

@uh.route("/")
def functionname():
    if "faveflave" in request.args:
        return redirect(url_for("browserecipes",
            flavor=request.args['faveflave']))
    else:
        conn = sqlite3.connect("bj.sqlite")
        cur = conn.cursor()
        cur.execute("select distinct flavorName from recipe order by flavorName")
        parker = cur.fetchall()
        conn.close()
        return render_template("chooseflavor.html", flavors=parker)


@uh.route("/browserecipes")
def browserecipes():
    conn = sqlite3.connect("bj.sqlite")
    cur = conn.cursor()
    cur.execute("select name, cartonsOrdered from recipe where flavorName=?",
        (request.args['flavor'],))
    recipes = cur.fetchall()
    conn.close()
    if len(recipes) == 0:
       return f"<HTML><BODY><H1>GROSS!! We hate {request.args['flavor']} here at B and J's</H1></BODY></HTML>"
    return render_template("browserecipes.html", flavor=request.args['flavor'],
        recipes=recipes)














