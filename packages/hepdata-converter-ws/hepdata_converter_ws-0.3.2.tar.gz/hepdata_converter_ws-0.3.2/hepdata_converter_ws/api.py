# -*- encoding: utf-8 -*-
from io import BytesIO
import base64
import os
import tarfile
import tempfile
from flask.globals import request
from flask.wrappers import Response
import hepdata_converter
import shutil
from flask import current_app, Blueprint, render_template
api = Blueprint('api', __name__)

__author__ = 'Michał Szostak'

SINGLEFILE_FORMATS = ['root', 'yoda', 'yoda1', 'yoda.h5']


@api.route('/debug-sentry')
def trigger_error():
    raise Exception('Testing that Sentry picks up this error')


@api.route('/ping', methods=['GET'])
def ping():
    return Response('OK')


@api.route('/convert', methods=['GET'])
def convert():
    kwargs = request.get_json(force=True)
    input_tar = kwargs['input']
    archive_name = kwargs['options'].get('filename', 'hepdata-converter-ws-data')
    output_format = kwargs['options'].get('output_format', '')

    output, os_handle = BytesIO(), None
    if output_format.lower() in SINGLEFILE_FORMATS or 'table' in kwargs['options']:
        os_handle, tmp_output = tempfile.mkstemp(suffix='.'+output_format if output_format else '')
    else:
        tmp_output = tempfile.mkdtemp()

    tmp_dir = tempfile.mkdtemp()
    try:
        conversion_input = os.path.abspath(tmp_dir)
        conversion_output = os.path.abspath(tmp_output)

        with tarfile.open(mode="r:gz", fileobj=BytesIO(base64.b64decode(input_tar))) as tar:
            tar.extractall(path=conversion_input)

        # one file - treat it as one file input format
        walked = list(os.walk(tmp_dir))
        if len(walked) == 1 and len(walked[0][2]) == 1:
            path, dirs, files = walked[0]
            conversion_input = os.path.join(path, files[0])
        else:
            conversion_input = conversion_input + '/' + archive_name + '/'

        hepdata_converter.convert(conversion_input,
                                  conversion_output,
                                  kwargs.get('options', {}))

        if not os.path.isdir(conversion_output):
            output_format = output_format[:-1] if output_format == 'yoda1' else output_format
            archive_name = archive_name + '.' + output_format

        with tarfile.open(mode='w:gz', fileobj=output) as tar:
            tar.add(conversion_output, arcname=archive_name)

    finally:
        if os_handle:
            os.fdopen(os_handle).close()
            if os.path.exists(tmp_output):
                os.remove(tmp_output)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        shutil.rmtree(tmp_output, ignore_errors=True)

    return Response(output.getvalue(), mimetype='application/x-gzip')
