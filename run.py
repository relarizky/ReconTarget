import os

if __name__ == '__main__':
    config = os.getcwd() + '/config.json'

    if os.path.exists(config) == False:
        print('[!] Config file is not found.')
        os._exit(1)

    from app import app
    app.run()
