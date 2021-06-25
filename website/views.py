from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import Note, User
from . import db
import json
import random

views = Blueprint('views', __name__)
placeholder_sentence = ["Today I though about...", "It's important that...", "I want to remember...", "I think about...", "Today happened...", "WOW! Note this..."]

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('Note is too short.', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    
    return render_template("home.html", user=current_user, plcs=random.choice(placeholder_sentence))

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=current_user.email).first()
        
        if user:
            flash("User already exists!", category="error")
        elif user.email != email:
            if len(email) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            else:
                user.email = email
                db.session.commit()
        elif user.first_name != first_name:
            if len(first_name) < 2:
                flash('First name must be greater than 1 character.', category='error')
            else:
                user.first_name = first_name
                db.session.commit()
        elif check_password_hash(user.password, password1):
            if password1 == password2:
                user.password = password1
                db.session.commit()
            else:
                flash("The passwords do not match!", category="error")
    return render_template("edit.html", user=current_user)