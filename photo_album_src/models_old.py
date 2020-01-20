#!/usr/bin/env python3

#########################################################
# This is the database processing file. (aka. Models)
# It contains the DB connections, queries and functions.
# Uses principles of Models, Views, Controllers (MVC).
#########################################################

# Import modules required for app
import os
import boto3
import json
from pymongo import MongoClient
from werkzeug import secure_filename
from PIL import Image
from config import ecs_test_drive

# Check if running in Pivotal Web Services with MongoDB service bound
if 'VCAP_SERVICES' in os.environ:
    VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
    MONGOCRED = VCAP_SERVICES["mlab"][0]["credentials"]
    client = MongoClient(MONGOCRED["uri"])
    DB_NAME = str(MONGOCRED["uri"].split("/")[-1])

# Otherwise, assume running locally with local MongoDB instance
else:
    client = MongoClient('172.18.0.2:27017')
    DB_NAME = "mongodb"  # Make sure this matches the name of your MongoDB database ######

# Get database connection with database name
db = client[DB_NAME]

# Remove any existing documents in photos collection
# db.photos.delete_many({})   # Comment this line if you don't want to remove documents each time you start the app

# Retrieve all photos records from database


def get_photos():
    return db.photos.find({})

# Insert form fields into database


def insert_photo(request):
    title = request.form['title']
    comments = request.form['comments']
    filename = secure_filename(request.files['photo'].filename)
    thumbfile = filename.rsplit(".", 1)[0] + "-thumb.jpg"
    photo_url = "http://" + ecs_test_drive['ecs_access_key_id'].split(
        '@')[0] + ".public.ecstestdrive.com/" + ecs_test_drive['ecs_bucket_name'] + "/" + filename
    thumbnail_url = "http://" + ecs_test_drive['ecs_access_key_id'].split(
        '@')[0] + ".public.ecstestdrive.com/" + ecs_test_drive['ecs_bucket_name'] + "/" + thumbfile

    db.photos.insert_one({'title': title, 'comments': comments,
                          'photo': photo_url, 'thumb': thumbnail_url})


def upload_photo(file):
    # Get ECS credentials from external config file
    ecs_endpoint_url = ecs_test_drive['ecs_endpoint_url']
    ecs_access_key_id = ecs_test_drive['ecs_access_key_id']
    ecs_secret_key = ecs_test_drive['ecs_secret_key']
    ecs_bucket_name = ecs_test_drive['ecs_bucket_name']

    # Open a session with ECS using the S3 API
    session = boto3.resource(service_name='s3', aws_access_key_id=ecs_access_key_id,
                             aws_secret_access_key=ecs_secret_key, endpoint_url=ecs_endpoint_url)

    # Remove unsupported characters from filename
    filename = secure_filename(file.filename)

    # First save the file locally
    file.save(os.path.join("uploads", filename))

    # Create a thumbnail
    size = 225, 225
    with open("uploads/" + filename, 'rb') as f:
        img = Image.open(f)
        img.thumbnail(size)
        thumbfile = filename.rsplit(".", 1)[0] + "-thumb.jpg"
        img.save("uploads/" + thumbfile, "JPEG")
        img.close()

    # Empty the variables to prevent memory leaks
    img = None

    # Upload the original image to ECS
    session.Object(ecs_bucket_name, filename).put(
        Body=open("uploads/" + filename, 'rb'), ACL='public-read')

    # Upload the thumbnail to ECS
    session.Object(ecs_bucket_name, thumbfile).put(
        Body=open("uploads/" + thumbfile, 'rb'), ACL='public-read')

    # Delete the local files
    os.remove("uploads/" + filename)
    os.remove("uploads/" + thumbfile)
