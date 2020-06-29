import os

from app.model import *
from helper.general import *
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for, flash

home_bp = Blueprint('home', __name__, template_folder = 'views')

from .user import *
from .whois import *
from .dns_lookup import *
from .reverse_ip import *
from .link_scrapper import *
from .wp_user_finder import *

@home_bp.route('/')
@home_bp.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type = int)
    target = Target.query.filter_by(id_user = current_user.id).paginate(page, 5, False)
    return render_template('home/index.html', targets = target)


@home_bp.route('/edit_profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        realname = request.form.get('realname', '')
        username = request.form.get('username', '')
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')

        if not filter_edit_form(realname, username, new_password):
            return redirect(url_for('home.edit_profile'))

        current_user.real_name = realname
        current_user.user_name = username

        if old_password != '' and new_password != '':
            if current_user.check_password(old_password) == True:
                current_user.secure_password(new_password)
            else:
                flash('error', 'Old password is incorrect.')
                return redirect(url_for('home.edit_profile'))

        db.session.add(current_user)
        db.session.commit()

        flash('success', 'Successfully update profile.')
        return redirect(url_for('home.edit_profile'))
    else:
        roles = Role.query.all()
        return render_template('home/edit_profile.html', user = current_user, roles = roles)


@home_bp.route('/add', methods = ['POST'])
@login_required
def add_target():
    target_url  = request.form.get('target_url', '')

    if not filter_target_form(target_url):
        return redirect(url_for('home.index'))

    check_conn = check_connection(target_url)

    target = Target(current_user, target_url)
    target.target_url = check_conn.get('url')
    target.target_server = check_conn.get('server')
    target.target_country = get_country(target_url)
    target.target_status_code = check_conn.get('code')

    db.session.add(target)
    db.session.commit()

    flash('success', 'Successfully add target.')
    return redirect(url_for('home.index'))


@home_bp.route('/delete/<int:id>')
@login_required
def delete_target(id):
    target = Target.query.get(id)
    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.index'))
        else:
            db.session.delete(target)
            db.session.commit()
            flash('success', 'Successfully delete target.')
            return redirect(url_for('home.index'))
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.index'))


@home_bp.route('/check/<int:id>')
@login_required
def check_target_connection(id):
    target = Target.query.get(id)

    if target != None:
        check_conn = check_connection(target.target_url)
        target.target_url = check_conn.get('url')
        target.target_status_code = check_conn.get('code')

        db.session.add(target)
        db.session.commit()
        return redirect(url_for('home.index'))
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.index'))


@home_bp.route('/download_list')
@login_required
def download_list():
    tempfile.tempdir = os.getcwd()
    list_target = Target.query.filter_by(id_user = current_user.id).all()

    if len(list_target) != 0:
        with tempfile.TemporaryDirectory() as temp_dir:
            tempfile.tempdir = temp_dir
            file_name = 'list_target_' + current_user.user_name + '.txt'
            file_object = tempfile.NamedTemporaryFile(mode = 'w+t')
            file_content = [
                [
                    target.target_url, target.target_server,
                    target.target_country, target.target_status_code
                ] for target in list_target
            ]
            file_content = ['|'.join(target) for target in file_content]
            file_content = '\n'.join(file_content)

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
        flash('error', 'You have not even input one target')
        return redirect(url_for('home.index'))


@home_bp.route('/view_raw_list')
@login_required
def view_raw_list():
    list_target = Target.query.filter_by(id_user = current_user.id).all()

    if len(list_target) != 0:
        content = [
            [
                target.target_url, target.target_server,
                target.target_country, target.target_status_code
            ] for target in list_target
        ]
        content = ['|'.join(target) for target in content]
        content = '<br>'.join(content)
        return content
    else:
        flash('error', 'You have not even input one target')
        return redirect(url_for('home.index'))


@home_bp.route('/view_raw_info/<int:id>')
@login_required
def view_raw_info(id):
    target = Target.query.filter_by(id_user = current_user.id, id = id).first()

    if target != None:
        content = ''
        whois = target.whois.first()
        wp_user = target.wpuser.first()
        reverse_ip = target.revip.first()
        dns_lookup = target.dnslookup.first()
        link_scrapper = target.foundlink.first()

        if whois != None:
            content += '''
            ## Whois Result
            <br>
            {}
            <br><br>
            '''.format(whois.whois_result.replace('\n', '<br>'))

        if dns_lookup != None:
            content += '''
            ## DNS Lookup Result
            <br>
            {}
            <br><br>
            '''.format(dns_lookup.dnslookup_result.replace('\n', '<br>'))

        if reverse_ip != None:
            content += '''
            ## Reverse IP
            <br>
            {}
            <br><br>
            '''.format('<br>'.join(domain for domain in reverse_ip.list_domain))

        if wp_user != None:
            content += '''
            ## Wordpress User
            <br>
            {}
            <br><br>
            '''.format('<br>'.join(user for user in wp_user.list_username))

        if link_scrapper != None:
            content += '''
            ## Found Link
            <br>
            {}
            <br><br>
            '''.format('<br>'.join(link for link in link_scrapper.found_link))

        return content
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.index'))


@home_bp.route('/download_info/<int:id>')
@login_required
def download_info(id):
    tempfile.tempdir = os.getcwd()
    target = Target.query.filter_by(id_user = current_user.id, id = id).first()

    if target != None:
        content = ''
        whois = target.whois.first()
        wp_user = target.wpuser.first()
        reverse_ip = target.revip.first()
        dns_lookup = target.dnslookup.first()
        link_scrapper = target.foundlink.first()

        # i dont use assignment operator += because it doesnt work, idk why:'
        if whois != None:
            content = content + "\n\n" + "## Whois Result\n{}\n".format(whois.whois_result).strip()

        if dns_lookup != None:
            content = content + "\n\n" + "## DNS Lookup Result\n{}\n".format(dns_lookup.dnslookup_result).strip()

        if reverse_ip != None:
            content = content + "\n\n" + "\n## Reverse IP\n{}\n".format('\n'.join(domain for domain in reverse_ip.list_domain)).strip()

        if wp_user != None:
            content = content + "\n\n" + '\n## Wordpress User\n{}\n'.format('\n'.join(user for user in wp_user.list_username)).strip()

        if link_scrapper != None:
            content = content + "\n\n" + '\n## Found Link\n{}\n'.format('\n'.join(link for link in link_scrapper.found_link)).strip()

        with tempfile.TemporaryDirectory() as temp_dir:
            tempfile.tempdir = temp_dir
            file_name = 'info_' + get_info(target.target_url, info = 'domain') + '.txt'
            file_object = tempfile.NamedTemporaryFile(mode = 'w+t')
            file_content = content

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
        return redirect(url_for('home.index'))


@home_bp.route('/update')
@login_required
def update():
    if current_user.user_role.id == 1:
        check_update = auto_update()
        if check_update == True:
            flash('success', 'Successfully updated.')
        else:
            flash('error', 'No updates found.')
        return redirect(url_for('home.index'))
    else:
        return redirect(url_for('home.index'))
