#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash, g
from flask_babel import lazy_gettext,gettext
from flask_login import login_required

from app.utils import admin_required, crypt
from app.data.models import Firma
from app.public.forms import EditFirmaForm
from . import admin


@admin.route('/firma/list', methods=['GET', 'POST'])
@admin_required
def firma_list():

    from app.data import DataTable
    datatable = DataTable(
        model=Firma,
        columns=[],
        sortable=[Firma.nazev, Firma.created_ts],
        searchable=[Firma.nazev],
        filterable=[],
        limits=[25, 50, 100],
        request=request
    )

    if g.pjax:
        return render_template(
            'firma.html',
            datatable=datatable
        )

    return render_template(
        'firma-list.html',
        datatable=datatable
    )


@admin.route('/firma/edit/<str_hash>', methods=['GET', 'POST'])
@admin_required
def firma_edit(str_hash):
    id = int(float(crypt(str_hash, decrypt=True)))
    firma = Firma.query.filter_by(id=id).first_or_404()
    form = EditFirmaForm(obj=firma)
    if form.validate_on_submit():
        form.populate_obj(firma)
        firma.commit()
        flash(gettext('Organization {nazev} edited').format(nazev=firma.nazev),'success')
    return render_template('firma-edit.html', form=form, firma=firma)


@admin.route('/firma/delete/<str_hash>', methods=['GET'])
@admin_required
def firma_delete(str_hash):
    id = int(float(crypt(str_hash, decrypt=True)))
    firma = Firma.query.filter_by(id=id).first_or_404()
    firma.delete()
    flash(gettext('Organization {nazev} deleted').format(nazev=firma.nazev),'success')
    return redirect(url_for('.firma_list'))
