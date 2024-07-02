from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'oleratomauwane02@gmail.com'
app.config['MAIL_PASSWORD'] = 'wszxderfc1'

db = SQLAlchemy(app)
mail = Mail(app)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    service = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    details = db.Column(db.Text, nullable=True)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            service = request.form['service']
            date = request.form['date']
            details = request.form.get('details', '')

            logging.debug(f"Booking data: name={name}, email={email}, phone={phone}, service={service}, date={date}, details={details}")

            # Validate form data
            if not name or not email or not phone or not service or not date:
                return jsonify({'success': False, 'message': 'Please fill in all required fields.'})

            # Save to database
            new_booking = Booking(name=name, email=email, phone=phone, service=service, date=date, details=details)
            db.session.add(new_booking)
            db.session.commit()

            # Send confirmation email
            msg = Message('Booking Confirmation', sender=app.config['MAIL_USERNAME'], recipients=[email])
            msg.body = f'Thank you for booking with us, {name}!\n\nHere are your booking details:\n\nService: {service}\nDate: {date}\n\nBest regards,\nPascal Ice-Cubes'
            mail.send(msg)

            return jsonify({'success': True})
        
        except Exception as e:
            db.session.rollback()
            logging.error(f"An error occurred in submit_booking: {e}", exc_info=True)
            return jsonify({'success': False, 'message': 'An error occurred while processing your booking. Please try again later.'})

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            message = request.form['message']

            logging.debug(f"Contact data: name={name}, email={email}, phone={phone}, message={message}")

            # Validate form data
            if not name or not email or not phone or not message:
                flash('Please fill in all the required fields.', 'error')
                return redirect(url_for('contact'))

            # Save to database
            new_contact = Contact(name=name, email=email, phone=phone, message=message)
            db.session.add(new_contact)
            db.session.commit()

            # Send notification email
            msg = Message('New Contact Form Submission', sender=app.config['MAIL_USERNAME'], recipients=['info@pascalicecubes.co.za'])
            msg.body = f'New contact form submission from {name}.\n\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}'
            mail.send(msg)

            flash('Contact form submitted successfully!', 'success')
            return redirect(url_for('contact'))
        
        except Exception as e:
            db.session.rollback()
            logging.error(f"An error occurred: {e}", exc_info=True)
            flash('An error occurred while processing your request. Please try again later.', 'error')
            return redirect(url_for('contact'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
