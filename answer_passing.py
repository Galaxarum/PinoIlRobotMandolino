class AnswerReceiver:
    def receive_answer(self, answer):
        raise SystemError('not implemented')


class AnswerProvider:
    def provide_answer(self, right_answer, wrong_answer):
        raise SystemError('not implemented')
