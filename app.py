from flask import Flask, render_template, request, json, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "super_secret_key_for_flash_messages"

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

# --- DASHBOARD ---
@app.route('/')
def dashboard():
    conn = get_db()
    if not conn: return "Database connection failed!", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM applications")
    apps_count = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM jobs")
    jobs_count = cursor.fetchone()['total']
    cursor.execute("SELECT status, COUNT(*) as count FROM applications GROUP BY status")
    status_stats = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', apps_count=apps_count, jobs_count=jobs_count, status_stats=status_stats)

# --- COMPANIES ---
@app.route('/companies', methods=['GET', 'POST'])
def companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        cursor.execute("""
            INSERT INTO companies (company_name, industry, website, city, state, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (request.form['name'], request.form['industry'], request.form['website'], 
              request.form['city'], request.form['state'], request.form['notes']))
        conn.commit()
    cursor.execute("SELECT * FROM companies")
    data = cursor.fetchall()
    conn.close()
    return render_template('companies.html', companies=data)

@app.route('/edit_company/<int:id>', methods=['POST'])
def edit_company(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE companies SET company_name=%s, industry=%s, website=%s, city=%s, state=%s, notes=%s
        WHERE company_id=%s
    """, (request.form['name'], request.form['industry'], request.form['website'], 
          request.form['city'], request.form['state'], request.form['notes'], id))
    conn.commit()
    conn.close()
    return redirect(url_for('companies'))

@app.route('/delete_company/<int:id>')
def delete_company(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM companies WHERE company_id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('companies'))

# --- JOBS ---
@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        skills = json.dumps([s.strip() for s in request.form['skills'].split(',')])
        cursor.execute("INSERT INTO jobs (company_id, job_title, requirements) VALUES (%s, %s, %s)",
                       (request.form['company_id'], request.form['title'], skills))
        conn.commit()
    cursor.execute("SELECT jobs.*, companies.company_name FROM jobs JOIN companies ON jobs.company_id = companies.company_id")
    data = cursor.fetchall()
    cursor.execute("SELECT company_id, company_name FROM companies")
    comps = cursor.fetchall()
    conn.close()
    return render_template('jobs.html', jobs=data, companies=comps)

@app.route('/edit_job/<int:id>', methods=['POST'])
def edit_job(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE jobs SET job_title=%s, company_id=%s, requirements=%s
        WHERE job_id=%s
    """, (request.form['title'], request.form['company_id'], request.form['skills'], id))
    conn.commit()
    conn.close()
    return redirect(url_for('jobs'))

@app.route('/delete_job/<int:id>')
def delete_job(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE job_id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('jobs'))

# --- APPLICATIONS ---
@app.route('/applications', methods=['GET', 'POST'])
def applications():
    conn = get_db()
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

@app.route('/update_application_status/<int:id>', methods=['POST'])
def update_app_status(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE applications SET status = %s WHERE application_id = %s", (request.form['status'], id))
    conn.commit()
    conn.close()
    return redirect(url_for('applications'))

@app.route('/delete_application/<int:id>')
def delete_application(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE application_id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('applications'))

# --- CONTACTS ---
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        cursor.execute("INSERT INTO contacts (contact_name, email, phone, company_id) VALUES (%s, %s, %s, %s)",
                       (request.form['contact_name'], request.form['email'], request.form['phone'], request.form['company_id']))
        conn.commit()
    
    cursor.execute("""
        SELECT contacts.*, companies.company_name 
        FROM contacts 
        LEFT JOIN companies ON contacts.company_id = companies.company_id
    """)
    data = cursor.fetchall()
    cursor.execute("SELECT company_id, company_name FROM companies")
    comps = cursor.fetchall()
    conn.close()
    return render_template('contacts.html', contacts=data, companies=comps)

@app.route('/edit_contact/<int:id>', methods=['POST'])
def edit_contact(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE contacts SET contact_name=%s, email=%s, phone=%s, company_id=%s
        WHERE contact_id=%s
    """, (request.form['contact_name'], request.form['email'], request.form['phone'], request.form['company_id'], id))
    conn.commit()
    conn.close()
    return redirect(url_for('contacts'))

@app.route('/delete_contact/<int:id>')
def delete_contact(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE contact_id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('contacts'))

# --- JOB MATCH ---
@app.route('/job_match', methods=['GET', 'POST'])
def job_match():
    matches = []
    if request.method == 'POST':
        user_skills_input = request.form['skills'].strip()
        if user_skills_input:
            user_skills = set([s.strip().lower() for s in user_skills_input.split(',')])
            conn = get_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT job_title, requirements FROM jobs")
            for job in cursor.fetchall():
                try:
                    job_skills = set([s.lower() for s in json.loads(job['requirements'])])
                    match_count = len(user_skills.intersection(job_skills))
                    total_skills = len(job_skills)
                    if total_skills > 0:
                        score = (match_count / total_skills) * 100
                        if score > 0:
                            matches.append({'title': job['job_title'], 'score': round(score)})
                except: continue
            conn.close()
    return render_template('job_match.html', matches=matches)

if __name__ == '__main__':
    app.run(debug=True)