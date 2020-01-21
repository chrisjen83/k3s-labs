#!/usr/bin/env python3

# Import modules required for app
import os
from flask import Flask, render_template, request
from models import get_photos, insert_photo, upload_photo
from werkzeug import secure_filename
import time

HOSTNAME = os.environ.get("HOSTNAME", "")

# Create a Flask instance
app = Flask(__name__)

##### Define routes #####
@app.route('/')
def home():
    album_photos = get_photos()							                        # Call function in 'models.py' to retrieve all photo's from database
    return render_template('default.html', album_photos=album_photos, url="home")

# This route accepts GET and POST calls
@app.route('/upload', methods=['POST'])
def upload():
    filename = secure_filename(request.files['photo'].filename)
    uuid = "%s-%s-"%(time.time(), HOSTNAME)
    filename = uuid + filename

    insert_photo(request, filename)								                        # Call function in 'models.py' to process the database transaction
    upload_photo(request.files['photo'], filename)				                        # Call function in 'models.py' to upload photo to ECS
                                                                                # Return a page to inform the user of a successful upload
    return render_template('submit-photo.html')


@app.route('/photo/<path:photo>')
def photo(photo):
    return render_template('photo.html', photo=photo)


##### Run the Flask instance, browse to http://<< Host IP or URL >>:5000 #####
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', '5000')), threaded=True)
