from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField(
        'Location',
        validators=[
            DataRequired(),
            URL(require_tld=True, message="This is not a valid URL")
        ]
    )
    open = StringField('Open', validators=[DataRequired()])
    close = StringField('Close', validators=[DataRequired()])
    coffee = SelectField(
        'Coffee',
        validators=[DataRequired()],
        choices=["✘", "☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"]
    )
    wifi = SelectField(
        'Wifi',
        validators=[DataRequired()],
        choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"]
    )
    power = SelectField(
        'Power',
        validators=[DataRequired()],
        choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"]
    )
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a", encoding="utf8") as file:
            cafe = form.cafe.data
            location = form.location.data
            open_form = form.open.data
            close_form = form.close.data
            coffee = form.coffee.data
            wifi = form.wifi.data
            power = form.power.data
            file.write(f"\n{cafe},{location},{open_form},{close_form},{coffee},{wifi},{power}")
            return redirect(url_for("cafes"))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
