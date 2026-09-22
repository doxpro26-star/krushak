import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), 'instance'), exist_ok=True)

# CORS for Vercel frontend -> Render backend
CORS(app, supports_credentials=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'farmer_login'

# ---------------- Models ----------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='farmer')  # farmer / admin
    mobile = db.Column(db.String(20))
    village = db.Column(db.String(100))
    district = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reports = db.relationship('DamageReport', backref='farmer', lazy=True)

    def set_password(self, p): self.password_hash = generate_password_hash(p)
    def check_password(self, p): return check_password_hash(self.password_hash, p)

class DamageReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    farmer_name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    village = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), default='Maharashtra')
    survey_no = db.Column(db.String(50))
    crop_type = db.Column(db.String(50), nullable=False)
    farm_size = db.Column(db.String(20), nullable=False)  # in acre
    damage_type = db.Column(db.String(50), nullable=False)  # monsoon, pollution, flood, drought, pest, hailstorm
    severity = db.Column(db.String(20), nullable=False) # low, medium, high, severe
    damage_date = db.Column(db.String(20), nullable=False)
    area_affected = db.Column(db.String(20))
    estimated_loss = db.Column(db.String(20))
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(200))
    status = db.Column(db.String(30), default='Pending') # Pending, Verified, Approved, Rejected, Compensation Initiated
    admin_remark = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ---------------- Helpers ----------------
def get_stats():
    total = DamageReport.query.count()
    pending = DamageReport.query.filter_by(status='Pending').count()
    verified = DamageReport.query.filter_by(status='Verified').count()
    approved = DamageReport.query.filter_by(status='Approved').count()
    rejected = DamageReport.query.filter_by(status='Rejected').count()
    compensated = DamageReport.query.filter_by(status='Compensation Initiated').count()
    # damage type breakdown
    types = ['Heavy Monsoon', 'Flood', 'Drought', 'Pollution', 'Pest Attack', 'Hailstorm', 'Other']
    type_counts = {t: DamageReport.query.filter_by(damage_type=t).count() for t in types}
    return dict(total=total, pending=pending, verified=verified, approved=approved, rejected=rejected, compensated=compensated, type_counts=type_counts)

# ---------------- Routes - Public ----------------
@app.route('/')
def index():
    stats = get_stats()
    recent = DamageReport.query.order_by(DamageReport.created_at.desc()).limit(3).all()
    return render_template('index.html', stats=stats, recent=recent)

@app.route('/about')
def about():
    return render_template('about.html')

# ---------------- Farmer Auth ----------------
@app.route('/farmer/register', methods=['GET','POST'])
def farmer_register():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        email = request.form.get('email','').strip()
        mobile = request.form.get('mobile','').strip()
        village = request.form.get('village','').strip()
        district = request.form.get('district','').strip()
        password = request.form.get('password','')
        if not username or not email or not password:
            flash('Please fill all required fields.', 'danger')
            return redirect(url_for('farmer_register'))
        if User.query.filter((User.username==username)|(User.email==email)).first():
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('farmer_register'))
        u = User(username=username, email=email, mobile=mobile, village=village, district=district, role='farmer')
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('farmer_login'))
    return render_template('farmer/register.html')

