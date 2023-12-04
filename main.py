from flask import Flask
from flask_cors import CORS
from routes.authentication_routes import auth_bp
from routes.market_routes import market_bp
from routes.collection_routes import collection_bp
from routes.card_routes import card_bp
from routes.transaction_routes import transaction_bp
from routes.cart_routes import cart_bp

# from service.user_service import UserService
# from service.card_service import CardService

app = Flask(__name__)

# For sessions
app.secret_key = '7103a98b1a7555d73e40990b'

#CORS(app)
CORS(app, supports_credentials=True, resources={r'*': {'origins': '*'}})


@app.route("/")
def main():
  #return render_template("homepage.html")
  return "Hello"


# Register the blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(collection_bp, url_prefix='/collection')
app.register_blueprint(market_bp, url_prefix='/market')
app.register_blueprint(card_bp, url_prefix='/card')
app.register_blueprint(transaction_bp, url_prefix='/transaction')
app.register_blueprint(cart_bp, url_prefix='/cart')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
