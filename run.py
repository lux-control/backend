from app import create_app

app = create_app()

@app.route("/")
def landing_page():
    return "HELLO WORLD"

if __name__ == "__main__":
    app.run(debug=True)