##
# EPITECH PROJECT, 2022
# Desktop_pet (Workspace)
# File description:
# ask_question.py
##

"""
The file containing the code to speed up the boiling
process that occurs when a question is asked.
This module is provided as if and without any warranty
Crediting the author is appreciated.
"""

__Author__ = "(c) Henry Letellier"

from typing import Union, Dict

from ask_question import Ask_Question as AskQuestionAnswerProcessing

try:
    import asciimatics.widgets as WIG
    from asciimatics.event import Event
    from asciimatics import screen as SC
    from asciimatics_overlay_ov.widgets import FrameNodes
    from asciimatics_overlay_ov import AsciiMaticsOverlayMain
except ImportError as exc:
    raise ImportError(
        "Class AskQuestionTUI requires matplotlib. Install with `pip install ask_question[tui]`."
    ) from exc


class AskQuestionTUIManagement(WIG.Frame, AsciiMaticsOverlayMain, FrameNodes):
    """ The class in charge of managing the TUI """

    def __init__(self, screen: SC, ask_question_answer_processing: AskQuestionAnswerProcessing, question: str, answer_type: str, screen_width: int, screen_height: int, screen_offset_x: int, screen_offset_y: int) -> None:
        """ The globals for the class """
        final_screen_width = self._recalculate_screen_width(
            screen.width,
            screen_width,
            screen_offset_x
        )
        final_screen_height = self._recalculate_screen_height(
            screen.height,
            screen_height,
            screen_offset_y
        )

        super(AskQuestionTUIManagement, self).__init__(
            screen,
            final_screen_height,
            final_screen_width,
            has_border=True,
            title="Ask question (TUI version)"
        )
        self.__version__ = "1.0.0"
        self.author = "(c) Henry Letellier"
        self.version = self.__version__
        self.question = question
        self.answer_type = answer_type
        self.screen = screen
        self.usr_answer = ""
        self.error_message = ""
        self.textbox_widget = None
        self.error_message_widget = None
        self.user_has_decided_to_quit = False
        self.run_status = self.success

        self.asciimatics_overlay = AsciiMaticsOverlayMain(Event, screen)
        self.frame_node = FrameNodes()
        self.ask_question_answer_processing = ask_question_answer_processing

        # Define a layout with three columns
        self.layout = WIG.Layout([100], fill_frame=True)
        self.add_layout(self.layout)
        self.layout_buttons = WIG.Layout([25, 25, 25, 25], fill_frame=False)
        self.add_layout(self.layout_buttons)
        self.place_content_on_screen()
        self.fix()

    def _recalculate_screen_height(self, screen_height: int, usr_screen_height: int, usr_screen_offset: int) -> int:
        """ Recalculate the screen size """
        default_screen_height = screen_height
        if usr_screen_height > 0 and usr_screen_height < default_screen_height:
            screen_height = usr_screen_height
        if usr_screen_offset > 0 and usr_screen_offset < default_screen_height:
            screen_height += usr_screen_offset
        return screen_height

    def _recalculate_screen_width(self, screen_width: int, usr_screen_width: int, usr_screen_offset: int) -> int:
        """ Recalculate the screen width """
        default_screen_width = screen_width
        if usr_screen_width > 0 and usr_screen_width < default_screen_width:
            screen_width = usr_screen_width
        if usr_screen_offset > 0 and usr_screen_offset < default_screen_width:
            screen_width += usr_screen_offset
        return screen_width

    def place_content_on_screen(self) -> None:
        """ Place the required assets on the screen for the user to interact """
        self.textbox_widget = self.add_textbox(
            height=5,
            label=self.question,
            name="usr_input",
            as_string=True,
            line_wrap=True,
            on_change=self._reset_error_message,
            readonly=False
        )
        self.error_message_widget = self.add_label(
            text=self.error_message,
            height=2,
            align=self.label_center,
            name="error_message"
        )
        self.layout.add_widget(self.textbox_widget, 0)
        self.layout.add_widget(self.error_message_widget, 0)
        self.layout_buttons.add_widget(
            self.add_button(
                text="Submit",
                on_click=self._submit,
                name=None
            ),
            1
        )
        self.layout_buttons.add_widget(
            self.add_button(
                text="Cancel",
                on_click=self._exit,
                name=None
            ),
            2
        )

    def _reset_error_message(self) -> None:
        """ Reset the error message """
        self.error_message = ""
        self.apply_text_to_display(
            self.error_message_widget, self.error_message)

    def _check_usr_input(self) -> Union[str, int, float, bool]:
        """ Check the input provided by the user """
        usr_input = self.get_widget_value(self.textbox_widget)
        self.usr_answer = self.ask_question_answer_processing.test_input(
            usr_input, self.answer_type, is_tui=True)
        if isinstance(self.usr_answer, list) is True:
            self.apply_text_to_display(
                self.error_message_widget,
                self.usr_answer[1]
            )
            self.error_message = self.usr_answer[1]
            self.run_status = self.error
        else:
            self._reset_error_message()
            self.run_status = self.success
            return self.usr_answer

    def _submit(self) -> str:
        """ Submit the answer """
        self._check_usr_input()
        if isinstance(self.usr_answer, list) is True:
            self.usr_answer = self.usr_answer[0]
        self._exit()

    def _exit(self) -> None:
        """ Exit the Scene """
        self.usr_answer = ""
        self.user_has_decided_to_quit = True


