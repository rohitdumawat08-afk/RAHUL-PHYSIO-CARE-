# app.py
import os
import uuid
from datetime import datetime
from functools import wraps
from flask import (
    Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
)
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'rahul-physio-jaipur-secret-key-2026-secure')

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif', 'svg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Authentication Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized. Please log in.'}), 401
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ----------------- PUBLIC ROUTES ----------------- #

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/therapies', methods=['GET'])
def get_public_therapies():
    category = request.args.get('category', '').strip()
    search = request.args.get('search', '').strip()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM therapies WHERE status = 'active'"
    params = []
    
    if category and category.lower() != 'all':
        query += " AND category = ?"
        params.append(category)
        
    if search:
        query += " AND (name LIKE ? OR short_desc LIKE ? OR full_desc LIKE ? OR indications LIKE ?)"
        search_pattern = f"%{search}%"
        params.extend([search_pattern, search_pattern, search_pattern, search_pattern])
        
    query += " ORDER BY id ASC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    therapies = []
    for r in rows:
        therapies.append({
            'id': r['id'],
            'name': r['name'],
            'category': r['category'],
            'image_url': r['image_url'] or '/static/images/default-physio.jpg',
            'short_desc': r['short_desc'],
            'full_desc': r['full_desc'],
            'price': r['price'],
            'duration': r['duration'] or '45-60 Mins',
            'status': r['status'],
            'indications': r['indications'] or ''
        })
        
    conn.close()
    return jsonify({'therapies': therapies, 'count': len(therapies)})

