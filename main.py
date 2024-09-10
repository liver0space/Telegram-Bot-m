from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True,
                 host='0.0.0.0', port=5000, use_reloader=True, log_output=True)