from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Code, ScanLog

scan_bp = Blueprint('scan', __name__, url_prefix='/scan')

@scan_bp.route('/')
@login_required
def scanner():
    return render_template('scanner.html')

@scan_bp.route('', methods=['POST'])
@login_required
def scan_api():
    code_str = request.json['code']
    code_record = Code.query.filter_by(code=code_str).first()
    if not code_record:
        return jsonify({'error': '无效二维码'}), 404
    if code_record.scanned:
        return jsonify({'error': '该二维码已使用'})
    code_record.scanned = True
    log = ScanLog(code_id=code_record.id, checker_id=current_user.id)
    db.session.add(log)
    db.session.commit()
    return jsonify({
        'success': True,
        'name': code_record.name,
        'note': code_record.note
    })
