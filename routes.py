
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
    cur.execute("select mixin_name from ingredients where recipe_name=?",
        (recipename,))
    mixins = cur.fetchall()
    conn.close()
    return render_template("recipedetails.html", recipename=recipename,
        flavor=flavor, mixins=mixins)

@uh.route("/handleorder")
def handleorder():
    # Handle non-integer input.   -- Matt
    quantity = int(request.args['quantity'])
    recipename = request.args['recipename']
    conn = sqlite3.connect("bj.sqlite")
    cur = conn.cursor()
    cur.execute("update recipe set cartonsOrdered = cartonsOrdered + ? " +
        "where name=?", (quantity, recipename))
    conn.commit()
    cur.execute("select cartonsOrdered from recipe where name=?",
        (recipename,))
    totalOrdered = cur.fetchone()[0]
    return redirect(url_for("functionname",
        msg=f"There are now {totalOrdered} cartons ordered of {recipename}!"))


@uh.route("/recipemaker", methods=['GET','POST'])
def recipemaker():
    if "name" in request.form:
        conn = sqlite3.connect("bj.sqlite")
        cur = conn.cursor()
        cur.execute("insert into recipe (name, cartonsOrdered, flavorName) " +
            "values (?, 0, ?)", (request.form['name'],
            request.form['baseFlave']))
        for key,value in request.form.items():
            if key == value:
                cur.execute("insert into ingredients (recipe_name, " +
                    "mixin_name) values (?, ?)", (request.form['name'], key))
        conn.commit()
        return "Thanks!"
        #return redirect(url_for("recipedetails", name=request.form['name']))
    else:
        conn = sqlite3.connect("bj.sqlite")
        cur = conn.cursor()
        cur.execute("select distinct flavorName from recipe")
        flavors = cur.fetchall()
        cur.execute("select distinct mixin_name from ingredients")
        mixins = cur.fetchall()
        return render_template("recipemaker.html", flavors=flavors, mixins=mixins)











