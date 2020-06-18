import os
import tempfile

from app.model import *
from helper.whois import *
from helper.general import *

from .home import home_bp
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for, redirect, flash, send_file

@home_bp.route('/whois')
@login_required
def whois_index():
    page = request.args.get('page', 1, type = int)
    target = Target.query.filter_by(id_user = current_user.id).paginate(page, 5, False)
    return render_template('home/whois/list_target.html', targets = target)


@home_bp.route('/whois/scan/<int:id>', methods = ['GET', 'POST'])
@login_required
def whois_scan(id):
    target = Target.query.get(id)
    reference = request.form.get('tools')

    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.whois_index'))
        if target.target_status_code == 'dead':
            flash('error', 'This site seems to be dead')
            return redirect(url_for('home.whois_index'))

        try:
            if reference == 'whois.com':
                whois_result = whois_from_whois_com(target.target_url)
            elif reference == 'hackertarget':
                whois_result = whois_from_hacker_target(target.target_url)
            else:
                flash('error', 'Specify appropriate reference!')
                return secure_redirect(request.headers.get('referer'), url_for('home.whois_index'))
        except Exception as Error:
            flash('error', 'Fail to scan whois bcz, {}'.format(Error))
            return secure_redirect(request.headers.get('referer'), url_for('home.whois_index'))

        if whois_result != None:
            if target.whois.first() == None:
                whois = Whois(target, True, whois_result)
            else:
                whois = Whois.query.get(target.whois.first().id)
                whois.whois_result = whois_result
            db.session.add(whois)
            db.session.commit()
        else:
            flash('error', 'No whois result found for {}'.format(get_info(target.target_url, info = 'domain')))
            return secure_redirect(request.headers.get('referer'), url_for('home.whois_index'))

        flash('success', 'Successfully scan {}'.format(get_info(target.target_url, info = 'domain')))
        return secure_redirect(request.headers.get('referer'), url_for('home.whois_index'))
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.whois_index'))


@home_bp.route('/whois/download/<int:id>')
@login_required
def whois_download(id):
    tempfile.tempdir = os.getcwd()
    target = Target.query.get(id)

    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.whois_index'))

        if target.whois.first() == None:
            flash('error', 'You have not done any scan to this target')
            return redirect(url_for('home.whois_index'))

        with tempfile.TemporaryDirectory() as temp_dir:
            tempfile.tempdir = temp_dir
            file_name = 'whois_' + get_info(target.target_url, info = 'domain') + '.txt'
            file_object = tempfile.NamedTemporaryFile(mode = 'w+t')
            file_content = target.whois.first().whois_result

            try:
                file_object.writelines(file_content)
                file_object.seek(0)
                response = send_file(file_object.name,
                    mimetype='text/plain',
                    as_attachment=True,
                    attachment_filename=file_name)
                response.headers['Content-Length'] = os.path.getsize(file_object.name)
                response.headers['Cache-Control'] = 'no-cache'
            finally:
                file_object.close()

            return response
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.whois_index'))


@home_bp.route('/whois/view/<int:id>')
@login_required
def whois_view_raw(id):
    target = Target.query.get(id)

    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.whois_index'))
        elif target.whois.first() == None:
            flash('error', 'You have not done any scan to this target')
            return redirect(url_for('home.whois_index'))
        else:
            return target.whois.first().whois_result.replace('\n', '<br>')
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.whois_index'))