class AskQuestionTUI:
    """ An advanced function that contains boiling to gain time when asking a question """

    def __init__(self, screen: SC, human_type: Dict = {}, illegal_characters_nb: str = "", screen_width: int = -1, screen_height: int = -1, screen_offset_x: int = 0, screen_offset_y: int = 0, tui_enabled: bool = True) -> None:
        """ The globals for the class """
        self.__version__ = "1.0.0"
        self.human_type = human_type
        self.illegal_characters_nb = illegal_characters_nb
        self.author = "(c) Henry Letellier"
        self.version = self.__version__
        self.usr_answer = ""
        self.answer_was_found = True
        self.answer_was_not_found = False
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_offset_x = screen_offset_x
        self.screen_offset_y = screen_offset_y
        self.user_has_decided_to_quit = False
        if tui_enabled is None:
            self.tui_enabled = True
        else:
            self.tui_enabled = tui_enabled
        self.ask_question_tui_management = None
        self.ask_question_answer_processing = AskQuestionAnswerProcessing(
            human_type=human_type,
            illegal_characters_nb=illegal_characters_nb
        )

    def ask_question_tty(self, question: str, answer_type: str) -> Union[str, int, float, bool]:
        """ Ask a question and continue asking until type met """
        answer_found = False
        usr_answer = ""
        self.usr_answer = ""
        while answer_found is False:
            usr_answer = input(str(question))
            answer_found = self.ask_question_answer_processing.test_input(
                usr_answer,
                answer_type,
                is_tui=False
            )
            if isinstance(answer_found, list) is True:
                answer_found = False
        self.usr_answer = self.ask_question_answer_processing.usr_answer
        return self.usr_answer

    def ask_question_tui(self, question: str, answer_type: str) -> Union[str, int, float, bool]:
        """ Display a graphical interface to ask the question """
        aqtuim = AskQuestionTUIManagement(
            screen=self.screen,
            ask_question_answer_processing=self.ask_question_answer_processing,
            question=question,
            answer_type=answer_type,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            screen_offset_x=self.screen_offset_x,
            screen_offset_y=self.screen_offset_y
        )
        self.usr_answer = aqtuim.usr_answer
        self.user_has_decided_to_quit = aqtuim.user_has_decided_to_quit
        return self.usr_answer

    def ask_question(self, question: str, answer_type: str, tui_enabled: bool = None) -> Union[str, int, float, bool]:
        """ Display a graphical or non-graphical question based on the input """
        if tui_enabled is None:
            tui_enabled = self.tui_enabled
        if tui_enabled is True:
            return self.ask_question_tui(question, answer_type)
        return self.ask_question_tty(question, answer_type)

    def pause(self, pause_message: str = "Press enter to continue...") -> None:
        """ Act like the windows batch pause function """
        empty = ""
        pause_response = input(pause_message)
        empty += pause_response


if __name__ == "__main__":
    AQI = AskQuestionTUI(dict(), "")
    answer = AQI.ask_question("How old are you?", "uint")
    ADD_S = ""
    if answer > 1:
        ADD_S = "s"
    print(f"You are {answer} year{ADD_S} old")
    answer = AQI.ask_question("Enter a ufloat:", "ufloat")
    print(f"You entered {answer}")
    AQI.pause()
