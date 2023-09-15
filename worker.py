#!/usr/bin/env python3
import argparse
import os

import src.config as config

from threading import Thread

from src.common.amqp import QueueConsumer, configure_queue
from src.common.logger import get_logger

logger = get_logger(__name__)

try:
    #import worker implementation module here
    pass
except ModuleNotFoundError:
    pass
    #set module to None if error

message_processor = None
worker_name = None
worker_info = {
    # '<worker_name_1>': {
    #     'message_processor': <worker_module_name>,
    #     'queue': <queue_name>,
    #     'routing_key': <routing_key>
    # },
}

parser = argparse.ArgumentParser(description='Model Server Worker(s)')
# pylint: disable=dict-keys-not-iterating
parser.add_argument('-w', '--worker', required=False,
                    choices=worker_info.keys())


def callback(params):
    if 'queue_consumer' not in params.keys():
        raise RuntimeError(
            'Cannot continue as params does not contain queue_consumer instance')
    if 'basic_deliver' not in params.keys():
        raise RuntimeError(
            'Cannot continue as params does not contain basic_deliver')
    if params['queue_consumer'] is None:
        raise RuntimeError('queue_consumer is None!!!.')

    th = Thread(target=message_consumer, kwargs={
                'params': params}, daemon=False)
    th.start()


def message_consumer(params):
    queue_consumer = params['queue_consumer']
    basic_deliver = params['basic_deliver']
    try:
        process_message(params)
    except Exception as e:
        logger.error(f'Dropping message! E:{e}')
    finally:
        queue_consumer.add_callback_threadsafe(basic_deliver)


def print_sanitized_params(params, hide_jwt=True, hide_list=False):
    sanitized_params = {}
    for k, v in params.items():
        if k in ['queue_consumer', 'basic_deliver']:
            continue
        if hide_jwt is True and 'jwt' in k:
            continue
        if hide_list is True and isinstance(v, list):
            sanitized_params[k] = f'List with {len(v)} items'
            continue
        sanitized_params[k] = v
    logger.info('-' * 30)
    logger.info('Params:')
    for k, v in sanitized_params.items():
        try:
            logger.info(f'{k}: {v}')
        except Exception as e:
            logger.info(f'{k}: Unable to serialize. E:{e}')
    logger.info('-' * 30)


def process_message(params):
    global message_processor

    logger.info('Received message:')

    print_sanitized_params(params, hide_jwt=True, hide_list=True)
    params = {k: v for k, v in params.items() if k not in [
        'queue_consumer', 'basic_deliver']}

    try:
        if callable(message_processor):
            message_processor(params)

        else:
            raise RuntimeError(
                'Message processor not callable. Cannot process message!!!!')

    except Exception as e:
        logger.error(
            f'Error in worker:{worker_name} message: E: {e}', exc_info=True)
        print_sanitized_params(params, hide_jwt=True, hide_list=False)

        raise


def main():
    if len(worker_info) == 0:
        logger.info("No workers to spin up. Exiting...")
        exit(0)

    global message_processor
    global worker_name

    args = vars(parser.parse_args())
    worker_name = args.get('worker', None)

    if worker_name is None:
        worker_name = os.environ.get('WORKER_NAME')

    logger.info('--- Starting {} ---'.format(worker_name))

    priority = 255

    message_processor = worker_info[worker_name]['message_processor']

    logger.info(f"Binding {worker_name} to exchange: {config.EXCHANGE_NAME}")
    configure_queue(config.RABBIT_URL,
                    config.EXCHANGE_NAME,
                    worker_info[worker_name]['queue'],
                    worker_info[worker_name]['routing_key'],
                    priority=priority)

    if worker_info[worker_name].get('bind_to_delay_exchange', False) is True:
        if config.ENABLE_REQUEUE is True:
            logger.info(
                f"Also binding {worker_name} to delay exchange: {config.DELAY_EXCHANGE_NAME}")
            configure_queue(config.RABBIT_URL,
                            config.DELAY_EXCHANGE_NAME,
                            worker_info[worker_name]['queue'],
                            worker_info[worker_name]['routing_key'],
                            priority=priority,
                            exchange_type='x-delayed-message')

        else:
            logger.warning(f"ENABLE_REQUEUE=False - not binding {worker_name} "
                           f"to delay exchange: {config.DELAY_EXCHANGE_NAME}")

    consumer = QueueConsumer(
        config.RABBIT_URL, worker_info[worker_name]['queue'], callback)

    try:
        consumer.run()

    except KeyboardInterrupt:
        logger.info(f'\nExiting Worker')
        consumer.stop()
        consumer.close_connection()
        logger.info('Bye!!!')


if __name__ == '__main__':
    main()
