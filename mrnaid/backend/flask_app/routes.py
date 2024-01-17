import json

from flask import Flask
from flask import request
from tasks import optimization_evaluation_task
from flask_cors import CORS
from utils.Exceptions import EmptySequenceError, SequenceLengthError, NoGCError, EntropyWindowError, \
    NumberOfSequencesError, WrongCharSequenceError, RangeError, SpeciesError
from utils.Logger import MyLogger
from utils.RequestParser import RequestParser

app = Flask(__name__)
CORS(app)

# Setting up a logger
logger = MyLogger(__name__)


# Defining the routes
@app.route('/api/v1/optimize', methods=['POST'])
def optimization():
    """
    Parse optimization task parameters from the request, create a celery task for optimization.
    :return: JSON with task ID
    """
    # Processing the input
    logger.info(10 * '#' + 'NEW REQUEST' + 10 * '#')
    parser = RequestParser(request)

    # -- Getting input sequences
    try:
        parameters = parser.parse()
    except (EmptySequenceError, SequenceLengthError, NoGCError, EntropyWindowError, NumberOfSequencesError,
            WrongCharSequenceError,
            RangeError, SpeciesError) as e:
        logger.error(e.message)
        return e.message, 500
    except KeyError as e:
        logger.error('Error with json structure for the input sequences', exc_info=True)
        return 'Problem with json structure for the input sequences. Contact administrator. {}'.format(str(e)), 500
    else:
        logger.debug('Sequences are received from Parser')

    # Task optimization/evaluation:
    try:
        task = optimization_evaluation_task.apply_async(args=[parameters.dict()],
                                                        kwargs={})
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f'Something went wrong when sending task to the queue: {e}')
        return str(e), 500
    else:
        return json.dumps({'task_id': task.id})


@app.route('/api/v1/status/<task_id>', methods=['GET'])
def status(task_id: str) -> str:
    """
    Get task status based on task ID
    :param task_id: string
    :return: JSON with task ID, task state, message and task result, if any.
    """
    task = optimization_evaluation_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        return json.dumps(
            {"message": "Task is in progress... Lay back or get some coffee, I'm working hard on your request!",
             "task_id": task.id,
             "state": task.state,
             "data": None}), 202
    elif task.state == 'FAILURE':
        logger.info(10 * '#' + 'END OF PROCESSING THE REQUEST: FAILURE' + 10 * '#')
        return json.dumps(
            {
                "message": f"Ooops, something went wrong! Please contact administrator and provide him/her your task id: {task.id}",
                "task_id": task.id,
                "state": task.state,
                "data": None}), 500
    elif task.state == 'SUCCESS':
        logger.info(10 * '#' + 'END OF PROCESSING THE REQUEST: SUCCESS' + 10 * '#')
        return json.dumps(
            {"message": "Done!",
             "task_id": task.id,
             "state": task.state,
             "data": json.loads(task.get())})
