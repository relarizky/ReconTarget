from app.model import *
from helper.user import *
from helper.reverse_ip import *

from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for, redirect, flash
from .home import home_bp

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
                return redirect(url_for('home.reverse_ip_index'))
        except Exception as Error:
            flash('error', 'Fail to do reverse ip bcz, {}'.format(Error))
            return redirect(url_for('home.reverse_ip_index'))

        if target.revip.all() == []:
            tb_revip = RevIP(target, revip)
        else:
            tb_revip = RevIP.query.get(target.revip.first().id)
            old_list = target.revip.first().list_domain
            new_list = set(old_list + revip) # remove duplicate
            tb_revip.list_domain = list(new_list)

        db.session.add(tb_revip)
        db.session.commit()
        flash('success', 'Found {} other sites in same server'.format(str(len(revip))))
        return redirect(url_for('home.reverse_ip_index'))
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.reverse_ip_index'))
