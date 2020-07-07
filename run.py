import os
from app import app

if __name__ == '__main__':
    config = app.config.get('CONFIG')

    if os.path.exists(config) == False:
        print('[!] Config file is not found.')
        os._exit(1)
    else:
        app.run()
