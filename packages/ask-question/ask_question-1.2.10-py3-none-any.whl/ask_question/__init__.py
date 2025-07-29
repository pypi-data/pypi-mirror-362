"""
File in charge of automating and simplify the process of asking a question and expecting a specific type of response
"""

from .ask_question import AskQuestion
TUI_AVAILABLE = True


try:
    from .ask_question_tui import AskQuestionTUI
except ImportError:
    TUI_AVAILABLE = False

__all__ = [
    "ask_question", "askquestion", "Ask_Question", "ASK_QUESTION", "ASKQUESTION"
]

if TUI_AVAILABLE:
    __all__.extend([
        "AskQuestionTUI", "ask_question_tui", "askquestiontui",
        "Ask_Question_TUI", "ASK_QUESTION_TUI", "ASKQUESTIONTUI"
    ])

__version__ = "1.2.0"

if TUI_AVAILABLE:
    class ask_question_tui(AskQuestionTUI):
        """ Ask a question to the user while expecting a specific format """

    class askquestiontui(AskQuestionTUI):
        """ Ask a question to the user while expecting a specific format """

    class Ask_Question_TUI(AskQuestionTUI):
        """ Ask a question to the user while expecting a specific format """

    class ASK_QUESTION_TUI(AskQuestionTUI):
        """ Ask a question to the user while expecting a specific format """

    class ASKQUESTIONTUI(AskQuestionTUI):
        """ Ask a question to the user while expecting a specific format """


class ask_question(AskQuestion):
    """ Ask a question to the user while expecting a specific format """
    pass


class askquestion(AskQuestion):
    """ Ask a question to the user while expecting a specific format """
    pass


class Ask_Question(AskQuestion):
    """ Ask a question to the user while expecting a specific format """
    pass


class ASK_QUESTION(AskQuestion):
    """ Ask a question to the user while expecting a specific format """
    pass


class ASKQUESTION(AskQuestion):
    """ Ask a question to the user while expecting a specific format """
    pass
