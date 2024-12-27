from app import app

port = 2020

if __name__ == "__main__":
    app.run(debug=True, port=port, host='0.0.0.0')