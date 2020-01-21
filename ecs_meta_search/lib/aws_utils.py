import time
import datetime
import base64
import hmac
import hashlib
try:
    from urllib import quote_plus, quote
except:
    from urllib.parse import quote_plus, quote

S3_SIGNED_URL_FORMAT = '%(prot)s://%(bucket)s/%(endpoint)s/%(obj)s?AWSAccessKeyId=%(id)s&Expires=%(expires)d&Signature=%(sig)s'
ECS_SIGNED_URL_FORMAT = '%(prot)s://%(endpoint)s/%(bucket)s/%(obj)s?AWSAccessKeyId=%(id)s&Expires=%(expires)d&Signature=%(sig)s'

def get_signed_url(endpoint, bucket, obj, id, key, type='s3', expire=3600):
  """
  Get a signed URL  for an object
  
  Parameters:
    endpoint (string): Base URL to access the resource.
        e.g. https://object.ecstestdrive.com or https://s3.amazonaws.com
    bucket (string): Name of the bucket containing the object
    obj (string): ID for the object. e.g. Something/File.ext
    id (string): User ID credentials
    key (string): The secret key for the User ID crendentials
    type (string): Optional - Either 's3' (default) or 'ecs'. This determines 
        the URL style that will be returned.
        's3' style uses bucket.endpoint/object
        'ecs' style uses endpoint/bucket/object
    expire (int): Optional - Number of seconds from now that the URL will be
        valid. Default 3600 seconds. You can also pass in a datetime object.
        When this is done, the expiration time will be based on the datetime
        object only.
  
  Returns:
    Signed URL string value that can be used to access the object resource
  """
  # Parse out the http:// or https:// portion of the URL
  if endpoint[0:8] == 'https://':
    prot = 'https'
    endpoint = endpoint[8:]
  elif endpoint [0:7] == 'http://':
    prot = 'http'
    endpoint = endpoint[7:]
  if not (type == 's3' or type == 'ecs'):
    type = 's3'
  url_format = S3_SIGNED_URL_FORMAT
  if type == 'ecs':
    url_format = ECS_SIGNED_URL_FORMAT
  if isinstance(expire, datetime.datetime):
    expiry_ts = int(expire.strftime('%s'))
  else:
    expiry_ts = int(time.time()) + expire
  h = hmac.new(
      bytes(key.encode('utf-8')),
      ("GET\n\n\n%d\n/%s/%s"%(expiry_ts, bucket, obj)).encode('utf-8'),
      hashlib.sha1)
  # Signature
  sig = quote_plus(base64.encodestring(h.digest()).strip().decode('utf-8'))
  # S3 and ECS require different URL encoding for the object name
  # S3 uses the standard quote_plus while ECS allows for extra characters
  if type == 's3':
    obj = quote_plus(obj)
  else:
    obg = quote(obj, '/')
  # Create full signed URL
  signed_url = url_format%{
      'prot': prot,
      'endpoint': endpoint,
      'bucket': bucket,
      'obj': obj,
      'id': id,
      'key': key,
      'expires': expiry_ts,
      'sig': sig
  }
  return signed_url
