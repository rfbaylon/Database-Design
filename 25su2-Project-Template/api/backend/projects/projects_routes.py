from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

projects = Blueprint('projects', __name__)
    
# ------------------------------------------------------------
# This is a POST route to add a new product.
# Remember, we are using POST routes to create new entries
# in the database. 
@projects.route('/addproject', methods=['POST'])
def add_new_project():
    
    # In a POST request, there is a 
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(f'Add Project Data: {the_data}')

    #extracting the variable
    userID = the_data.get('userID')
    tagID = the_data.get('tagID')
    title = the_data.get('title')
    notes = the_data.get('notes')
    status = the_data.get('status', 'onIce')
    priority = the_data.get('priority', 4)
    completedAt = the_data.get('completedAt')
    schedule = the_data.get('schedule')

    
    query = '''
        INSERT INTO goals (userID,
                              tagID,
                              title, 
                              notes,
                              status,
                              priority,
                              completedAt,
                              schedule)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    # TODO: Make sure the version of the query above works properly
    # Constructing the query
    # query = 'insert into products (product_name, description, category, list_price) values ("'
    # query += name + '", "'
    # query += description + '", "'
    # query += category + '", '
    # query += str(price) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query, (userID, tagID, title, notes, status, priority, completedAt, schedule))
    db.get_db().commit()
    
    response = make_response("Successfully added project")
    response.status_code = 202
    return response

@projects.route('/completedprojects', methods=['GET'])
def view_completed_projects():
    query = '''
        SELECT * FROM goals WHERE status = 'completed'
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    completed_projects = cursor.fetchall()

    if not completed_projects:
        return jsonify({"message": "No completed projects found"}), 404

    response = make_response(jsonify(completed_projects))
    response.status_code = 200
    return response

@projects.route('/projecttags', methods=['GET'])
def view_projects_by_tags():
    query = '''
        SELECT * FROM goals WHERE tagID IS NOT NULL
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    projects_by_tags = cursor.fetchall()

    if not projects_by_tags:
        return jsonify({"message": "No projects found with tags"}), 404

    response = make_response(jsonify(projects_by_tags))
    response.status_code = 200
    return response

@projects.route('/projectprioity', methods=['GET'])
def view_projects_by_priority():
    query = '''
        SELECT * FROM goals ORDER BY priority DESC
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    projects_by_priority = cursor.fetchall()

    if not projects_by_priority:
        return jsonify({"message": "No projects found"}), 404

    response = make_response(jsonify(projects_by_priority))
    response.status_code = 200
    return response