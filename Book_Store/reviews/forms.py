from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_babel import lazy_gettext as _l

class ReviewForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired(), Length(min=3, max=100)])
    content = TextAreaField(_l('Content'), validators=[DataRequired(), Length(min=5, max=500)])
    submit = SubmitField(_l('Submit Review'))
