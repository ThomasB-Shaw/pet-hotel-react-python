from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from dataclasses import dataclass

engine = create_engine("postgresql://localhost:5432/pet-hotel-python")
Session = sessionmaker(bind = engine)
session = Session()

## postgres:postgres was looking for the route of postgres which didn't exist. 
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost:5432/pet-hotel-python"
migrate = Migrate(app, db)

## this is our route to connect to DB 
@dataclass
class PetModel(db.Model):
    __tablename__ = 'pets'
    id = int
    name = str
    breed = str
    color = str
    is_checked_in = str
    owner_id = int

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    breed = db.Column(db.String())
    color = db.Column(db.String())
    is_checked_in = db.Column(db.String())
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))


    def __init__(self, name, breed, color, is_checked_in, owner_id):
        self.name = name
        self.breed = breed
        self.color = color
        self.is_checked_in = is_checked_in
        self.owner_id = owner_id

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'breed': self.breed,
            'color':self.color,
            'is_checked_in':self.is_checked_in,
            'owner_id':self.owner_id
        }

# @app.route('/pet', methods=['POST', 'GET'])
# def pet_get():
#     if request.method == 'POST':
#         if request.is_json:
#             data = request.get_json()
#             new_pet = PetModel(name=data['name'], breed=data['breed'], color=data['color'], is_checked_in=data['is_checked_in'], owner_id=data['owner_id'])
#             db.session.add(new_pet)
#             db.session.commit()
#             return {"message": f"pet {new_pet.name} has been birthed, congrats"}
#         else:
#             return {"error": "baby pet didn't make it, F in the chat"}
#     elif request.method == 'GET':
        # pets = PetModel.query.all()

        
#     return {"pets": results}

@app.route('/pet', methods=['POST', 'GET'])
def pet_get():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_pet = PetModel(name=data['name'], breed=data['breed'], color=data['color'], is_checked_in=data['is_checked_in'], owner_id=data['owner_id'])
            db.session.add(new_pet)
            db.session.commit()
            return {"message": f"pet {new_pet.name} has been birthed, congrats"}
        else:
            return {"error": "baby pet didn't make it, F in the chat"}
    elif request.method == 'GET':
        pets = PetModel.query.all()
        pet_results = [
            {   "id": pet.id,
                "name": pet.name,
                "breed": pet.breed,
                "color": pet.color,
                "is_checked_in": pet.is_checked_in,
                "owner_id": pet.owner_id
            } for pet in pets]
        results = session.query(PetModel).join(OwnerModel).all()
        for row in results:
            print(row)

        
        # for row in result:
            
        
    return  {"pets": pet_results , "owner": results} 

 
#########


# #########
# result = session.query(Customer).join(Invoice).filter(Invoice.amount == 8500)
# for row in result:
#    for inv in row.invoices:
#       print (row.id, row.name, inv.invno, inv.amount

##############OWNER GET / POST 
@dataclass
class OwnerModel(db.Model):
    __tablename__ = 'owner'
    id: int
    first_name = str
    last_name = str
    admin = bool

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    admin = db.Column(db.Boolean())


    def __init__(self, first_name, last_name, admin):
        self.first_name = first_name
        self.last_name = last_name
        self.admin = admin

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    # def serialize(self):
    #     return {
    #         'id': self.id, 
    #         'first_name': self.first_name,
    #         'last_name': self.last_name,
    #         'admin':self.admin,
    #     }

@app.route('/owner', methods=['POST', 'GET'])
def owner_get():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_owner = OwnerModel(first_name=data['first_name'], last_name=data['last_name'], admin=data['admin'])
            db.session.add(new_owner)
            db.session.commit()
            return {"message": f"owner {new_owner.first_name} has been birthed, congrats"}
        else:
            return {"error": "owner didn't make it, F in the chat"}
    elif request.method == 'GET':
        owners = OwnerModel.query.all()
        results = [
            {   "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "admin": owner.admin,
            } for owner in owners]
        
    return {"owners": results}


app.config['DEBUG'] = True


if __name__ == '__main__':
    app.run()
