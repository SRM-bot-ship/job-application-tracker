Tools Used
ChatGPT (GPT-4): For generating and refining Flask routes, SQL queries, and overall backend logic.
Claude: Assisted with debugging, code review, and improving Flask error handling.
Gemini: Helped brainstorm and improve the Job Match feature's algorithm by suggesting improvements and optimizations.


Key Prompts
"Generate a Flask route for displaying a dashboard with basic statistics from the applications table."
ChatGPT helped generate the code for displaying total application counts, job counts, and the status breakdown of applications in the dashboard route.
"Write a Flask form to add new companies, and make sure to validate required fields."
This prompt was used to create the POST handling for adding companies, and it also generated a basic validation logic to ensure required fields (name, industry, city, and state) were filled out before submitting.
"Create a job matching algorithm that compares user skills with job requirements and returns a match percentage."
The AI generated the core of the job match algorithm. It suggested using sets to compare skills, and calculated the percentage match based on the number of skills the user had in common with the job’s required skills.
"Generate SQL queries to display job applications by status, and job information using JOIN."
AI provided optimized SQL queries to fetch application statistics and join job data for the applications page, which was later adjusted for better performance.
"How can I optimize a Flask form that accepts CSV data for bulk job insertion?"
This helped refine the logic for adding jobs, even though CSV bulk insertion wasn't implemented directly, but the prompt guided thinking on how to handle multiple jobs efficiently.


What Worked Well
Flask Routes: The AI-generated CRUD routes for companies, jobs, and applications were useful for quickly setting up the basic functionality. The routes also included error handling, which helped speed up development.
Job Matching Algorithm: The initial job matching algorithm was quite efficient. It correctly identified common skills between the user and jobs by converting both skill lists into sets, and it calculated the match percentage accurately.
Error Handling in Flask: ChatGPT’s suggestions for handling database connection failures and form validation were very helpful, especially in preventing the app from crashing and providing meaningful error messages to users.
SQL Queries: The AI-generated SQL queries for the dashboard and for fetching applications were functional, and they correctly used JOIN to pull data from multiple tables.


What I Modified
Variable Naming: The variable names suggested by AI were generally useful but I had to rename a few variables to better reflect the database schema. For example, job_id_fk was renamed to job_id to align with the schema.
Input Validation: While AI provided basic form validation logic, I added extra checks for edge cases (such as empty or invalid form data). Additionally, I implemented more detailed error messages, particularly for users filling out the job application form.
Job Matching Algorithm Adjustments: The AI’s initial implementation compared skills as exact matches. I expanded this logic by including partial matches, where skills like “Python” and “python” would now be treated as equivalent (case-insensitive matching).
Database Query Optimizations: I optimized some of the SQL queries to make them more efficient by ensuring that the JOIN conditions and indices were set up correctly, which wasn't explicitly covered in the AI's suggestions.
Improved UI Rendering: While the AI suggested a basic way to pass data from Flask to the template, I modified the rendering process to ensure a better user experience, such as passing the matches variable for job matching results and adding additional CSS classes for styling.


Lessons Learned
Testing AI Code: I learned that while AI-generated code is helpful, it often requires additional testing and validation. I found several cases where variable names needed to be modified, and some queries had performance issues when tested with a large database.
Iterative Development: AI is great for generating quick solutions, but the best results come from iterating on AI suggestions and combining them with manual debugging and refinement. I found that AI is excellent for providing a foundation, but it needs human customization to meet specific project needs.
Improving Code Structure: The AI helped me structure the app’s routes logically, but I also learned the importance of adding extra error handling, validation, and edge case handling that AI sometimes overlooks.
Job Match Feature: The job matching algorithm worked well out of the box but needed some tweaks, like case-insensitive matching and handling incomplete job requirements. The AI’s suggestion to use sets for matching skills was useful, but it required refinement to handle edge cases and ensure more accurate matches.
SQL Query Debugging: The AI was very helpful in generating queries, but sometimes I had to rework them for optimization. I also learned that using JOIN effectively can prevent performance problems when fetching large amounts of data from related tables.
