import threading
import time

import pytest

try:
    from assemblyline.odm.messages.alert import AlertMessage
    from assemblyline.odm.messages.alerter_heartbeat import AlerterMessage
    from assemblyline.odm.messages.dispatcher_heartbeat import DispatcherMessage
    from assemblyline.odm.messages.expiry_heartbeat import ExpiryMessage
    from assemblyline.odm.messages.ingest_heartbeat import IngestMessage
    from assemblyline.odm.messages.service_heartbeat import ServiceMessage
    from assemblyline.odm.messages.service_timing_heartbeat import ServiceTimingMessage
    from assemblyline.odm.messages.submission import SubmissionMessage
    from assemblyline.odm.randomizer import random_model_obj
    from assemblyline.remote.datatypes.queues.comms import CommsQueue
    from assemblyline.remote.datatypes.queues.named import NamedQueue

    from assemblyline_client.v4_client.common.utils import get_random_id
except (ImportError, SyntaxError):
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_alert_created(datastore, client):
    alert_queue = CommsQueue('alerts', private=True)

    created = random_model_obj(AlertMessage)
    created.msg_type = "AlertCreated"

    updated = random_model_obj(AlertMessage)
    updated.msg_type = "AlertUpdated"

    test_res_array = []

    def alerter_created_callback(data):
        test_res_array.append(('created', created['msg'] == data))

    def alerter_updated_callback(data):
        test_res_array.append(('updated', updated['msg'] == data))

    def publish_thread():
        time.sleep(1)
        alert_queue.publish(created.as_primitives())
        alert_queue.publish(updated.as_primitives())

    threading.Thread(target=publish_thread).start()
    client.socketio.listen_on_alerts_messages(alert_created_callback=alerter_created_callback,
                                              alert_updated_callback=alerter_updated_callback,
                                              timeout=2)
    assert len(test_res_array) == 2

    for test, result in test_res_array:
        if not result:
            pytest.fail("{} failed.".format(test))


def test_status_messages(datastore, client):
    status_queue = CommsQueue('status', private=True)
    test_res_array = []

    alerter_hb_msg = random_model_obj(AlerterMessage).as_primitives()
    dispatcher_hb_msg = random_model_obj(DispatcherMessage).as_primitives()
    expiry_hb_msg = random_model_obj(ExpiryMessage).as_primitives()
    ingest_hb_msg = random_model_obj(IngestMessage).as_primitives()
    service_hb_msg = random_model_obj(ServiceMessage).as_primitives()
    service_timing_msg = random_model_obj(ServiceTimingMessage).as_primitives()

    def alerter_callback(data):
        test_res_array.append(('alerter', alerter_hb_msg['msg'] == data))

    def dispatcher_callback(data):
        test_res_array.append(('dispatcher', dispatcher_hb_msg['msg'] == data))

    def expiry_callback(data):
        test_res_array.append(('expiry', expiry_hb_msg['msg'] == data))

    def ingest_callback(data):
        test_res_array.append(('ingest', ingest_hb_msg['msg'] == data))

    def service_callback(data):
        test_res_array.append(('service', service_hb_msg['msg'] == data))

    def service_timing_callback(data):
        test_res_array.append(('service_timing', service_timing_msg['msg'] == data))

    def publish_thread():
        time.sleep(1)
        status_queue.publish(alerter_hb_msg)
        status_queue.publish(dispatcher_hb_msg)
        status_queue.publish(expiry_hb_msg)
        status_queue.publish(ingest_hb_msg)
        status_queue.publish(service_hb_msg)
        status_queue.publish(service_timing_msg)

    threading.Thread(target=publish_thread).start()
    client.socketio.listen_on_status_messages(alerter_msg_callback=alerter_callback,
                                              dispatcher_msg_callback=dispatcher_callback,
                                              expiry_msg_callback=expiry_callback,
                                              ingest_msg_callback=ingest_callback,
                                              service_msg_callback=service_callback,
                                              service_timing_msg_callback=service_timing_callback,
                                              timeout=2)
    assert len(test_res_array) == 6

    for test, result in test_res_array:
        if not result:
            pytest.fail("{} failed.".format(test))


def test_submission_ingested(datastore, client):
    submission_queue = CommsQueue('submissions', private=True)
    test_res_array = []

    ingested = random_model_obj(SubmissionMessage).as_primitives()
    ingested['msg_type'] = "SubmissionIngested"
    received = random_model_obj(SubmissionMessage).as_primitives()
    received['msg_type'] = "SubmissionReceived"
    queued = random_model_obj(SubmissionMessage).as_primitives()
    queued['msg_type'] = "SubmissionQueued"
    started = random_model_obj(SubmissionMessage).as_primitives()
    started['msg_type'] = "SubmissionStarted"

    def ingested_callback(data):
        test_res_array.append(('ingested', ingested['msg'] == data))

    def received_callback(data):
        test_res_array.append(('received', received['msg'] == data))

    def queued_callback(data):
        test_res_array.append(('queued', queued['msg'] == data))

    def started_callback(data):
        test_res_array.append(('started', started['msg'] == data))

    def publish_thread():
        time.sleep(1)
        submission_queue.publish(ingested)
        submission_queue.publish(received)
        submission_queue.publish(queued)
        submission_queue.publish(started)

    threading.Thread(target=publish_thread).start()
    client.socketio.listen_on_submissions(ingested_callback=ingested_callback,
                                          received_callback=received_callback,
                                          queued_callback=queued_callback,
                                          started_callback=started_callback,
                                          timeout=2)

    assert len(test_res_array) == 4

    for test, result in test_res_array:
        if not result:
            pytest.fail("{} failed.".format(test))


def test_watch_queue_messages(datastore, client):
    wq_data = {'wq_id': get_random_id()}
    wq = NamedQueue(wq_data['wq_id'], private=True)

    start_msg = {'status': 'START'}
    stop_msg = {'status': 'STOP'}
    cachekey_msg = {'status': 'OK', 'cache_key': get_random_id()}
    cachekeyerr_msg = {'status': 'FAIL', 'cache_key': get_random_id()}

    test_res_array = []

    def result_callback(data):
        test_res_array.append(('result', data['msg'] == cachekey_msg['cache_key']))

    def error_callback(data):
        test_res_array.append(('error', data['msg'] == cachekeyerr_msg['cache_key']))

    def publish_thread():
        time.sleep(1)
        wq.push(start_msg)
        wq.push(cachekey_msg)
        wq.push(cachekeyerr_msg)
        wq.push(stop_msg)

    threading.Thread(target=publish_thread).start()
    client.socketio.listen_on_watch_queue(wq_data['wq_id'],
                                          result_callback=result_callback,
                                          error_callback=error_callback,
                                          timeout=2)

    assert len(test_res_array) == 2

    for test, result in test_res_array:
        if not result:
            pytest.fail("{} failed.".format(test))
