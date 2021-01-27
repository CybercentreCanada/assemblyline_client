import logging
from copy import deepcopy

import socketio

from assemblyline_client.v4_client.common.utils import ClientError


class SocketIO(object):
    def __init__(self, connection):
        class TerminateLogHandler(logging.StreamHandler):
            def __init__(self):
                super(TerminateLogHandler, self).__init__(stream=None)
                self._sio = None

            def emit(self, _):
                # noinspection PyBroadException
                try:
                    self._sio.disconnect()
                except Exception:
                    pass

            def set_sio(self, sio):
                self._sio = sio

        self._server = connection.server
        self._header = {"Cookie": "session=%s" % connection.session.cookies.get('session', None)}
        self._sio = None
        self._log = logging.getLogger('socketIO_client')
        self._log.setLevel(logging.WARNING)
        self._stop_on_warning = TerminateLogHandler()
        self._log.addHandler(self._stop_on_warning)
        self._verify = connection.verify

    # noinspection PyUnusedLocal,PyBroadException
    def _stop_callback(self, data):
        try:
            self._sio.disconnect()
        except Exception:
            pass

    # noinspection PyBroadException
    def _error_callback(self, data):
        try:
            self._sio.disconnect()
        except Exception:
            pass

        raise ClientError(data['err_msg'], data['status_code'])

    def listen_on_alerts_messages(self, alert_created_callback=None, alert_updated_callback=None, timeout=None):
        """\
Listen to the various alerts created messages in the system and call the callback for each alerts

Required:
    alert_created_callback : Callback function for when alerts created messages are received
    alert_updated_callback : Callback function for when alerts updated messages are received

This function wait indefinitely and calls the appropriate callback for each messages returned
"""
        if alert_created_callback is None and alert_updated_callback is None:
            raise ClientError("At least one of the callbacks needs to be defined...", 400)

        self._sio = socketio.Client(ssl_verify=False)
        self._stop_on_warning.set_sio(self._sio)

        if alert_created_callback:
            self._sio.on("AlertCreated", alert_created_callback, namespace='/alerts')
        if alert_updated_callback:
            self._sio.on("AlertUpdated", alert_updated_callback, namespace='/alerts')

        self._sio.connect(self._server, namespaces=['/alerts'], headers=deepcopy(self._header))
        self._sio.emit('alert', {"status": "start", "client": "assemblyline_client"}, namespace='/alerts')
        if timeout is None:
            self._sio.wait()
        else:
            self._sio.sleep(timeout)
            self._sio.disconnect()

    def listen_on_status_messages(self, alerter_msg_callback=None, archive_msg_callback=None,
                                  dispatcher_msg_callback=None, expiry_msg_callback=None,
                                  ingest_msg_callback=None, scaler_msg_callback=None,
                                  scaler_status_msg_callback=None, service_msg_callback=None,
                                  timeout=None):
        """\
Listen to the various status messages you would find on the UI dashboard.

Required (one of):
    alerter_msg_callback :         Callback function when an alerter message is received
    archive_msg_callback :         Callback function when an archive message is received
    dispatcher_msg_callback :      Callback function when a dispatcher message is received
    expiry_msg_callback :          Callback function when an expiry message is received
    ingest_msg_callback :          Callback function when an ingest message is received
    scaler_msg_callback :          Callback function when an scaler message is received
    scaler_status_msg_callback :   Callback function when a scaler status message is received
    service_msg_callback :         Callback function when a service message is received

This function wait indefinitely and calls the appropriate callback for each messages returned
"""
        if dispatcher_msg_callback is None and ingest_msg_callback is None and service_msg_callback is None and \
                alerter_msg_callback is None and expiry_msg_callback is None and scaler_msg_callback is None and \
                archive_msg_callback is None and scaler_status_msg_callback is None:
            raise ClientError("At least one of the callbacks needs to be defined...", 400)

        self._sio = socketio.Client(ssl_verify=False)
        self._stop_on_warning.set_sio(self._sio)

        if alerter_msg_callback:
            self._sio.on("AlerterHeartbeat", alerter_msg_callback, namespace='/status')
        if archive_msg_callback:
            self._sio.on("ArchiveHeartbeat", archive_msg_callback, namespace='/status')
        if dispatcher_msg_callback:
            self._sio.on("DispatcherHeartbeat", dispatcher_msg_callback, namespace='/status')
        if expiry_msg_callback:
            self._sio.on("ExpiryHeartbeat", expiry_msg_callback, namespace='/status')
        if ingest_msg_callback:
            self._sio.on("IngestHeartbeat", ingest_msg_callback, namespace='/status')
        if scaler_msg_callback:
            self._sio.on("ScalerHeartbeat", scaler_msg_callback, namespace='/status')
        if scaler_status_msg_callback:
            self._sio.on("ScalerStatusHeartbeat", scaler_status_msg_callback, namespace='/status')
        if service_msg_callback:
            self._sio.on("ServiceHeartbeat", service_msg_callback, namespace='/status')

        self._sio.connect(self._server, namespaces=['/status'], headers=deepcopy(self._header))
        self._sio.emit('monitor', {"status": "start", "client": "assemblyline_client"}, namespace='/status')

        if timeout is None:
            self._sio.wait()
        else:
            self._sio.sleep(timeout)
            self._sio.disconnect()

    def listen_on_submissions(self, completed_callback=None, ingested_callback=None,
                              received_callback=None, started_callback=None, timeout=None):
        """\
Listen to the various submission messages in the system and call the callback for each of them

Required:
    completed_callback : Callback function for when submission completed messages are received
    ingested_callback : Callback function for when submission ingested messages are received
    received_callback : Callback function for when submission received messages are received
    started_callback : Callback function for when submission started messages are received

This function wait indefinitely and calls the appropriate callback for each messages returned
"""
        if ingested_callback is None and received_callback is None and \
                completed_callback is None and started_callback is None:
            raise ClientError("At least one of the callbacks needs to be defined...", 400)

        self._sio = socketio.Client(ssl_verify=False)
        self._stop_on_warning.set_sio(self._sio)

        if ingested_callback is not None:
            self._sio.on("SubmissionIngested", ingested_callback, namespace='/submissions')

        if received_callback is not None:
            self._sio.on("SubmissionReceived", received_callback, namespace='/submissions')

        if completed_callback is not None:
            self._sio.on("SubmissionCompleted", completed_callback, namespace='/submissions')

        if started_callback is not None:
            self._sio.on("SubmissionStarted", started_callback, namespace='/submissions')

        self._sio.connect(self._server, namespaces=['/submissions'], headers=deepcopy(self._header))
        self._sio.emit('monitor', {"status": "start", "client": "assemblyline_client"}, namespace='/submissions')

        if timeout is None:
            self._sio.wait()
        else:
            self._sio.sleep(timeout)
            self._sio.disconnect()

    def listen_on_watch_queue(self, wq, result_callback=None, error_callback=None, timeout=None):
        """\
Listen to the various messages of a currently running submission's watch queue

Required:
    wq :              ID of the watch queue to listen for
    result_callback : Callback function when receiveing a result cache key
    error_callback :  Callback function when receiveing a error cache key

This function wait indefinitely and calls the appropriate callback for each messages returned
"""
        if result_callback is None and error_callback is None:
            raise ClientError("At least one of the callbacks needs to be defined...", 400)

        self._sio = socketio.Client(ssl_verify=False)
        self._stop_on_warning.set_sio(self._sio)

        if result_callback:
            self._sio.on("cachekey", result_callback, namespace='/live_submission')
        if error_callback:
            self._sio.on("cachekeyerr", error_callback, namespace='/live_submission')

        self._sio.on("stop", self._stop_callback, namespace='/live_submission')
        self._sio.on("error", self._error_callback, namespace='/live_submission')

        self._sio.connect(self._server, namespaces=['/live_submission'], headers=deepcopy(self._header))

        self._sio.emit('listen',
                       {"status": "start", "client": "assemblyline_client", "wq_id": wq, 'from_start': True},
                       namespace="/live_submission")

        if timeout is None:
            self._sio.wait()
        else:
            self._sio.sleep(timeout)
            self._sio.disconnect()
