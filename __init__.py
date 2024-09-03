from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from flask_login import login_required, current_user

from utils import *
from services.manager import *
from services.teacher import *