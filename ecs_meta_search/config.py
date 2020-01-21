#!/usr/bin/env python
# -*- coding: utf8 -*-
import os

class Config(object):
  DEBUG = os.environ.get('ECS_META_SEARCH_DEBUG') or False
  SECRET_KEY = os.environ.get('ECS_META_SEARCH_SECRET_KEY') or 'ecs_meta_search_secrets'
  SESSION_COOKIE_NAME = 'ecs_meta_search'
  HIDE_PASSWORD = os.environ.get('ECS_META_SEARCH_HIDE_PASSWORD') or False
  # User defined values below
  ACCESS_ID = os.environ.get('ECS_META_SEARCH_ACCESS_ID') or None
  ACCESS_KEY = os.environ.get('ECS_META_SEARCH_ACCESS_KEY') or None
  TOKEN = os.environ.get('ECS_META_SEARCH_TOKEN') or None
  ENDPOINT = os.environ.get('ECS_META_SEARCH_ENDPOINT') or None
  BUCKET = os.environ.get('ECS_META_SEARCH_BUCKET') or None
  URL_TYPE = 'ecs'
  URL_EXPIRATION = 3600
  LISTEN_IP = os.environ.get('ECS_META_SEARCH_LISTEN_IP') or '0.0.0.0'
  LISTEN_PORT = os.environ.get('ECS_META_SEARCH_LISTEN_PORT') or 5000
  