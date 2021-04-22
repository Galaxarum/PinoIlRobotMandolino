class AnswerReceiver:
    def receive_answer(self, answer):
        raise SystemError('not implemented')


class AnswerProvider:
    def __init__(self, answer_receiver: AnswerReceiver):
        self._answer_receiver = answer_receiver

    def provide_answer(self, right_answer, wrong_answer):
        raise SystemError('not implemented')

    def stop(self):
        pass
