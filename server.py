from flask import Flask, request, jsonify
import pymysql



app = Flask(__name__)


DB_CONFIG =  {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "dbVerano",
    "cursorclass": pymysql.cursors.DictCursor
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)


@app.route("/employees", methods=["GET", "POST"])
def get_add():
    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            if request.method == "GET":
                cursor.execute(
                    """
                    SELECT 
                        id,
                        full_name,
                        position,
                        department,
                        address,
                        gender,
                        email,
                        contact_no,
                        birth_date,
                        date_hired
                    FROM tblEmployees
                    """
                )
                employees = cursor.fetchall()

                if employees is None:
                    return jsonify({
                        "message": "Employees are not found."
                    }), 404

                for employee in employees:
                    if employee["birth_date"] or employee["date_hired"]:
                        employee["birth_date"] = employee["birth_date"].isoformat()
                        employee["date_hired"] = employee["date_hired"].isoformat()

                return jsonify(employees), 200

            user_input = request.get_json()

            if user_input is None:
                return jsonify({
                    "message": "Please fill all field before submit."
                }), 400

            cursor.execute(
                """
                INSERT INTO tblEmployees
                    (
                        id,
                        full_name,
                        position,
                        department,
                        address,
                        gender,
                        email,
                        contact_no,
                        birth_date,
                        date_hired
                    )
                VALUES
                    (%s, %s, %s, %s, %s, %s)
                """,
                (
                    user_input.get("full_name"),
                    user_input.get("position"),
                    user_input.get("department"),
                    user_input.get("address"),
                    user_input.get("gender"),
                    user_input.get("email"),
                    user_input.get("contact_no"),
                    user_input.get("birth_date"),
                    user_input.get("date_hired")
                )
            )

            conn.commit()

            return jsonify({
                "message": "Added successfully."
            }), 201

    except Exception as e:
        print(f"Error: {e}")
        jsonify({
            "message": str(e)
        }), 500
        
    finally:
        if conn: conn.close()


@app.route("/employees/<int:id>", methods=["GET", "PUT", "DELETE"])
def get_update_delete(id):
    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cursor:

            if request.method == "GET":
                cursor.execute(
                    """
                    SELECT 
                        id,
                        full_name,
                        position,
                        department,
                        address,
                        gender,
                        email,
                        contact_no,
                        birth_date,
                        date_hired
                    FROM tblEmployees
                    WHERE id = %s
                    """,
                    (id,)
                )

                employee = cursor.fetchone()

                if employee is None:
                    return jsonify({
                        "message": "Employee is not found."
                    }), 404

                if employee["birth_date"] or employee["date_hired"]:
                    employee["birth_date"] = employee["birth_date"].isoformat()
                    employee["date_hired"] = employee["date_hired"].isoformat()


                return jsonify(employee), 200

            elif request.method == "PUT":
                employee = request.get_json()

                cursor.execute(
                    """
                    SELECT id FROM tblEmployees WHERE id = %s
                    """,
                    (id,)
                )
                if cursor.fetchone() is None:
                    return jsonify({"message": "Employee is not found."}), 404
                
                cursor.execute(
                    """
                    UPDATE tblEmployees
                    SET
                        full_name   = %s,
                        position    = %s,
                        department  = %s,
                        address     = %s,
                        gender      = %s,
                        email       = %s,
                        contact_no  = %s,
                        birth_date  = %s,
                        date_hired  = %s
                    WHERE id        = %s
                    """,
                    (
                        employee.get("full_name"),
                        employee.get("position"),
                        employee.get("department"),
                        employee.get("address"),
                        employee.get("gender"),
                        employee.get("email"),
                        employee.get("contact_no"),
                        employee.get("birth_date"),
                        employee.get("date_hired")
                    )
                )
                conn.commit()

            elif request.method == "DELETE": 
                cursor.execute(
                    """
                    SELECT id FROM tblEmployees WHERE id = %s
                    """,
                    (id,)
                )
                if cursor.fetchone() is None:
                    return jsonify({"message": "Employee is not found."}), 404
                
                
                cursor.execute(
                    """
                    DELETE FROM tblEmployees WHERE id = %s
                    """
                )

    except Exception as e:
        if conn: conn.rollback()
        return jsonify({
            "message": str(e)
        })
    
    finally:
        if conn:conn.close()
        



if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)