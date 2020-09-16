from feedbackinator import db

class Cursos(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(50), nullable=False)
	actividades = db.relationship("Actividades", backref="cursos", lazy=True)

	def __repr__(self):
		return self.nombre


class Actividades(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(50), nullable=False)
	curso = db.Column(db.Integer, db.ForeignKey("cursos.id"), nullable=False)
	feedback = db.relationship("Feedback", backref="actividades", lazy=True)

	def __repr__(self):
		return self.nombre


class Feedback(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	actividad = db.Column(db.Integer, db.ForeignKey("actividades.id"), nullable=False)
	feedback = db.Column(db.Text, nullable = False)
	#tag = db.Column(db.Text, db.ForeignKey("tags.id"), nullable=False)

	def __repr__(self):
		return self.feedback


class Tags(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tag = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return self.tag