@app.route('/api/therapies/<int:therapy_id>', methods=['GET'])
def get_public_therapy_detail(therapy_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM therapies WHERE id = ? AND status = 'active'", (therapy_id,))
    r = cursor.fetchone()
    conn.close()
    
    if not r:
        return jsonify({'error': 'Therapy not found or inactive'}), 404
        
    return jsonify({
        'id': r['id'],
        'name': r['name'],
        'category': r['category'],
        'image_url': r['image_url'] or '/static/images/default-physio.jpg',
        'short_desc': r['short_desc'],
        'full_desc': r['full_desc'],
        'price': r['price'],
        'duration': r['duration'] or '45-60 Mins',
        'status': r['status'],
        'indications': r['indications'] or ''
    })

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json() or {}
    
    patient_name = data.get('patient_name', '').strip()
    phone = data.get('phone', '').strip()
    area = data.get('area', '').strip()
    preferred_date = data.get('preferred_date', '').strip()
    preferred_time = data.get('preferred_time', '').strip()
    service_name = data.get('service_name', '').strip()
    message = data.get('message', '').strip()
    
    if not (patient_name and phone and area and preferred_date and preferred_time and service_name):
        return jsonify({'error': 'Please fill all required booking fields.'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookings (patient_name, phone, area, preferred_date, preferred_time, service_name, message, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
    """, (patient_name, phone, area, preferred_date, preferred_time, service_name, message))
    
    booking_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': 'Your home-visit appointment request has been submitted successfully! We will contact you shortly to confirm.',
        'booking_id': booking_id,
        'phone': '7023029646'
    }), 201

@app.route('/api/check-area', methods=['POST'])
def check_area():
    data = request.get_json() or {}
    user_area = data.get('area', '').strip().lower()
    
    service_areas = [
        "sitapura", "india gate", "kumbha marg", "haldi ghati",
        "pratap nagar", "sanganer", "durgapura", "gopalpura",
        "gurjar ki thadi", "shyam nagar", "vivek vihar", "vaishali nagar"
    ]
    
    if not user_area:
        return jsonify({'error': 'Please enter an area or locality name'}), 400
        
    matched = None
    for area in service_areas:
        if area in user_area or user_area in area:
            matched = area.title()
            break
            
    if matched:
        return jsonify({
            'available': True,
            'area': matched,
            'message': f"Home visits are fully active in {matched} & surrounding neighborhoods! Morning and night slots are available.",
            'phone': '7023029646'
        })
    else:
        return jsonify({
            'available': True,
            'area': user_area.title(),
            'message': f"We regularly provide home visits across Jaipur. Please call or WhatsApp 7023029646 to check specific travel availability for {user_area.title()}.",
            'phone': '7023029646'
        })

# ----------------- ADMIN AUTH ----------------- #

@app.route('/admin/login', methods=['GET'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/api/admin/login', methods=['POST'])
def api_admin_login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admin_users WHERE username = ?', (username,))
    admin = cursor.fetchone()
    conn.close()
    
    if admin and check_password_hash(admin['password_hash'], password):
        session['admin_logged_in'] = True
        session['admin_user'] = username
        return jsonify({'success': True, 'message': 'Login successful'})
        
    return jsonify({'error': 'Invalid username or password.'}), 401

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/api/admin/logout', methods=['POST'])
def api_admin_logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/admin/check-auth', methods=['GET'])
def api_check_auth():
    is_logged_in = bool(session.get('admin_logged_in'))
    username = session.get('admin_user', '')
    return jsonify({'authenticated': is_logged_in, 'user': username})

# ----------------- ADMIN DASHBOARD & CRUD ----------------- #

@app.route('/admin')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html', username=session.get('admin_user', 'Admin'))

@app.route('/api/admin/stats', methods=['GET'])
@login_required
def get_admin_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM therapies')
    total_therapies = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM therapies WHERE status = 'active'")
    active_therapies = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM therapies WHERE status != 'active'")
    inactive_therapies = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM bookings')
    total_bookings = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM bookings WHERE status = 'pending'")
    pending_bookings = cursor.fetchone()['count']
    
    conn.close()
    return jsonify({
        'total_therapies': total_therapies,
        'active_therapies': active_therapies,
        'inactive_therapies': inactive_therapies,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings
    })

@app.route('/api/admin/therapies', methods=['GET'])
@login_required
def get_admin_therapies():
    category = request.args.get('category', '').strip()
    search = request.args.get('search', '').strip()
    status = request.args.get('status', '').strip()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM therapies WHERE 1=1"
    params = []
    
    if category and category.lower() != 'all':
        query += " AND category = ?"
        params.append(category)
        
    if status and status.lower() != 'all':
        query += " AND status = ?"
        params.append(status)
        
    if search:
        query += " AND (name LIKE ? OR short_desc LIKE ? OR full_desc LIKE ? OR indications LIKE ?)"
        search_pattern = f"%{search}%"
        params.extend([search_pattern, search_pattern, search_pattern, search_pattern])
        
    query += " ORDER BY id DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    therapies = [dict(r) for r in rows]
    conn.close()
    return jsonify({'therapies': therapies, 'count': len(therapies)})

@app.route('/api/admin/therapies', methods=['POST'])
@login_required
def add_therapy():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    category = data.get('category', '').strip()
    image_url = data.get('image_url', '').strip() or 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80'
    short_desc = data.get('short_desc', '').strip()
    full_desc = data.get('full_desc', '').strip()
    price = data.get('price', '').strip()
    duration = data.get('duration', '').strip() or '45-60 Mins'
    status = data.get('status', 'active').strip()
    indications = data.get('indications', '').strip()
    
    if not name or not category or not short_desc or not full_desc:
        return jsonify({'error': 'Name, Category, Short Description, and Full Description are required.'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO therapies (name, category, image_url, short_desc, full_desc, price, duration, status, indications, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (name, category, image_url, short_desc, full_desc, price, duration, status, indications))
    
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Therapy added successfully!', 'id': new_id}), 201

@app.route('/api/admin/therapies/<int:therapy_id>', methods=['GET'])
@login_required
def get_single_therapy(therapy_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM therapies WHERE id = ?", (therapy_id,))
    r = cursor.fetchone()
    conn.close()
    
    if not r:
        return jsonify({'error': 'Therapy not found'}), 404
        
    return jsonify(dict(r))

@app.route('/api/admin/therapies/<int:therapy_id>', methods=['PUT'])
@login_required
def update_therapy(therapy_id):
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    category = data.get('category', '').strip()
    image_url = data.get('image_url', '').strip()
    short_desc = data.get('short_desc', '').strip()
    full_desc = data.get('full_desc', '').strip()
    price = data.get('price', '').strip()
    duration = data.get('duration', '').strip() or '45-60 Mins'
    status = data.get('status', 'active').strip()
    indications = data.get('indications', '').strip()
    
    if not name or not category or not short_desc or not full_desc:
        return jsonify({'error': 'Name, Category, Short Description, and Full Description are required.'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE therapies
        SET name = ?, category = ?, image_url = ?, short_desc = ?, full_desc = ?, price = ?, duration = ?, status = ?, indications = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (name, category, image_url, short_desc, full_desc, price, duration, status, indications, therapy_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Therapy updated successfully!'})

@app.route('/api/admin/therapies/<int:therapy_id>', methods=['DELETE'])
@login_required
def delete_therapy(therapy_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM therapies WHERE id = ?", (therapy_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Therapy deleted successfully!'})

@app.route('/api/admin/therapies/<int:therapy_id>/toggle-status', methods=['POST'])
@login_required
def toggle_therapy_status(therapy_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM therapies WHERE id = ?", (therapy_id,))
    r = cursor.fetchone()
    if not r:
        conn.close()
        return jsonify({'error': 'Therapy not found'}), 404
        
    new_status = 'inactive' if r['status'] == 'active' else 'active'
    cursor.execute("UPDATE therapies SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (new_status, therapy_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'new_status': new_status, 'message': f'Status changed to {new_status}'})

@app.route('/api/admin/bookings', methods=['GET'])
@login_required
def get_admin_bookings():
    status = request.args.get('status', '').strip()
    search = request.args.get('search', '').strip()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM bookings WHERE 1=1"
    params = []
    
    if status and status.lower() != 'all':
        query += " AND status = ?"
        params.append(status)
        
    if search:
        query += " AND (patient_name LIKE ? OR phone LIKE ? OR area LIKE ? OR service_name LIKE ?)"
        s = f"%{search}%"
        params.extend([s, s, s, s])
        
    query += " ORDER BY id DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    bookings = [dict(r) for r in rows]
    conn.close()
    return jsonify({'bookings': bookings, 'count': len(bookings)})

@app.route('/api/admin/bookings/<int:booking_id>/status', methods=['POST'])
@login_required
def update_booking_status(booking_id):
    data = request.get_json() or {}
    new_status = data.get('status', '').strip()
    
    if new_status not in ['pending', 'confirmed', 'completed', 'cancelled']:
        return jsonify({'error': 'Invalid status'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", (new_status, booking_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': f'Booking marked as {new_status}'})

@app.route('/api/admin/bookings/<int:booking_id>', methods=['DELETE'])
@login_required
def delete_booking(booking_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Booking deleted successfully'})

@app.route('/api/admin/upload-image', methods=['POST'])
@login_required
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_name = f"therapy_{uuid.uuid4().hex[:10]}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        file.save(filepath)
        url = f"/static/uploads/{unique_name}"
        return jsonify({'success': True, 'url': url, 'message': 'Image uploaded successfully'})
        
    return jsonify({'error': 'Invalid file format. Allowed: JPG, PNG, WEBP, GIF, SVG'}), 400

@app.route('/api/admin/change-password', methods=['POST'])
@login_required
def change_admin_password():
    data = request.get_json() or {}
    old_pwd = data.get('old_password', '').strip()
    new_pwd = data.get('new_password', '').strip()
    username = session.get('admin_user')
    
    if not old_pwd or not new_pwd:
        return jsonify({'error': 'Old and new passwords are required'}), 400
        
    if len(new_pwd) < 6:
        return jsonify({'error': 'New password must be at least 6 characters'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admin_users WHERE username = ?', (username,))
    admin = cursor.fetchone()
    
    if not admin or not check_password_hash(admin['password_hash'], old_pwd):
        conn.close()
        return jsonify({'error': 'Incorrect current password'}), 400
        
    hashed = generate_password_hash(new_pwd)
    cursor.execute('UPDATE admin_users SET password_hash = ? WHERE username = ?', (hashed, username))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Password updated successfully'})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Rahul Physio Web Server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
