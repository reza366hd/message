from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# تعریف اپلیکیشن Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# لیست کاربران متصل به سرور
users = []

# صفحهٔ اصلی پیامرسان
@app.route('/')
def index():
    return render_template('index.html')

# وقتی یک کاربر به سرور متصل می‌شود
@socketio.on('connect')
def connect():
    # افزودن کاربر به لیست کاربران
    users.append({'id': request.sid})
    print('یک کاربر به سرور متصل شد.')
    # اعلان ورود کاربر به سایر کاربران
    emit('user_connected', {'id': request.sid}, broadcast=True)

# وقتی یک کاربر از سرور قطع می‌شود
@socketio.on('disconnect')
def disconnect():
    # حذف کاربر از لیست کاربران
    user = next((user for user in users if user['id'] == request.sid), None)
    if user:
        users.remove(user)
        print('یک کاربر از سرور قطع شد.')
        # اعلان خروج کاربر به سایر کاربران
        emit('user_disconnected', {'id': request.sid}, broadcast=True)

# وقتی یک کاربر پیامی ارسال می‌کند
@socketio.on('send_message')
def send_message(data):
    print('پیام ارسال شد:', data)
    # ارسال پیام به سایر کاربران
    emit('receive_message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)