from flask import render_template, request, redirect, url_for, request
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


@app.route("/feedback/<actividad>", methods=["GET", "POST"])
def feedback(actividad):
	feedback = Feedback.query.filter_by(actividad=actividad).all()
	if request.method=="GET":
		actividad = actividad
		mensaje = "Elige feedback"
		return render_template("feedback.html", actividad=actividad, feedback=feedback, mensaje=mensaje)
	elif request.method=="POST":
		snippets = request.form.getlist('formafeedback')
		t_snippets = tuple(snippets)
		compiled_feedback = " "
		espacio = " "
		for t in t_snippets:
			specific_feedback = Feedback.query.filter_by(id=t).first()
			string_feedback = str(specific_feedback)
			compiled_feedback = compiled_feedback + string_feedback + compiled_feedback
		print(compiled_feedback)
		return render_template("feedback.html", actividad=actividad, feedback=feedback, mensaje=compiled_feedback)



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
	feedback = Feedback.query.filter_by(actividad=actividad).all()
	db.session.delete(feedback)
	db.session.delete(actividad)
	db.session.commit()
	actividades = Actividades.query.all()
	cursos = Cursos.query.all()
	return redirect(url_for("index", cursos=cursos))


@app.route("/managefeedback/<actividad>")
def managefeedback(actividad):
	feedback = Feedback.query.filter_by(actividad=actividad).all()
	return render_template("managefeedback.html", feedback=feedback, actividad=actividad)


@app.route("/borrarfeedback/<feedback>", methods=["POST"])
def borrarfeedback(feedback):
	feed = Feedback.query.get(feedback)
	actividad = request.form.get("actividad")
	db.session.delete(feed)
	db.session.commit()
	cursos = Cursos.query.all()
	return redirect(url_for("managefeedback", actividad=actividad))
	#return redirect(url_for("index", cursos=cursos))