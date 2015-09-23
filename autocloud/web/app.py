# -*- coding: utf-8 -*-

from __future__ import absolute_import
import flask
from flask import request, url_for
import os
from sqlalchemy import desc
from autocloud.models import init_model
from autocloud.models import JobDetails
from autocloud.web.pagination import RangeBasedPagination
from autocloud.web.utils import get_object_or_404
import autocloud

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
                JobDetails.id))
        else:
            self.queryset = self.queryset.order_by(JobDetails.id)

    def filter_queryset(self):
        if self.page_key is None:
            return
        from_jobdetails = session.query(JobDetails).get(self.page_key)
        if from_jobdetails:
            if self.direction == 'prev':
                self.queryset = self.queryset.filter(
                    JobDetails.id > from_jobdetails.id)
            else:
                self.queryset = self.queryset.filter(
                    JobDetails.id < from_jobdetails.id)


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/jobs')
@app.route('/jobs/')
def job_details():
    queryset = session.query(JobDetails)
    limit = int(request.args.get('limit', 50))
    job_details, prev_link, next_link = JobDetailsPagination(
        queryset, request.args.get('from'), limit,
        request.path,
        request.referrer, dict(request.args)).paginate()
    return flask.render_template(
        'job_details.html', job_details=job_details, prev_link=prev_link,
        next_link=next_link
    )


@app.route('/jobs/<jobid>/output')
def job_output(jobid):
    job = get_object_or_404(session, JobDetails, JobDetails.id == jobid)
    return flask.render_template(
        'job_output.html', job=job)

if __name__ == '__main__':
    app.run(host=autocloud.HOST, port=autocloud.PORT, debug=autocloud.DEBUG)
