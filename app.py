from flask import Flask, request, jsonify
from models import db, Team

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "API is running!"})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    if Team.query.count() == 0:
        teams_data = [
            Team(name="India", captain="STQA Exam", ranking=1),
            Team(name="Australia", captain="STQA Exam", ranking=2),
            Team(name="South Africa", captain="STQA Exam", ranking=3),
            Team(name="West Indies", captain="STQA Exam", ranking=4),
            Team(name="New Zealand", captain="STQA Exam", ranking=5),
            Team(name="England", captain="STQA Exam", ranking=6),
            Team(name="Pakistan", captain="STQA Exam", ranking=7),
            Team(name="Bangladesh", captain="STQA Exam", ranking=8),
            Team(name="Sri Lanka", captain="STQA Exam", ranking=9),
        ]
        db.session.bulk_save_objects(teams_data)
        db.session.commit()

@app.route('/teams', methods=['GET'])
def get_teams():
    teams = Team.query.all()
    return jsonify([team.to_dict() for team in teams])

@app.route('/teams/<int:id>', methods=['GET'])
def get_team(id):
    team = Team.query.get_or_404(id)
    return jsonify(team.to_dict())

@app.route('/teams', methods=['POST'])
def add_team():
    data = request.json
    new_team = Team(
        name=data['name'],
        captain=data['captain'],
        ranking=data['ranking']
    )
    db.session.add(new_team)
    db.session.commit()
    return jsonify(new_team.to_dict()), 201

@app.route('/teams/<int:id>', methods=['PUT'])
def update_team(id):
    team = Team.query.get_or_404(id)
    data = request.json
    team.name = data.get('name', team.name)
    team.captain = data.get('captain', team.captain)
    team.ranking = data.get('ranking', team.ranking)
    db.session.commit()
    return jsonify(team.to_dict())

@app.route('/teams/<int:id>', methods=['DELETE'])
def delete_team(id):
    team = Team.query.get_or_404(id)
    db.session.delete(team)
    db.session.commit()
    return jsonify({"message": "Team deleted"})

if __name__ == '__main__':
    app.run(debug=True)