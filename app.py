from flask import Flask, render_template, request, json
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Jan@2025',
    'database': 'job_tracker'
}

def get_db():
    try:
        return mysql.connector.connect(**db_config)
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

@app.route('/')
def dashboard():
    conn = get_db()
    if not conn:
        return "Database connection failed!", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM applications")
    apps_count = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM jobs")
    jobs_count = cursor.fetchone()['total']
    cursor.execute("SELECT status, COUNT(*) as count FROM applications GROUP BY status")
    status_stats = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', apps_count=apps_count, jobs_count=jobs_count, status_stats=status_stats)

@app.route('/companies', methods=['GET', 'POST'])
def companies():
    conn = get_db()
    if not conn:
        return "Database connection failed!", 500
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        industry = request.form['industry']
        website = request.form['website']
        city = request.form['city']
        state = request.form['state']
        notes = request.form['notes']
        if not name or not industry or not city or not state:
            return "All required fields must be filled out!", 400
        cursor.execute("""
            INSERT INTO companies (company_name, industry, website, city, state, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, industry, website, city, state, notes))
        conn.commit()
    cursor.execute("SELECT * FROM companies")
    data = cursor.fetchall()
    conn.close()
    return render_template('companies.html', companies=data)

@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    conn = get_db()
    if not conn:
        return "Database connection failed!", 500
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        company_id = request.form['company_id']
        title = request.form['title']
        skills = json.dumps([s.strip() for s in request.form['skills'].split(',')])
        cursor.execute("""
            INSERT INTO jobs (company_id, job_title, requirements)
            VALUES (%s, %s, %s)
        """, (company_id, title, skills))
        conn.commit()
    cursor.execute("""
        SELECT jobs.*, companies.company_name FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
    """)
    data = cursor.fetchall()
    cursor.execute("SELECT company_id, company_name FROM companies")
    comps = cursor.fetchall()
    conn.close()
    return render_template('jobs.html', jobs=data, companies=comps)

@app.route('/applications', methods=['GET', 'POST'])
def applications():
    conn = get_db()
    if not conn:
        return "Database connection failed!", 500
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        cursor.execute("INSERT INTO applications (job_id, application_date, status) VALUES (%s, %s, %s)",
                       (request.form['job_id'], request.form['date'], request.form['status']))
        conn.commit()
    cursor.execute("SELECT applications.*, jobs.job_title FROM applications JOIN jobs ON applications.job_id = jobs.job_id")
    data = cursor.fetchall()
    cursor.execute("SELECT job_id, job_title FROM jobs")
    job_list = cursor.fetchall()
    conn.close()
    return render_template('applications.html', applications=data, jobs=job_list)

@app.route('/contacts')
def contacts():
    conn = get_db()
    if not conn:
        return "Database connection failed!", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contacts")
    data = cursor.fetchall()
    conn.close()
    return render_template('contacts.html', contacts=data)

@app.route('/job_match', methods=['GET', 'POST'])
def job_match():
    matches = []
    if request.method == 'POST':
        user_skills_input = request.form['skills'].strip()
        if user_skills_input:
            user_skills = set([s.strip().lower() for s in user_skills_input.split(',')])
            conn = get_db()
            if not conn:
                return "Database connection failed!", 500
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT job_title, requirements FROM jobs")
            all_jobs = cursor.fetchall()
            for job in all_jobs:
                job_title = job['job_title']
                job_skills = set([s.lower() for s in json.loads(job['requirements'])])
                matching_skills = user_skills.intersection(job_skills)
                match_count = len(matching_skills)
                total_skills = len(job_skills)
                if total_skills > 0:
                    match_percentage = (match_count / total_skills) * 100
                else:
                    match_percentage = 0
                if match_percentage > 0:
                    matches.append({'title': job_title, 'score': round(match_percentage)})
            conn.close()
    return render_template('job_match.html', matches=matches)

if __name__ == '__main__':
    app.run(debug=True)