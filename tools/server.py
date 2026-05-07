from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def home():
   return render_template("C:/Users/heric/PycharmProjects/TCC/gui/login/login.html")
@app.route("/sobre")
def sobre():
   return "Esta é a página Sobre."
if __name__ == "__main__":
   app.run(debug=True)