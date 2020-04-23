from flask import render_template, request, redirect, url_for
from feedbackinator import app, db
from feedbackinator.models import Cursos, Actividades, Feedback

@app.route("/")
def index():
	cursos = Cursos.query.all()
	return render_template("home.html", cursos=cursos)


@app.route("/cursos/<curso>")
def cursos(curso):
	actividades = Actividades.query.filter_by(curso=curso).all()
	curso_actual = curso
	return render_template("cursos.html", actividades=actividades, curso=curso_actual)


@app.route("/feedback/<actividad>")
def feedback(actividad):
	feedback = Feedback.query.filter_by(actividad=actividad).all()
	return render_template("feedback.html", actividad=actividad, feedback=feedback)


@app.route("/nuevocurso", methods=["POST"])
def nuevocurso():
	nombrecurso = request.form['nombrecurso']
	nuevo_curso = Cursos(nombre=nombrecurso)
	db.session.add(nuevo_curso)
	db.session.commit()
	cursos = Cursos.query.all()
	return render_template("home.html", cursos=cursos)


@app.route("/nuevaactividad", methods=["POST"])
def nuevaactividad():
	nombreactividad = request.form['nombreactividad']
	nombrecurso = request.form['nombrecurso']
	nueva_actividad = Actividades(nombre=nombreactividad, curso=nombrecurso)
	db.session.add(nueva_actividad)
	db.session.commit()
	curso = nombrecurso
	return redirect(url_for("cursos", curso=curso))


@app.route("/nuevofeedback", methods=["POST"])
def nuevofeedback():
	nuevofeedback = request.form['feedback']
	nombreactividad = request.form['nombreactividad']
	nuevo_feedback = Feedback(feedback=nuevofeedback, actividad=nombreactividad)
	db.session.add(nuevo_feedback)
	db.session.commit()
	actividades = Actividades.query.all()
	return redirect(url_for("feedback", actividad=nombreactividad))


@app.route("/agregarfeedback/<feedback>")
def agregarfeedback(feedback):
	return render_template("feedback.html")


@app.route("/borrarcurso/<curso>")
def borrarcurso(curso):
	curso = Cursos.query.get(curso)
	db.session.delete(curso)
	db.session.commit()
	cursos = Cursos.query.all()
	return redirect(url_for("index", cursos=cursos))


@app.route("/borraractividad/<actividad>")
def borraractiviidad(actividad):
	actividad = Actividades.query.get(actividad)
	db.session.delete(actividad)
	db.session.commit()
	actividades = Actividades.query.all()
	cursos = Cursos.query.all()
	return redirect(url_for("index", cursos=cursos))


@app.route("/borrarfeedback/<feedback>")
def borrarfeedback(feedback):
	feedback = Feedback.query.get(feedback)
	db.session.delete(feedback)
	db.session.commit()
	cursos = Cursos.query.all()
	return redirect(url_for("index", cursos=cursos))