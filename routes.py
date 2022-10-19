
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
        msg = request.args['msg'] if "msg" in request.args else ""
        return render_template("chooseflavor.html", flavors=parker, msg=msg)


@uh.route("/browserecipes")
def browserecipes():
    conn = sqlite3.connect("bj.sqlite")
    cur = conn.cursor()
    cur.execute("select name, cartonsOrdered from recipe where flavorName=?",
        (request.args['flavor'],))
    recipes = cur.fetchall()
    conn.close()
    if len(recipes) == 0:
       return redirect(url_for("functionname", msg=f"Please choose a valid flavor, not {request.args['flavor']}"))
    return render_template("browserecipes.html", flavor=request.args['flavor'],
        recipes=recipes)

@uh.route("/recipedetails")
def recipedetails():
    recipename= request.args['name']
    conn = sqlite3.connect("bj.sqlite")
    cur = conn.cursor()
    cur.execute("select flavorName from recipe where name=?", (recipename,))
    flavor = cur.fetchone()[0]
    conn.close()
    return render_template("recipedetails.html", recipename=recipename,
        flavor=flavor)













