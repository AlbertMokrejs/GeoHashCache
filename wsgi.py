from app import app

if __name__ == "__main__":
    app.secret_key = "app.secret_key"
    app.run()
