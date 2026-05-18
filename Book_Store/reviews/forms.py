from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from flask_babel import lazy_gettext as _l

class ReviewForm(FlaskForm):
    rating = SelectField(_l('Rating'), choices=[(5, '5 - Excellent'), (4, '4 - Good'), (3, '3 - Average'), (2, '2 - Poor'), (1, '1 - Terrible')], coerce=int, validators=[DataRequired()])
    content = TextAreaField(_l('Content'), validators=[DataRequired(), Length(min=5, max=500)])
    submit = SubmitField(_l('Submit Review'))
