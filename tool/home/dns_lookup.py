import os
import tempfile

from app.model import *
from helper.general import *
from helper.dns_lookup import *

from .home import home_bp
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for, redirect, flash, send_file

@home_bp.route('/dnslookup')
@login_required
def dns_lookup_index():
    page = request.args.get('page', 1, type = int)
    dnslookup = Target.query.filter_by(id_user = current_user.id).paginate(page, 5, False)
    return render_template('home/dnslookup/list_target.html', dnslookups = dnslookup)


@home_bp.route('/dnslookup/scan/<int:id>')
@login_required
def dns_lookup_scan(id):
    target = Target.query.get(id)

    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.dns_lookup_index'))
        if target.target_status_code == 'dead':
            flash('error', 'The site seems to be dead')
            return redirect(url_for('home.dns_lookup_index'))

        try:
            dns_result = dns_lookup_hacker_target(target.target_url)
            if target.dnslookup.first() == None:
                dns_lookup = DNSLookup(target, True, dns_result)
            else:
                dns_lookup = DNSLookup.query.get(target.dnslookup.first().id)
                dns_lookup.dnslookup_result = dns_result
        except Exception as Error:
            flash('error', 'Fail to scan DNS Lookup bcz, {}'.format(Error))
            return secure_redirect(request.headers.get('referer'), url_for('home.dns_lookup_index'))

        if dns_lookup == None:
            flash('error', 'no result found for target {}'.format(get_info(target.target_url, info = 'domain')))
            return secure_redirect(request.headers.get('referer'), url_for('home.dns_lookup_index'))
        else:
            db.session.add(dns_lookup)
            db.session.commit()
            flash('success', 'Successfully scanned {}'.format(get_info(target.target_url, info = 'domain')))
            return secure_redirect(request.headers.get('referer'), url_for('home.dns_lookup_index'))
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.dns_lookup_index'))


@home_bp.route('/dnslookup/download/<int:id>')
@login_required
def dns_lookup_download(id):
    tempfile.tempdir = os.getcwd()
    target = Target.query.get(id)

    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.dns_lookup_index'))

        if target.dnslookup.first() == None:
            flash('error', 'You have not done any scan to this target')
            return redirect(url_for('home.dns_lookup_index'))

        with tempfile.TemporaryDirectory() as temp_dir:
            tempfile.tempdir = temp_dir
            file_name = 'dnslookup_' + get_info(target.target_url, info = 'domain') + '.txt'
            file_object = tempfile.NamedTemporaryFile(mode = 'w+t')
            file_content = target.dnslookup.first().dnslookup_result

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
        return redirect(url_for('home.dns_lookup_index'))


@home_bp.route('/dnslookup/view/<int:id>')
@login_required
def dns_lookup_view_raw(id):
    target = Target.query.get(id)

    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.dns_lookup_index'))
        elif target.dnslookup.first() == None:
            flash('error', 'You have not done any scan to this target')
            return redirect(url_for('home.dns_lookup_index'))
        else:
            return target.dnslookup.first().dnslookup_result.replace('\n', '<br>')
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.dns_lookup_index'))
