from flask import Blueprint, render_template, request, flash, redirect, url_for
from .index_manager import IndexManager

bp = Blueprint('index_update', __name__, template_folder='templates/routes')

@bp.route('/update_index', methods=['GET', 'POST'])
def update_index():
    if request.method == 'POST':
        result = IndexManager.update_index()
        if result['success']:
            flash(f"インデックス更新成功！文書数: {result['document_count']}（所要時間: {result['time']:.2f}秒）", "success")
        else:
            flash(f"インデックス更新失敗: {result['error']}", "error")
        return redirect(url_for('index_update.update_index'))

    return render_template('index_update.html')
