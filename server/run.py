from app import app, socketIO

if __name__ == '__main__':
    print("Running...")
    socketIO.run(app, host='127.0.0.1')
