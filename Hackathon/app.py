# app.py
from flask import Flask, render_template, request
import os
import shutil
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Function to organize files
def organize_files(file_path):
    pdf_folder = os.path.join(file_path, 'PDFs')
    video_folder = os.path.join(file_path, 'Videos')
    audio_folder = os.path.join(file_path, 'Audios')
    image_folder = os.path.join(file_path, 'Images')
    docs_folder = os.path.join(file_path, 'Documents')
    zip_folder = os.path.join(file_path, 'ZIP')
    pptx_folder = os.path.join(file_path, 'PPTX')

    # Create directories if they don't exist
    for folder in [pdf_folder, video_folder, audio_folder, image_folder, docs_folder, zip_folder, pptx_folder]:
        os.makedirs(folder, exist_ok=True)

    # Categorize files based on extensions
    categorized_files = {
        'pdfs': [file for file in os.listdir(file_path) if file.lower().endswith('.pdf')],
        'videos': [file for file in os.listdir(file_path) if file.lower().endswith(('.mp4', '.m4a'))],
        'audios': [file for file in os.listdir(file_path) if file.lower().endswith('.mp3')],
        'images': [file for file in os.listdir(file_path) if file.lower().endswith(('.jpeg', '.jpg', '.png', '.webp'))],
        'docs': [file for file in os.listdir(file_path) if file.lower().endswith(('.docx', '.doc'))],
        'zips': [file for file in os.listdir(file_path) if file.lower().endswith('.zip')],
        'pptx': [file for file in os.listdir(file_path) if file.lower().endswith(('.pptx', '.ppt'))],
    }

    # Move files to respective folders
    for category, files in categorized_files.items():
        destination_folder = os.path.join(file_path, category.capitalize())
        for file in files:
            shutil.move(os.path.join(file_path, file), os.path.join(destination_folder, file))

    return {category: len(files) for category, files in categorized_files.items()}

# Function for web scraping
def scrape_website(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises HTTPError for bad responses
    soup = BeautifulSoup(response.content, 'html.parser')
    body_content = soup.body.get_text(separator='\n', strip=True)
    return body_content

# Function to send an email
def send_email(recipient, subject, body):
    sender_email = "youremail@example.com"       # Replace with your email
    sender_password = "yourpassword"             # Replace with your email password or app-specific password

    # Create the email content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/organize', methods=['GET', 'POST'])
def organize():
    if request.method == 'POST':
        file_path = request.form.get('directory')
        confirmation = request.form.get('confirm')

        if not file_path:
            return render_template('organize.html', error="Please enter a directory path.")

        if not os.path.exists(file_path):
            return render_template('organize.html', error="The specified path does not exist.")

        if confirmation.lower() == 'yes':
            try:
                organized_files = organize_files(file_path)
                return render_template('organize.html', success=True, result=organized_files)
            except Exception as e:
                return render_template('organize.html', error=f"An error occurred: {e}")
        else:
            return render_template('organize.html', error="Operation cancelled by user.")

    return render_template('organize.html')

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        url = request.form.get('url')

        if not url:
            return render_template('scrape.html', error="Please enter a URL.")

        try:
            scraped_content = scrape_website(url)
            return render_template('scrape.html', success=True, content=scraped_content)
        except Exception as e:
            return render_template('scrape.html', error=f"Error scraping website: {e}")

    return render_template('scrape.html')

@app.route('/sendmail', methods=['GET', 'POST'])
def sendmail():
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not recipient or not subject or not message:
            return render_template('sendmail.html', error="All fields are required.")

        if send_email(recipient, subject, message):
            return render_template('sendmail.html', success=True)
        else:
            return render_template('sendmail.html', error="Failed to send the email.")

    return render_template('sendmail.html')

if __name__ == '__main__':
    app.run(debug=True)