@app.route('/farmer/login', methods=['GET','POST'])
def farmer_login():
    if request.method == 'POST':
        ident = request.form.get('username','').strip()
        password = request.form.get('password','')
        user = User.query.filter((User.username==ident)|(User.email==ident)).first()
        if user and user.check_password(password) and user.role=='farmer':
            login_user(user)
            return redirect(url_for('farmer_dashboard'))
        flash('Invalid credentials or not a farmer account.', 'danger')
    return render_template('farmer/login.html')

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        ident = request.form.get('username','').strip()
        password = request.form.get('password','')
        user = User.query.filter((User.username==ident)|(User.email==ident)).first()
        if user and user.check_password(password) and user.role=='admin':
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin credentials.', 'danger')
    return render_template('admin/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

# ---------------- Farmer Dashboard ----------------
@app.route('/farmer/dashboard')
@login_required
def farmer_dashboard():
    if current_user.role != 'farmer':
        return redirect(url_for('admin_dashboard'))
    reports = DamageReport.query.filter_by(farmer_id=current_user.id).order_by(DamageReport.created_at.desc()).all()
    stats = {
        'total': len(reports),
        'pending': len([r for r in reports if r.status=='Pending']),
        'approved': len([r for r in reports if r.status=='Approved']),
    }
    return render_template('farmer/dashboard.html', reports=reports, stats=stats)

@app.route('/farmer/report/new', methods=['GET','POST'])
@login_required
def farmer_report_new():
    if current_user.role != 'farmer':
        flash('Only farmers can submit reports.', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        try:
            farmer_name = request.form.get('farmer_name') or current_user.username
            mobile = request.form.get('mobile') or current_user.mobile or ''
            village = request.form.get('village') or current_user.village or ''
            district = request.form.get('district') or current_user.district or ''
            photo_file = request.files.get('photo')
            filename = None
            if photo_file and photo_file.filename != '':
                if allowed_file(photo_file.filename):
                    filename = datetime.now().strftime('%Y%m%d%H%M%S_') + secure_filename(photo_file.filename)
                    photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                else:
                    flash('Only png/jpg/jpeg/webp allowed.', 'warning')

            report = DamageReport(
                farmer_id=current_user.id,
                farmer_name=farmer_name,
                mobile=mobile,
                village=village,
                district=district,
                state=request.form.get('state','Maharashtra'),
                survey_no=request.form.get('survey_no',''),
                crop_type=request.form.get('crop_type'),
                farm_size=request.form.get('farm_size'),
                damage_type=request.form.get('damage_type'),
                severity=request.form.get('severity'),
                damage_date=request.form.get('damage_date'),
                area_affected=request.form.get('area_affected',''),
                estimated_loss=request.form.get('estimated_loss',''),
                description=request.form.get('description'),
                photo=filename,
                status='Pending'
            )
            db.session.add(report)
            db.session.commit()
            flash('Damage report submitted successfully! Reference ID: #'+str(report.id), 'success')
            return redirect(url_for('farmer_dashboard'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    return render_template('farmer/report.html')

@app.route('/farmer/report/<int:report_id>')
@login_required
def farmer_report_detail(report_id):
    report = DamageReport.query.get_or_404(report_id)
    if report.farmer_id != current_user.id and current_user.role != 'admin':
        abort(403)
    return render_template('farmer/report_detail.html', report=report)

# ---------------- Admin ----------------
@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    stats = get_stats()
    # recent pending
    pending_reports = DamageReport.query.filter_by(status='Pending').order_by(DamageReport.created_at.desc()).limit(5).all()
    # districts top
    from sqlalchemy import func
    district_data = db.session.query(DamageReport.district, func.count(DamageReport.id)).group_by(DamageReport.district).all()
    # severity
    severity_counts = {
        'Low': DamageReport.query.filter_by(severity='Low').count(),
        'Medium': DamageReport.query.filter_by(severity='Medium').count(),
        'High': DamageReport.query.filter_by(severity='High').count(),
        'Severe': DamageReport.query.filter_by(severity='Severe').count(),
    }
    return render_template('admin/dashboard.html', stats=stats, pending_reports=pending_reports, district_data=district_data, severity_counts=severity_counts)

@app.route('/admin/reports')
@login_required
@admin_required
def admin_reports():
    status_filter = request.args.get('status','')
    damage_filter = request.args.get('damage_type','')
    search = request.args.get('q','').strip()
    query = DamageReport.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if damage_filter:
        query = query.filter_by(damage_type=damage_filter)
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                DamageReport.farmer_name.ilike(like),
                DamageReport.village.ilike(like),
                DamageReport.district.ilike(like),
                DamageReport.crop_type.ilike(like),
            )
        )
    reports = query.order_by(DamageReport.created_at.desc()).all()
    return render_template('admin/reports.html', reports=reports, status_filter=status_filter, damage_filter=damage_filter, search=search)

@app.route('/admin/report/<int:report_id>', methods=['GET','POST'])
@login_required
@admin_required
def admin_report_detail(report_id):
    report = DamageReport.query.get_or_404(report_id)
    if request.method == 'POST':
        new_status = request.form.get('status')
        remark = request.form.get('admin_remark','').strip()
        if new_status in ['Pending','Verified','Approved','Rejected','Compensation Initiated']:
            report.status = new_status
            report.admin_remark = remark
            db.session.commit()
            flash(f'Report #{report.id} updated to {new_status}', 'success')
            return redirect(url_for('admin_reports'))
        flash('Invalid status.', 'danger')
    return render_template('admin/report_detail.html', report=report)

@app.route('/admin/report/<int:report_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_report_delete(report_id):
    report = DamageReport.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash('Report deleted.', 'info')
    return redirect(url_for('admin_reports'))

# ---------------- API for stats (for charts) ----------------
@app.route('/api/stats')
def api_stats():
    return jsonify(get_stats())

# ---------------- Error handlers ----------------
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

# ---------------- CLI / Init ----------------
@app.cli.command('init-db')
def init_db():
    db.create_all()
    # create default admin if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@krushak.gov.in', role='admin', village='HQ', district='Pune')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Default admin created: admin / admin123')

with app.app_context():
    db.create_all()
    # seed admin
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@krushak.gov.in', role='admin', village='HQ', district='Pune', mobile='9999999999')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Seeded admin: admin / admin123')
    # seed demo farmer if empty
    if not User.query.filter_by(username='ramesh').first():
        demo = User(username='ramesh', email='ramesh@farmer.com', role='farmer', mobile='9876543210', village='Shirur', district='Pune')
        demo.set_password('farmer123')
        db.session.add(demo)
        db.session.commit()
        # sample report
        if DamageReport.query.count()==0:
            sample = DamageReport(
                farmer_id=demo.id, farmer_name='Ramesh Patil', mobile='9876543210',
                village='Shirur', district='Pune', state='Maharashtra', survey_no='123/A',
                crop_type='Soybean', farm_size='2.5', damage_type='Heavy Monsoon',
                severity='High', damage_date='2026-08-15', area_affected='1.8 acre',
                estimated_loss='45000', description='Heavy monsoon destroyed soybean crop. Waterlogging for 5 days. Leaves yellowed and roots damaged due to excess water and chemical runoff from nearby factory.',
                status='Pending'
            )
            db.session.add(sample)
            db.session.commit()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
