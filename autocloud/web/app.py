# -*- coding: utf-8 -*-

from __future__ import absolute_import

import flask
import flask.ext.restless

from flask import request, url_for, render_template
from sqlalchemy import desc
from werkzeug.exceptions import abort

import autocloud

from autocloud.models import init_model
from autocloud.models import JobDetails, ComposeJobDetails, ComposeDetails
from autocloud.web.pagination import RangeBasedPagination
from autocloud.web.utils import get_object_or_404

app = flask.Flask(__name__)
session = init_model()


class JobDetailsPagination(RangeBasedPagination):

    def get_page_link(self, page_key, limit):
        get_params = dict(request.args)
        get_params.update({
            'from': page_key, 'limit': limit})
        return url_for('job_details', **dict(
            [(key, value) for key, value in get_params.items()])
        )

    def order_queryset(self):
        if self.direction == 'next':
            self.queryset = self.queryset.order_by(desc(
                ComposeJobDetails.id))
        else:
            self.queryset = self.queryset.order_by(ComposeJobDetails.id)

    def filter_queryset(self):
        if self.page_key is None:
            return
        from_jobdetails = session.query(ComposeJobDetails).get(self.page_key)
        if from_jobdetails:
            if self.direction == 'prev':
                self.queryset = self.queryset.filter(
                    ComposeJobDetails.id > from_jobdetails.id)
            else:
                self.queryset = self.queryset.filter(
                    ComposeJobDetails.id < from_jobdetails.id)


class ComposeDetailsPagination(RangeBasedPagination):
    def get_page_link(self, page_key, limit):
        get_params = dict(request.args)
        get_params.update({
            'from': page_key, 'limit': limit})
        return url_for('compose_details', **dict(
            [(key, value) for key, value in get_params.items()])
        )

    def order_queryset(self):
        if self.direction == 'next':
            self.queryset = self.queryset.order_by(desc(
                ComposeDetails.id))
        else:
            self.queryset = self.queryset.order_by(ComposeDetails.id)

    def filter_queryset(self):
        if self.page_key is None:
            return
        from_jobdetails = session.query(ComposeDetails).get(self.page_key)
        if from_jobdetails:
            if self.direction == 'prev':
                self.queryset = self.queryset.filter(
                    ComposeDetails.id > from_jobdetails.id)
            else:
                self.queryset = self.queryset.filter(
                    ComposeDetails.id < from_jobdetails.id)


@app.route('/')
def index():
    return flask.render_template('index.html', navbar_fixed=True)


@app.route('/compose/')
@app.route('/compose')
def compose_details():
    queryset = session.query(ComposeDetails)

    limit = int(request.args.get('limit', 5))
    compose_details, prev_link, next_link = ComposeDetailsPagination(
        queryset, request.args.get('from'), limit, request.path,
        request.referrer, dict(request.args)).paginate()

    compose_ids = [item.compose_id for item in compose_details]
    compose_locations = dict(session.query(
        ComposeDetails.compose_id,
        ComposeDetails.location).filter(
            ComposeDetails.compose_id.in_(compose_ids)).all())

    return flask.render_template(
        'compose_details.html', compose_details=compose_details,
        prev_link=prev_link, next_link=next_link,
        compose_locations=compose_locations,
        navbar_fixed=True
    )


@app.route('/jobs/')
@app.route('/jobs')
@app.route('/jobs/<compose_pk>/')
@app.route('/jobs/<compose_pk>')
def job_details(compose_pk=None):
    queryset = session.query(ComposeJobDetails)
    supported_archs = [arch for arch, _ in ComposeJobDetails.ARCH_TYPES]

    if compose_pk is not None:
        compose_obj = session.query(ComposeDetails).get(compose_pk)
        if compose_obj is None:
            abort(404)

        compose_id = compose_obj.compose_id

        queryset = queryset.filter_by(compose_id=compose_id).filter(
                ComposeJobDetails.arch.in_(supported_archs))

    # Apply filters
    filters = ('family', 'arch', 'status', 'image_type')
    selected_filters = {}
    for filter in filters:
        if request.args.get(filter):
            queryset = queryset.filter(
                getattr(ComposeJobDetails, filter) == request.args[filter])
            selected_filters[filter] = request.args[filter]

    limit = int(request.args.get('limit', 50))
    job_details, prev_link, next_link = JobDetailsPagination(
        queryset, request.args.get('from'), limit,
        request.path,
        request.referrer, dict(request.args)).paginate()
    filter_fields = (
        {'label': 'Family', 'name': 'family',
         'options': ComposeJobDetails.IMAGE_FAMILY_TYPES},
        {'label': 'Architecture', 'name': 'arch',
         'options': ComposeJobDetails.ARCH_TYPES},
        {'label': 'Type', 'name': 'image_type',
         'options': [(value[0], value[0])
                     for value in session.query(
                         ComposeJobDetails.image_type).distinct()]},
        {'label': 'Status', 'name': 'status',
         'options': ComposeJobDetails.STATUS_TYPES}
    )

    compose_ids = [item.compose_id for item in job_details]
    compose_locations = dict(session.query(
        ComposeDetails.compose_id,
        ComposeDetails.location).filter(
            ComposeDetails.compose_id.in_(compose_ids)).all())

    return flask.render_template(
        'job_details.html', job_details=job_details, prev_link=prev_link,
        next_link=next_link, filter_fields=filter_fields,
        selected_filters=selected_filters, compose_locations=compose_locations,
        navbar_fixed=True
    )


@app.route('/jobs/<jobid>/output')
def job_output(jobid):
    job_detail = get_object_or_404(session,
                                   ComposeJobDetails,
                                   ComposeJobDetails.id == jobid)

    _id = session.query(ComposeDetails.id).filter_by(
        compose_id=job_detail.compose_id).all()[0][0]

    compose_locations = dict(session.query(
        ComposeDetails.compose_id,
        ComposeDetails.location).filter(
            ComposeDetails.compose_id.in_(job_detail.compose_id)).all())

    job_output_lines = []
    if job_detail.output:
        job_output_lines = job_detail.output.split('\n')

    return flask.render_template(
        'job_output.html', job_detail=job_detail,
        compose_locations=compose_locations, _id=_id,
        job_output_lines=job_output_lines, navbar_fixed=False)


# Custom Error pages
@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404

# API stuff
apimanager = flask.ext.restless.APIManager(app, session=session)
apimanager.create_api(JobDetails, methods=['GET'])

if __name__ == '__main__':
    app.run(host=autocloud.HOST, port=autocloud.PORT, debug=autocloud.DEBUG)
