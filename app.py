from flask import Flask, request, jsonify
from pydantic import ValidationError
from models import Fruits
import json

app = Flask(__name__)

with open('fruits.json') as user_file:
  file_contents = user_file.read()

fruits = json.loads(file_contents)

@app.route('/fruits', methods=['GET'])
def get_fruits():
    color = request.args.get('color')
    season = request.args.get('season')

    if (type(color) != str) or (type(season) != str):
        return jsonify({"Error":"Invalid type, please provide correct input."}), 400

    filtered_fruits = [fruit for fruit in fruits if
                       (color is None or fruit['color'].lower() == color.lower()) and
                       (season is None or fruit['season'].lower() == season.lower())]
    
    if len(filtered_fruits):
        return jsonify(filtered_fruits), 200
    else:
        return jsonify({"Error": "No match found"}), 400

@app.route('/fruits', methods=['POST'])
def add_fruit():
    new_fruit = request.json
    print("request: -> ")
    print(new_fruit)
    try:
        new_fruit_val = Fruits(**new_fruit)
    except ValidationError as e:
        return jsonify({"Error": str(e)}), 400
    
    fruits.append(new_fruit)
    with open('fruits.json', 'w') as f:
        json.dump(fruits, f, indent=4)

    return jsonify(new_fruit), 201

@app.route('/compare', methods=['GET'])
def compare_fruits():
    fruit1_name = request.args.get('fruit1')
    fruit2_name = request.args.get('fruit2')

    if fruit1_name == fruit2_name:
        return jsonify({"error": "Invalid input"}), 400

    if not fruit1_name or not fruit2_name:
        return jsonify({"error": "Please provide both fruit1 and fruit2 query parameters"}), 400

    fruit1 = next((fruit for fruit in fruits if fruit["name"].lower() == fruit1_name.lower()), None)
    fruit2 = next((fruit for fruit in fruits if fruit["name"].lower() == fruit2_name.lower()), None)

    if not fruit1 or not fruit2:
        return jsonify({"error": "One or both of the fruits not found"}), 404


    # Extract sugar content and compare
    sugar1 = float(fruit1["nutrition"]["sugar"].replace('g', ''))
    sugar2 = float(fruit2["nutrition"]["sugar"].replace('g', ''))

    if sugar1 < sugar2:
        healthier = fruit1
    else:
        healthier = fruit2

    return jsonify({
        "healthier_fruit": healthier["name"],
        "sugar_content": healthier["nutrition"]["sugar"]
    })

if __name__ == '__main__':
    app.run(debug=True)
