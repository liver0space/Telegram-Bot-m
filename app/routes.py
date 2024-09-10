import time

from flask import (Blueprint, jsonify, redirect, render_template, request,
                   session)

from app.extensions import db, socketio
from bot.api import send_api_request

from .models import Admin, User
from .security import admin_required, check_password, create_jwt

routes_bp = Blueprint('routes', __name__, url_prefix="/")
mailing_status = 'disabled'

@routes_bp.route("/")
def home():
    return render_template('home.html')

@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            if not username or not password:
                return render_template('login.html', error_message="Both username and password must be specified")

            admin = db.session.query(Admin).filter_by(
                username=username).first()

            if admin is None:
                return render_template('login.html', error_message="Username not found")

            if check_password(admin.password, password):
                token = create_jwt(admin)
                session['jwt_token'] = token
                return redirect('/send_message')
            else:
                return render_template('login.html', error_message="Invalid password")

        except Exception as e:
            return jsonify({'error': e}), 500
    else:
        return render_template('login.html')


@routes_bp.route('/stop_message', methods=['GET'])
@admin_required
def stop_mailing():
    global mailing_status
    mailing_status = 'disabled'
    return 'Mailing Stopped', 200


@routes_bp.route('/send_message', methods=['POST', 'GET'])
@admin_required
def send_message():
    global mailing_status
    if request.method == 'POST':

        if mailing_status == 'enabled':
            return "Mailing already started", 409
        else:
            text = request.form.get('text')
            image_url = request.form.get('image_url')

            users = User.query.all()

            progress = {
                'total_sent': 0,
                'sent': 0,
                'not_sent': 0,
                'total': len(users),
                'blocked': 0,
                'messaging_status': 'Active'
            }
            
            mailing_status = 'enabled'

            for user in users:
                if mailing_status == 'disabled':
                    break
                    
                send_api_request(user.user_id, text, progress, image_url)

                sent = progress['sent']
                not_sent = progress['not_sent']
                blocked = progress['blocked']
                progress['total_sent'] = sent + not_sent + blocked

                socketio.emit('progress', progress)

                time.sleep(0.1)


            progress['messaging_status'] = 'Finished'
            socketio.emit('progress', progress)

            mailing_status = 'disabled'

            return "Success", 200

    else:
        progress = {
            'total_sent': 0,
            'sent': 0,
            'not_sent': 0,
            'total': 0,
            'blocked': 0,
            'messaging_status': 'Not Active'
        }
        return render_template("send_message.html", **progress)

 


