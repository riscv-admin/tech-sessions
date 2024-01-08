from flask import Flask, render_template, request, redirect, url_for
import requests, os

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit_form():
    # Collect form data
    data = request.form

    # Prepare data for GitHub issue
    title = f"New Tech Session Proposal: {data['presentationTitle']}"
    body = f"""
    Presenter Name: {data['presenterName']}
    Presentation Title: {data['presentationTitle']}
    Theme: {data.get('otherTheme') if data.get('classTheme') == 'other' else data.get('classTheme')}
    Presenter Bio: {data.get('presenterBio', '')}
    LinkedIn Profile: {data.get('linkedin', 'N/A')}
    Instagram Handle: {data.get('instagram', 'N/A')}
    Available Dates: {', '.join(data.getlist('availableDates'))}
    """

    github_token = os.getenv('GITHUB_TOKEN')
    github_user = os.getenv('GITHUB_USER')

    # Use GitHub API to create an issue
    url = "https://api.github.com/repos/riscv-admin/help/issues"
    headers = {
        "Authorization": "token " + github_token,
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "title": title,
        "body": body,
        "assignees": [github_user,],
        "labels": ["tech-session"]
    }

    response = requests.post(url, json=payload, headers=headers)

    # Inside your submit_form function in Flask app
    if response.status_code == 201:
        return redirect(url_for('success'))
    else:
        return "Failed to create GitHub issue."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html') 

if __name__ == '__main__':
    print (os.getenv('GITHUB_TOKEN'))
    print (os.getenv('GITHUB_USER'))
    app.run(debug=True)