from flask_wtf import FlaskForm
from wtforms import SubmitField

class formAgendaVuelos(FlaskForm):
    listaritinerario = SubmitField('Itinerario', render_kw={'class':'form_boton', 'onmouseover':'listarAgenda()'})

class formAgendaVuelos(FlaskForm):
    listarcomentarios = SubmitField('Itinerario', render_kw={'class':'form_boton', 'onmouseover':'listarAgenda()'})

class formAgendaVuelos(FlaskForm):
    editarcomentarios = SubmitField('Editar', render_kw={'class':'form_boton', 'onmouseover':'editarComentario()'})

class formAgendaVuelos(FlaskForm):
    eliminarcomentarios = SubmitField('Eliminar', render_kw={'class':'form_boton', 'onmouseover':'eliminarComentario()'})