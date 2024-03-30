from flask import Blueprint, render_template, request

from app import Policy, db

import json

policieslist_bp = Blueprint("policieslist", __name__)

# ********* All "policieslist" URLS ***********
# Defines View part of web application
