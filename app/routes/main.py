from flask import Blueprint, render_template, request, Response, redirect, url_for, send_from_directory, current_app
import os
from ..chat_db import add_chat, get_chat, get_all_chats
from ..utils.llama_service import generate_title, generate_summary
from werkzeug.utils import secure_filename

main_bp = Blueprint('main', __name__)

# AUTH ROUTES
@main_bp.route('/auth/register')
def register():
    return render_template('register.html')

@main_bp.route('/auth/login')
def login():
    return render_template('login.html')

@main_bp.route('/auth/logout')
def logout():
    return redirect(url_for('dashboard'))


# CHAT ROUTES
@main_bp.route('/')
def root():
    return redirect(url_for('main.home'))

@main_bp.route('/c/new')
def home():
    chats = get_all_chats()
    return render_template('home.html', chats=chats)


@main_bp.route('/c/<cid>')
def chatBox(cid):
    chats = get_all_chats()
    chat = get_chat(cid)
    if chat:
        return render_template(
            'chat.html',
            cid=cid,
            title=chat[1],
            image=chat[2],
            message=chat[3],
            chats=chats,
            is_streamed=chat[4]
        )
    return redirect(url_for('main.home'))


@main_bp.route('/mark_streamed/<chat_id>')
def mark_streamed(chat_id):
    from ..chat_db import update_chat_response, get_chat
    chat = get_chat(chat_id)
    if chat:
        update_chat_response(chat_id, chat[3], is_streamed=True)
        return 'OK'
    return 'Not found', 404


@main_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    upload_folder = os.path.join(current_app.root_path, '..', 'uploads')
    return send_from_directory(upload_folder, filename)


# TESTING ROUTES
@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@main_bp.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No file uploaded", 400

    file = request.files['image']
    filename = secure_filename(file.filename)
    upload_folder = os.path.join(current_app.root_path, '..', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    # Generate title and summary using LLaMA
    chat_title = generate_title(filepath)
    response_txt = generate_summary(filepath)
    # chat_title = "Coastal Urban-Industrial Zone"
    # response_txt = "This satellite image reveals a diverse urban and natural landscape segmented across distinct regions. In the Top Left, industrial infrastructure and a section of agricultural land are visible, bordering a coastal edge. The Top Right is densely packed with urban development, showcasing a tightly knit grid of buildings and roads indicative of a residential or mixed-use area. Moving to the Center, a major road or highway cuts vertically through the image, flanked by large white-roofed structures—possibly warehouses or commercial facilities—highlighting a transitional zone between urban and industrial usage. In the Bottom Left, a body of water curves inward, forming a small bay or inlet adjacent to more industrial land use, reinforcing the idea of a port or service area. The Bottom Right features a darker patch suggestive of a vegetated or forested zone, providing contrast to the surrounding urban sprawl and hinting at a park or preserved area. General Observations indicate a well-defined urban-industrial gradient from inland to the coast, with transportation infrastructure playing a central role in organizing land use and activity patterns."

    # Save to DB
    chat_id = add_chat(chat_title, filename, response_txt)

    return redirect(url_for('main.chatBox', cid=chat_id))

