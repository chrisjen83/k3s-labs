#!/usr/bin/env python3
# Import modules required for app
import os
import boto3
import json
from pymongo import MongoClient
from PIL import Image

# Get from K8s ConfigMap values for MongoDB Database
MONGO_SERVER = os.environ.get("MONGO_SERVER", None)
DB_NAME = os.environ.get("DB_NAME", None)
client = MongoClient(MONGO_SERVER, 27017)

# Get from K8s ConfigMap values for S3 connector
ecs_endpoint_url = os.environ.get("ecs_endpoint_url", None)
ecs_access_key_id = os.environ.get("ecs_access_key_id", None)
ecs_secret_key = os.environ.get("ecs_secret_key", None)
ecs_bucket_name = os.environ.get("ecs_bucket_name", None)

# Get database connection with database name
db = client[DB_NAME]

# Remove any existing documents in photos collection
# db.photos.delete_many({})
# Comment this line if you don't want to remove documents each time you start the app

# Retrieve all photos records from database


def get_photos():
    return db.photos.find({})

# Insert form fields into database


def insert_photo(request, filename):
    title = request.form['title']
    comments = request.form['comments']
    filename_ext = filename.rsplit(".", 1)[1]
    thumbfile = filename.rsplit(".", 1)[0] + "-thumb.%s"%filename_ext
    photo_url = "http://" + ecs_access_key_id.split(
        '@')[0] + ".public.ecstestdrive.com/" + ecs_bucket_name + "/" + filename
    thumbnail_url = "http://" + ecs_access_key_id.split(
        '@')[0] + ".public.ecstestdrive.com/" + ecs_bucket_name + "/" + thumbfile

    db.photos.insert_one({'title': title, 'comments': comments,
                          'photo': photo_url, 'thumb': thumbnail_url})


def upload_photo(file, filename, contenttype):
    # Open a session with ECS using the S3 API
    session = boto3.resource(service_name='s3', aws_access_key_id=ecs_access_key_id,
                             aws_secret_access_key=ecs_secret_key, endpoint_url=ecs_endpoint_url)

    # First save the file locally
    file.save(os.path.join("uploads", filename))

    # Create a thumbnail
    size = 225, 225
    with open("uploads/" + filename, 'rb') as f:
        img = Image.open(f)
        img.thumbnail(size)
        filename_ext = filename.rsplit(".", 1)[1]
        thumbfile = filename.rsplit(".", 1)[0] + "-thumb.%s"%filename_ext
        img.save("uploads/" + thumbfile)
        img.close()

    # Empty the variables to prevent memory leaks
    img = None

    # Upload the original image to ECS
    session.Object(ecs_bucket_name, filename).put(
        Body=open("uploads/" + filename, 'rb'), ACL='public-read', ContentType = contenttype)

    # Upload the thumbnail to ECS
    session.Object(ecs_bucket_name, thumbfile).put(
        Body=open("uploads/" + thumbfile, 'rb'), ACL='public-read')

    # Delete the local files
    os.remove("uploads/" + filename)
    os.remove("uploads/" + thumbfile)
