"""
File in charge of containing the demo script for the ask question TUI library
"""

from ask_question.ask_question import AskQuestion

TUI_AVAILABLE = True
try:
    from asciimatics import widgets as WIG
    from asciimatics.event import Event
    from asciimatics.screen import Screen as SC
    from asciimatics_overlay_ov import AsciiMaticsOverlayMain
    from asciimatics_overlay_ov.widgets import FrameNodes

    from ask_question.ask_question_tui import AskQuestionTUI

except ImportError:
    TUI_AVAILABLE = False

if TUI_AVAILABLE:
    def demo():
        """ This is the demo version of the asciimatics version of the program """
        print("Asciimatics demo is yet to come")
else:
    def demo():
        """ This is the demo code for the tty version of the program """
        AQI = AskQuestion({}, "")
        answer = AQI.ask_question("How old are you?", "uint")
        ADD_S = ""
        if isinstance(answer, int) and answer > 1:
            ADD_S = "s"
        print(f"You are {answer} year{ADD_S} old")
        answer = AQI.ask_question("Enter a ufloat:", "ufloat")
        print(f"You entered {answer}")
        AQI.pause()


if __name__ == "__main__":
    demo()
