from flask import Flask, jsonify
from models import EmployeePerformance
from db import create_app, db
import pandas as pd

with open('dataset.csv', 'r', encoding='utf-8') as f:
    df = pd.read_csv(f)


app, db = create_app()
@app.route('/')
def index():
    with app.app_context():

        # Crear y añadir el objeto de rendimiento del  empleado

        for index,row in df.iterrows():
            employee_performance = EmployeePerformance(
                employee_id=row['employee_id'],
                department=row['department'],
                performance_score=row['performance_score'],
                years_with_company=row['years_with_company'],
                salary=row['salary']
            )
            db.session.add(employee_performance)
            db.session.commit()

        # Verificar que se haya añadido
        added_employee = EmployeePerformance.query.filter_by(employee_id=1).first()
        if added_employee:
            return 'Informacion del empleado creada'
        else:
            return 'Fallo al crear la informacion del empleado'

@app.route("/api")
def api():
    with app.app_context():
        getdata = EmployeePerformance.query.all()

        # Convertir los datos a JSON
        data = []
        for item in getdata:
            data.append({
                'id': item.id,
                'employee_id': item.employee_id,
                'department': item.department,
                'performance_score': item.performance_score,
                'years_with_company': item.years_with_company,
                'salary': item.salary
            })


        if data:
            return jsonify(data)
        else:
            return jsonify([])
        



"""
● Utilizar pandas para extraer los datos de la tabla EmployeePerformance.
● Calcular las siguientes estadísticas para cada departamento:
● Media, mediana y desviación estándar del performance_score.
● Media, mediana y desviación estándar del salary.
● Número total de empleados por departamento.
● Correlación entre years_with_company y performance_score.
● Correlación entre salary y performance_score.

"""

@app.route("/analisis")
def analisis():
    with app.app_context():
        # Leemos los datos de la base de datos
        data = pd.read_sql_query("SELECT * FROM employee_performance", db.engine)

        # agrupo por depa
        grouped_data = data.groupby("department")

        # Performance Score
        media_performance_score = grouped_data["performance_score"].mean()
        std_performance_score = grouped_data["performance_score"].std()
        mediana_performance_score = grouped_data["performance_score"].median()

        # Salary
        media_salary = grouped_data["salary"].mean()
        std_salary = grouped_data["salary"].std()
        mediana_performance_score = grouped_data["salary"].median()

        # Imprimimos los resultados
        return f"Media performance_score por departamento:{media_performance_score} Desviación estándar performance_score por departamento:{std_performance_score} Mediana performance_score por departamento:{mediana_performance_score}  Media salary por departamento:{media_salary} Desviación estándar salary por departamento:{std_salary} Mediana salary por departamento:{mediana_performance_score}"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
    analisis()
