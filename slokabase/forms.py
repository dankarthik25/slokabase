#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
# from wtforms.validators import DataRequired, Length
#from wtforms.widgets import TextArea
#from wtforms.validators import DataRequired, Length, Email, EqualTo
#
#
#class RegistrationForm(FlaskForm):
#    username = StringField('Username',
#                           validators=[DataRequired(), Length(min=2, max=20)])
#    email = StringField('Email',
#                        validators=[DataRequired(), Email()])
#    password = PasswordField('Password', validators=[DataRequired()])
#    confirm_password = PasswordField('Confirm Password',
#                                     validators=[DataRequired(), EqualTo('password')])
#    submit = SubmitField('Sign Up')
#
#
#class LoginForm(FlaskForm):
#    email = StringField('Email',
#                        validators=[DataRequired(), Email()])
#    password = PasswordField('Password', validators=[DataRequired()])
#    remember = BooleanField('Remember Me')
#    submit = SubmitField('Login')
#
#class SongIndex(FlaskForm):
#    song_name = StringField('song_name',validators=[DataRequired(), Length(min=2)])
#    song_short_name = StringField('song_short_name')
#    division = StringField('division')
#    division_no = IntegerField('division_no')
#    sloka_statues = BooleanField('sloka_statues',validators=[DataRequired()],default=True)
#    total_slokas = IntegerField('total_slokas',validators=[DataRequired()])   # Total No.of Sloka 
#    group = StringField('group')
#    devotion_god = StringField('devotion_god')
#    author = StringField('author')
#    describtion = StringField('describtion', widget=TextArea())
#    # WTForms for efficient forms validation and rendering in Flask https://www.youtube.com/watch?v=j5IQI4aW9ZU
#    # Instead of Stringfiled we need textarea
#    # Retrieve text from textarea in Flask : https://www.youtube.com/watch?v=mAfUSjncjnM 
#    other_links = StringField('other_links', widget=TextArea())
#    submit = SubmitField('Song Index Submit')
#
#class Song_Details(FlaskForm):
#    sloka_no = IntegerField('sloka_no')
#    sloka_lang_hindi =  StringField('sloka_lang_hindi')
#    sloka_lang_eng =  StringField('sloka_lang_eng')
#    synonyms = StringField('sysnonyms')
#    translation = StringField('translation')
#    purpot = StringField('purpot')
#    submit = SubmitField('Song Details Submit')
