from app import create_app
import os

if __name__ == '__main__':
    app = create_app()
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=True, host='0.0.0.0', port=5001)
