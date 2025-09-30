from asyncio import new_event_loop, set_event_loop

from infrastructure.tasks import filter_and_push
from infrastructure.tasks import read_request_write
from infrastructure.tasks import watch_for_new_files


def compose_application():
    '''
    Creates and runs the loop and creates main tasks.
    '''

    print('Composition began...')

    event_loop = new_event_loop()
    set_event_loop(event_loop)

    event_loop.create_task(watch_for_new_files())
    event_loop.create_task(filter_and_push())
    event_loop.create_task(read_request_write())

    print('Created the event loop and all of the essential tasks...')

    try:
        event_loop.run_forever()
    finally:
        event_loop.close()
