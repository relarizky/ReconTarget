import os
import tempfile

from app.model import *
from helper.general import *
from helper.reverse_ip import *

from .home import home_bp
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for, redirect, flash, send_file

@home_bp.route('/revip')
@login_required
def reverse_ip_index():
    page = request.args.get('page', 1, type = int)
    revip = Target.query.filter_by(id_user = current_user.id).paginate(page, 5, False)
    return render_template('home/revip/list_target.html', revips = revip)


@home_bp.route('/revip/scan/<int:id>', methods = ['POST'])
@login_required
def reverse_ip_scan(id):
    target = Target.query.get(id)
    tools = request.form.get('tools')

    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.reverse_ip_index'))
        if target.target_status_code == 'dead':
            flash('error', 'The site seems to be dead')
            return redirect(url_for('home.reverse_ip_index'))

        try:
            revip = ReverseIP(target.target_url)
            if tools == 'bing':
                revip = revip.bing()
            elif tools == 'you_get_signal':
                revip = revip.you_get_signal()
            elif tools == 'hacker_target':
                revip = revip.hacker_target()
            else:
                flash('error', 'Specify appropriate tool!')
                return secure_redirect(request.headers.get('referer'), url_for('home.reverse_ip_index'))
        except Exception as Error:
            flash('error', 'Fail to do reverse ip bcz, {}'.format(Error))
            return secure_redirect(request.headers.get('referer'), url_for('home.reverse_ip_index'))

        if len(revip) != 0:
            if target.revip.all() == []:
                tb_revip = RevIP(target, revip)
            else:
                tb_revip = RevIP.query.get(target.revip.first().id)
                old_list = target.revip.first().list_domain
                new_list = set(old_list + revip) # remove duplicate
                tb_revip.list_domain = list(new_list)
        else:
            flash('error', 'No other domain found in same server')
            return secure_redirect(request.headers.get('referer'), url_for('home.reverse_ip_index'))

        db.session.add(tb_revip)
        db.session.commit()
        flash('success', 'Found {} other sites in same server'.format(str(len(revip))))
        return secure_redirect(request.headers.get('referer'), url_for('home.reverse_ip_index'))
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.reverse_ip_index'))


@home_bp.route('/revip/download/<int:id>')
@login_required
def reverse_ip_download(id):
    tempfile.tempdir = os.getcwd()
    target = Target.query.get(id)

    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.reverse_ip_index'))

        if target.revip.first() == None:
            flash('error', 'You have not done any scan to this target')
            return redirect(url_for('home.reverse_ip_index'))

        with tempfile.TemporaryDirectory() as temp_dir:
            tempfile.tempdir = temp_dir
            file_name = 'revip_' + get_info(target.target_url, info = 'domain') + '.txt'
            file_object = tempfile.NamedTemporaryFile(mode = 'w+t')
            file_content = target.revip.first().list_domain

            try:
                file_object.writelines('\n'.join(file_content))
                file_object.seek(0)
                response = send_file(file_object.name,
                    mimetype = 'text/plain',
                    as_attachment = True,
                    attachment_filename = file_name)
                response.headers['Content-Length'] = os.path.getsize(file_object.name)
                response.headers['Cache-Control'] = 'no-cache'
            finally:
                file_object.close()

            return response
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.reverse_ip_index'))


@home_bp.route('/revip/view/<int:id>')
@login_required
def reverse_ip_view_raw(id):
    target = Target.query.get(id)

    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.reverse_ip_index'))
        elif target.revip.first() == None:
            flash('error', 'You have not done any scan to this target')
            return redirect(url_for('home.reverse_ip_index'))
        else:
            return '<br>'.join(target.revip.first().list_domain)
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.reverse_ip_index'))
