from flask import Flask, make_response, jsonify, request
from infra.db_connection import session, SleepTracker

app = Flask(__name__)


@app.route('/dormir', methods=['POST'])
def post_dormir():
    sleep_data = request.json
    sleep_instance = SleepTracker(**sleep_data)
    session.add(sleep_instance)
    session.commit()

    return make_response(jsonify({'message': 'Sleep record created'}), 201)


@app.route('/resultados', methods=['GET'])
def get_sleep():
    sleep_records = session.query(SleepTracker).all()
    return make_response(
        jsonify([record.serialize() for record in sleep_records])
    )


@app.route('/apagar_tempo/<int:id>', methods=['DELETE'])
def delete_tempo(id):
    record = session.query(SleepTracker).filter_by(id=id).first()
    if record:
        session.delete(record)
        session.commit()
        return make_response(jsonify({'message': 'Record deleted'}), 200)
    return make_response(jsonify({'message': 'Record not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
