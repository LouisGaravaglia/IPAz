from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DecimalField
from wtforms.validators import InputRequired, Optional, NumberRange, URL, AnyOf, Length, Email, DataRequired

class ReviewForm(FlaskForm):
    """Form for adding/editing reviews."""
    rating = DecimalField('Rating', validators=[NumberRange(min=0, max=100, message='Value needs to be between 0 and 100.'), DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    
class EditReviewForm(FlaskForm):
    """Form for adding/editing reviews."""
    rating = DecimalField('Rating', validators=[NumberRange(min=0, max=100, message='Value needs to be between 0 and 100.'), DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])

class UserAddForm(FlaskForm):
    """Form for adding users."""
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class EditUserForm(FlaskForm):
    """Form for editing a user."""
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
     

