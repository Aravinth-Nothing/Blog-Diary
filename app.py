import sqlite3
import hashlib
from flask import Flask, render_template, request, redirect, session
import datetime 
from datetime import date, timedelta  
import base64
from PIL import Image
import io
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def hash_password(password):
    # Hashes the password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()
def compress_image(image_file):
    image = Image.open(image_file)
    
    # Convert RGBA image to RGB
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    # Create a BytesIO object to store the compressed image
    compressed_image_data = io.BytesIO()
    
    # Compress and save the image to the BytesIO object
    image.save(compressed_image_data, format='JPEG', quality=70)
    
    # Reset the file pointer to the beginning of the BytesIO object
    compressed_image_data.seek(0)
    
    return compressed_image_data


def calculate_streak(dates,day):
    streak = 0
    current_streak = 0
    today = date.today()
    if day==1:
        today = today - timedelta(days=1)

    for d in dates:
        blog_date = datetime.datetime.strptime(d[0], '%dth %B, %Y').date()  # Convert date string to date object
        if (today - blog_date).days == current_streak:
            current_streak += 1
        else:
            break

    streak = current_streak
    return streak
    
def save_image_to_database(compressed_image, entry_id):
    image_data = compressed_image.getvalue()

    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO content_images (entry_id, image_data) VALUES (?, ?)",
                   (entry_id, image_data))
    conn.commit()
    conn.close()



