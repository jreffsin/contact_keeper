from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, BooleanField, SelectField
from wtforms.validators import InputRequired, Length, Email, Regexp, Optional, DataRequired

class ContactForm(FlaskForm):
    first_name = StringField('First Name *', 
                             validators=[InputRequired(), Length(min=1, max=50)], render_kw={"autofocus": True})
    middle_name = StringField('Middle Name', 
                             validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name *', 
                             validators=[InputRequired(), Length(min=1, max=50)])
    email = StringField('Email', 
                        validators=[Optional(), Email(), Length(max=100)])
    phone = StringField('Phone', 
                        validators=[Optional()])
    submit = SubmitField('Add Contact')

class AddressForm(FlaskForm):
    street_1 = StringField('Street Line 1 *', 
                            validators=[InputRequired(), Length(min=1, max=100)], render_kw={"autofocus": True})
    street_2 = StringField('Street Line 2', 
                            validators=[Optional(), Length(max=100)])
    city = StringField('City *', 
                            validators=[InputRequired(), Length(min=1, max=100)])
    state = SelectField(
        'State *',
        choices=[('', 'Please select...'),
            ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
            ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
            ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
            ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
            ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
            ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'),
            ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'),
            ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'),
            ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
            ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'),
            ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'),
            ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
            ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'),
            ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
            ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
            # Territories
            ('AS', 'American Samoa'), ('DC', 'District of Columbia'), 
            ('FM', 'Federated States of Micronesia'), ('GU', 'Guam'), 
            ('MH', 'Marshall Islands'), ('MP', 'Northern Mariana Islands'), 
            ('PW', 'Palau'), ('PR', 'Puerto Rico'), ('VI', 'Virgin Islands')], 
            validators=[InputRequired()])
    zip = StringField('Zip Code *', 
                        validators=[InputRequired(), 
                        Regexp(regex=r'[\d]{5}(-[\d]{4})?', message="Zip code must be in either 5 or 9 digit format")])
    is_primary = BooleanField('Set as primary', validators=[Optional()])
    contact_id = HiddenField('Contact ID', validators=[DataRequired()])
    submit = SubmitField('Add Address')
    
