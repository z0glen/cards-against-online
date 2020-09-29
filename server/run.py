from app import app, socketIO

if __name__ == '__main__':
    print("Running...")
    socketIO.run(app, host='0.0.0.0', debug=True, use_reloader=True)
