from flaskr.app import create_app

slot_app = create_app()

if __name__ == '__main__':
    slot_app.run(debug=True,
            host='0.0.0.0', port=8888)