@app.route('/', methods=['GET', 'POST'])
def login():
    session.pop('username', None)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = hash_password(password)
        
        # Connect to the database
        conn = sqlite3.connect('blog.db')
        
        # Retrieve the hash value for the given username from the database
        cursor = conn.execute('SELECT password_hash,user_no FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()

        if row is not None:
            stored_hash = row[0]
            user_no=row[1]
            if hashed_password == stored_hash:
                session['username'] = username
                session['user_no'] = user_no
                conn.close()  # Close the database connection
                return redirect('/home')
        
        error = 'Invalid username or password'
        conn.close()  # Close the database connection
        return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/home')
def home():
    todays_entry = "Make Today's Entry"
    if 'username' not in session:
        return redirect('/')

    username = session['username']

    # Retrieve the list of blog entries from the database
    conn = sqlite3.connect('blog.db')
    entry_date_raw = datetime.datetime.now().strftime('%d')

# Determine the appropriate suffix for the date number
    suffix = "th"
    if entry_date_raw[-1] == '1' and entry_date_raw != '11':
        suffix = "st"
    elif entry_date_raw[-1] == '2' and entry_date_raw != '12':
        suffix = "nd"
    elif entry_date_raw[-1] == '3' and entry_date_raw != '13':
        suffix = "rd"

    # Format the complete date string with the correct suffix
    cursor = conn.execute("SELECT user_no FROM users WHERE username = ?", (username,))
    user_no = cursor.fetchone()[0]
    cursor=conn.execute("SELECT entry_date FROM content WHERE user_no = ? ORDER BY entry_date DESC",(user_no,))
    dates=cursor.fetchall()
    entry_date = entry_date_raw + suffix + datetime.datetime.now().strftime(' %B, %Y')
    cursor = conn.execute("SELECT COUNT(*) FROM content WHERE user_no = ? AND entry_date = ?",
                          (user_no, entry_date))
    entry_count = cursor.fetchone()[0]
    streak=calculate_streak(dates,1)
    if entry_count > 0:
        # User has already created a blog entry today, display an error message
        todays_entry = "Today's Entry Made Already"
        streak = calculate_streak(dates,0)
    conn.commit()
    cursor = conn.execute('SELECT * FROM content WHERE user_no = ?', (user_no,))
    blog_entries = cursor.fetchall()
    conn.close()
    return render_template('home.html', username=username, blog_entries=blog_entries, todays_entry=todays_entry, streak=streak)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            error_message = 'Passwords do not match. Please try again.'
            return render_template('register.html', error=error_message)
        
        hashed_password = hash_password(password)
        
        # Connect to the database
        conn = sqlite3.connect('blog.db')
        
        # Check if the user already exists
        cursor = conn.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            # User already exists, handle the error (e.g., show an error message)
            error_message = 'User already exists. Please choose a different username.'
            return render_template('register.html', error=error_message)
        
        # Insert a new user record into the 'users' table
        conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        
        conn.close()  # Close the database connection
        
        return redirect('/')
    
    return render_template('register.html')

@app.route('/write', methods=['GET', 'POST'])
def write():
    if 'username' not in session:
        return redirect('/')
    username = session['username']

    if request.method == 'POST':
        # Process the form submission and handle uploaded pictures
        title = request.form['title']
        content = request.form['content']

        # Get the current user ID
        conn = sqlite3.connect('blog.db')
        cursor = conn.execute("SELECT user_no FROM users WHERE username = ?", (username,))
        user_no = cursor.fetchone()[0]

        # Get the current date and time
        entry_date = datetime.datetime.now().strftime('%dth %B, %Y')

        cursor = conn.execute("SELECT COUNT(*) FROM content WHERE user_no = ? AND entry_date = ?",
                              (user_no, entry_date))
        entry_count = cursor.fetchone()[0]
        if entry_count > 0:
            # User has already created a blog entry today, display an error message
            todays_entry = "You have already created a blog entry today."
            return render_template('write.html', todays_entry=todays_entry)

        # Save the blog entry to the database
        conn.execute("INSERT INTO content (user_no, entry_date, content, title) VALUES (?, ?, ?, ?)",
                     (user_no, entry_date, content, title))
        cursor1 = conn.execute("SELECT * FROM content ORDER BY entry_id DESC LIMIT 1")
        entry_id = cursor1.fetchone()[0]
        conn.commit()

        # Get the entry_id of the newly inserted blog entry
        image_file = request.files['filefield']

        # Check if an image was uploaded
        if image_file:
            # Open the image using Pillow
            img = Image.open(image_file)

            # Compress the image (adjust the size as needed)
            img = img.convert('RGB')

            # Convert the compressed image to base64
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            compressed_image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')

            # Insert the compressed image data into the database
            conn = sqlite3.connect('blog.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO content_images (entry_id, image_data) VALUES (?, ?)",
                           (entry_id, compressed_image_data))
            conn.commit()
            conn.close()

        return redirect('/home')
    return render_template('write.html', username=username)

@app.route('/blog/<int:entry_id>')
def blog(entry_id):
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    conn = sqlite3.connect('blog.db')
    cursor = conn.execute("SELECT * FROM content WHERE entry_id = ?", (entry_id,))
    cursor1 = conn.execute("SELECT * FROM content_images WHERE entry_id = ?", (entry_id,))
    entry = cursor.fetchone()
    image = cursor1.fetchone()
    conn.close()
    date = entry[2]
    title = entry[3]
    content = entry[4]
    image_data = image[2] if image is not None else None
    return render_template('blog.html', title=title, content=content, image_data=image_data, username=username, date=date)

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'], )
def edit(entry_id):
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    if request.method == 'POST':
        # Process the form submission and update the blog entry
        title = request.form['title']
        content = request.form['content']

        # Update the blog entry in the database
        conn = sqlite3.connect('blog.db')
        conn.execute("UPDATE content SET title = ?, content = ? WHERE entry_id = ?",
                     (title, content, entry_id))
        conn.commit()
        conn.close()

        # Check if a new image was uploaded
        if 'filefield' in request.files:
            image_file = request.files['filefield']
            if image_file:
                # Open the image using Pillow
                img = Image.open(image_file)

                # Compress the image (adjust the size as needed)
                img = img.convert('RGB')

                # Convert the compressed image to base64
                buffered = BytesIO()
                img.save(buffered, format="JPEG")
                compressed_image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')

                # Update the image data in the database
                conn = sqlite3.connect('blog.db')
                conn.execute("UPDATE content_images SET image_data = ? WHERE entry_id = ?",
                             (compressed_image_data, entry_id))
                conn.commit()
                conn.close()

        return redirect('/home')

    conn = sqlite3.connect('blog.db')
    cursor = conn.execute("SELECT * FROM content WHERE entry_id = ?", (entry_id,))
    cursor1 = conn.execute("SELECT * FROM content_images WHERE entry_id = ?", (entry_id,))
    image = cursor1.fetchone()
    entry = cursor.fetchone()
    conn.close()

    if entry and entry[1] == session['user_no']:
        return render_template('edit.html', entry=entry,image_data=image[2],username=username)
    else:
        return redirect('/home')



@app.route('/delete/<int:entry_id>')
def delete(entry_id):
    if 'username' not in session:
        return redirect('/')

    conn = sqlite3.connect('blog.db')

    # Delete the blog entry from the content table
    conn.execute("DELETE FROM content WHERE entry_id = ?", (entry_id,))

    # Delete the associated images from the content_images table
    conn.execute("DELETE FROM content_images WHERE entry_id = ?", (entry_id,))

    conn.commit()
    conn.close()

    return redirect('/home')


if __name__ == '__main__':
    # Connect to the database and create the 'users' table if not present
    conn = sqlite3.connect('blog.db')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_no INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT
    )
''')

    conn.execute('''CREATE TABLE IF NOT EXISTS content (
                    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_no INTEGER,
                    entry_date DATETIME,
                    title TEXT,
                    content TEXT,
                    FOREIGN KEY (user_no) REFERENCES users (user_no)
                )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS content_images (
                    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_id INTEGER,
                    image_data BLOB,
                    FOREIGN KEY (entry_id) REFERENCES content (entry_id)
                )''')
    conn.close()  # Close the database connection
    
    app.run(debug=True)
