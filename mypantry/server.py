from flask import Flask
app = Flask(__name__)

@app.route('/')
def test():
  return 'Woohoo!'

if __name__ == "__main__":
  app.run(host="0.0.0.0")
