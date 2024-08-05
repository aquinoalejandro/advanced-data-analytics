from db import db

class EmployeePerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer)
    department = db.Column(db.String(50))
    performance_score = db.Column(db.Float)
    years_with_company = db.Column(db.Integer)
    salary = db.Column(db.Float)
