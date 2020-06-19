import os
import tempfile

from app.model import *
from helper.general import *
from helper.link_scrapper import *

from .home import home_bp
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for, redirect, flash, send_file

@home_bp.route('/linkscrapper')
@login_required
def link_scrapper_index():
    page = request.args.get('page', 1, type = int)
    link = Target.query.filter_by(id_user = current_user.id).paginate(page, 5, False)
    return render_template('home/linkscrapper/list_target.html', targets = link)


@home_bp.route('/linkscrapper/scan/<int:id>')
@login_required
def link_scrapper_scan(id):
    target = Target.query.get(id)
    reference = request.form.get('tools')

    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.link_scrapper_index'))

        if target.target_status_code == 'dead':
            flash('error', 'Target seems to be dead')
            return redirect(url_for('home.link_scrapper_index'))

        try:
            if reference == 'hackertarget':
                found_link = find_link_hacker_target(target.target_url)
            elif reference == 'manual':
                found_link = find_link_manual(target.target_url)
            else:
                flash('error', 'Specify appropriate reference!')
                return secure_redirect(request.headers.get('referer'), url_for('home.link_scrapper_index'))
        except Exception as Error:
            flash('error', 'fail to scan bcz, {}'.format(Error))
            return secure_redirect(request.headers.get('referer'), url_for('home.link_scrapper_index'))

        if found_link != None:
            if target.foundlink.first() == None:
                targetlink = FoundLink(target, found_link)
            else:
                targetlink = FoundLink.query.get(target.foundlink.first().id)
                targetlink.found_link = found_link
            db.session.add(targetlink)
            db.session.commit()
        else:
            flash('error', 'No link found in {}'.format(target.target_url))
            return secure_redirect(request.headers.get('referer'), url_for('home.link_scrapper_index'))

        flash('success', 'Found {} links in {}'.format(str(len(found_link)), target.target_url))
        return secure_redirect(request.headers.get('referer'), url_for('home.link_scrapper_index'))
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.link_scrapper_index'))
