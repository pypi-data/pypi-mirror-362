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

from string import printable
from typing import Union, Dict, List


class AskQuestion:
    """ An advanced function that contains boiling to gain time when asking a question """

    def __init__(self, human_type: Dict = {}, illegal_characters_nb: str = "", tui: bool = False) -> None:
        """ The globals for the class """
        self.human_type = human_type
        self.illegal_characters_nb = illegal_characters_nb
        self.author = "(c) Henry Letellier"
        self.in_tui = tui
        self.usr_answer: Union[str, int, float,  None, bool, List] = ""
        self.answer_was_found = True
        self.answer_was_not_found = False
        self.illegal_characters_found = False
        self._tui_key = "tui"
        self._message_key = "message"
        self._usr_answer_key = "user_answer"
        self._answer_found_key = "answer_found"
        self.check_load()

    def check_load(self) -> None:
        """ Check that the ressources are present """
        if isinstance(self.human_type, dict) is False or len(self.human_type) == 0:
            self.human_type = {
                "int": "whole number (-1, 0, 1, 2, 3, etc...)",
                "float": "floating number (-1.2, 0.1, 1.2, etc...)",
                "uint": "whole positive number (0, 1, 2, etc...)",
                "ufloat": "whole positive floating number (0.1, 1.2, etc ...)",
                "num": "numeric (numbers from 0 onwards)",
                "alnum": "alphanumeric (only numbers and the alphabet)",
                "alpha": "alphabet (from a to z and A to Z)",
                "char": "alphabet (from a to z and A to Z)",
                "ascii": "ascii Table",
                "str": "string (any character you can type)",
                "version": "version (numbers separated by '.' characters)",
                "ver": "version (numbers separated by '.' characters)",
                "bool": "boolean (yes/True/1 or no/False/0 answer type)",
                "up": "Convert the user input to uppercase",
                "low": "Convert the user input to lowercase"
            }
        if self.illegal_characters_nb == "":
            self.illegal_characters_nb = printable.replace("-", "")
            self.illegal_characters_nb = self.illegal_characters_nb.replace(
                ".",
                ""
            )
            self.illegal_characters_nb = self.illegal_characters_nb.replace(
                ",",
                ""
            )
            self.illegal_characters_nb = self.illegal_characters_nb.replace(
                "+",
                ""
            )
            self.illegal_characters_nb = self.illegal_characters_nb.replace(
                "0123456789",
                ""
            )

    def update_tui_status(self, tui: bool = False) -> None:
        """ Update the processing method used by the tui class """
        self.in_tui = tui

    def toggle_tui_status(self) -> bool:
        """ Change the status of the tui variable """
        if self.in_tui:
            self.in_tui = False
        else:
            self.in_tui = True
        return self.in_tui

    def get_tui_status(self) -> bool:
        """ Get the current status of the tui vairable """
        return self.in_tui

    def is_empty(self, string: str) -> bool:
        """ Check if the string is not empty """
        if len(string) == 0:
            return True
        return False

    def is_version(self, string: str) -> bool:
        """ Check if the given string is a version """
        string_length = len(string)-1
        for i in enumerate(string):
            if i[1].isdigit() is False:
                if i[0] == string_length and (i[1] == '.' or i[1] == ','):
                    return False
                if i[1] != "." and i[1] != ",":
                    return False
        return True

    def is_float(self, number: str) -> bool:
        """ Check if the given string is a float """
        try:
            float(number)
            return True
        except ValueError:
            return False

    def contains_illegal_characters(self, string: str, illegal_characters: str) -> bool:
        """ Check if there are no forbidden characters in a string destined to be converted to a number """
        for i in string:
            if i in illegal_characters:
                return True
        return False

    def remove_char_overflow(self, string: str, char: str, presence_tolerance: int = 1, case_sensitive: bool = False) -> str:
        """ Remove the number of times a specific character appears in a string after the allowed number of times """
        result = ""
        for i in string:
            if case_sensitive is False:
                if i.lower() == char:
                    if presence_tolerance > 0:
                        result += i
                        presence_tolerance -= 1
                else:
                    result += i
            else:
                if i == char:
                    if presence_tolerance > 0:
                        result += i
                        presence_tolerance -= 1
                else:
                    result += i
        return result

    def clean_number(self, string: str, char: str = ".", tolerance: int = 1, case_sensitive: bool = False) -> str:
        """ Remove content that should not be in a number input """
        if " " in string:
            string = string.replace(" ", "")
        if "," in string:
            string = string.replace(",", ".")
        if string.count(char) > tolerance:
            string = self.remove_char_overflow(
                string, char, tolerance, case_sensitive)
        return string

    def _display_accordingly(self, usr_answer: str, message: str, answer_status: bool = True) -> Dict[str, Union[str, int, float, bool, List]]:
        """ Display the message depending on is_tui """
        if self.in_tui is True:
            return {
                self._tui_key: self.in_tui,
                self._message_key: message,
                self._usr_answer_key: usr_answer,
                self._answer_found_key: answer_status
            }
        print(message)
        return {
            self._tui_key: self.in_tui,
            self._message_key: message,
            self._usr_answer_key: usr_answer,
            self._answer_found_key: answer_status
        }

    def _process_isint(self, input_answer: str, answer_type: str) -> bool:
        """ Process the uint data """
        if (answer_type == "int" or answer_type == "isint") and not ("uint" in answer_type or "isuint" in answer_type) and self.illegal_characters_found is False:
            input_answer = self.clean_number(input_answer, ".", 0, False)
            input_answer = self.remove_char_overflow(
                input_answer, "-", 1, False)
            try:
                self.usr_answer = int(input_answer)
                return self.answer_was_found
            except TypeError:
                self.usr_answer = ""
                return self.answer_was_not_found
            except BaseException:
                self.usr_answer = ""
                return self.answer_was_not_found
        return self.answer_was_not_found

    def _process_isfloat(self, input_answer: str, answer_type: str) -> bool:
        """ Process the float data """
        if ("isfloat" in answer_type or "float" in answer_type) and not ("isufloat" in answer_type or "ufloat" in answer_type) and self.illegal_characters_found is False:
            input_answer = self.clean_number(input_answer, ".", 1, False)
            input_answer = self.remove_char_overflow(
                input_answer,
                "-",
                1,
                False
            )
            try:
                self.usr_answer = float(input_answer)
                return self.answer_was_found
            except TypeError:
                self.usr_answer = ""
                return self.answer_was_not_found
            except BaseException:
                self.usr_answer = input_answer
                return self.answer_was_not_found
        return self.answer_was_not_found

    def _process_isuint(self, input_answer: str, answer_type: str) -> bool:
        """ Process the uint data """
        if input_answer.isdigit() is True and ("isuint" in answer_type or "uint" in answer_type):
            self.usr_answer = int(input_answer)
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_isufloat(self, input_answer: str, answer_type: str) -> bool:
        """ Process the ufloat data """
        if self.is_float(input_answer) is True and ("isufloat" in answer_type or "ufloat" in answer_type):
            if len(input_answer) > 0 and input_answer[0] != "-":
                self.usr_answer = float(input_answer)
                return self.answer_was_found
            return self.answer_was_not_found
        return self.answer_was_not_found

    def _process_isnum(self, input_answer: str, answer_type: str) -> bool:
        """ Process the isnum data """
        if input_answer.isdigit() is True and ("isnum" in answer_type or "num" in answer_type):
            self.usr_answer = float(input_answer)
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_isalnum(self, input_answer: str, answer_type: str) -> bool:
        """ Process the isalnum data """
        if input_answer.isalnum() is True and ("isalnum" in answer_type or "alnum" in answer_type):
            self.usr_answer = input_answer
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_isalpha(self, input_answer: str, answer_type: str) -> bool:
        """ Process the isalpha data """
        if input_answer.isalpha() is True and ("isalpha" in answer_type or "alpha" in answer_type):
            self.usr_answer = input_answer
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_ischar(self, input_answer: str, answer_type: str) -> bool:
        """ Process the char data """
        if input_answer.isalpha() is True and ("ischar" in answer_type or "char" in answer_type):
            self.usr_answer = input_answer
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_isascii(self, input_answer: str, answer_type: str) -> bool:
        """ Process the isascii data """
        if input_answer.isascii() is True and ("isascii" in answer_type or "ascii" in answer_type):
            self.usr_answer = input_answer
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_isstr(self, input_answer: str, answer_type: str) -> bool:
        """ Process the isstr data """
        if ("isstr" in answer_type or "str" in answer_type) and isinstance(input_answer, str) is True:
            for i in input_answer:
                if i not in printable:
                    return self.answer_was_not_found
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_isversion(self, input_answer: str, answer_type: str) -> bool:
        """ Process the version data """
        if self.is_version(input_answer) is True and ("isversion" in answer_type or "version" in answer_type or "isver" in answer_type or "ver" in answer_type):
            self.usr_answer = input_answer
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_isbool(self, input_answer: str, answer_type: str) -> bool:
        """ Process the bool data """
        if ("isbool" in answer_type or "bool" in answer_type):
            input_answer = input_answer.lower()
            if "y" in input_answer or "t" in input_answer or "1" in input_answer:
                self.usr_answer = True
                return self.answer_was_found
            if "n" in input_answer or "f" in input_answer or "0" in input_answer:
                self.usr_answer = False
                return self.answer_was_found
            self.usr_answer = None
            return self.answer_was_not_found
        return self.answer_was_not_found

    def _process_to_up(self, input_answer: str, answer_type: str) -> bool:
        """ Process the to up data """
        if "up" in answer_type:
            self.usr_answer = input_answer.upper()
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_to_low(self, input_answer: str, answer_type: str) -> bool:
        """ Process the to low data """
        if "low" in answer_type:
            self.usr_answer = input_answer.lower()
            return self.answer_was_found
        return self.answer_was_not_found

    def _first_chunk(self, input_answer: str, answer_type: str) -> bool:
        """ The second chunk in charge of checking the inputted data """
        if self._process_isint(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_isfloat(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_isuint(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_isufloat(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_isnum(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        return self.answer_was_not_found

    def _second_chunk(self, input_answer: str, answer_type: str) -> bool:
        """ The second chunk in charge of checking the inputted data """
        if self._process_to_low(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_isalnum(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_isalpha(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_ischar(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_isascii(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        return self.answer_was_not_found

    def _third_chunk(self, input_answer: str, answer_type: str) -> bool:
        """ The third chunk in charge of checking the inputted data """
        if self._process_isstr(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_isversion(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_isbool(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_to_up(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_to_low(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        return self.answer_was_not_found

    def test_input(self, input_answer: str, answer_type: str) -> Dict[str, Union[str, int, float, bool, List]]:
        """ The function in charge of ensuring that the user's response corresponds to the programmer's expectations """
        answer_type_cleaned = answer_type\
            .replace("is", "", 1)\
            .replace("is_", "", 1)\
            .replace("is ", "", 1)
        if self.is_empty(input_answer) is False and input_answer.isspace() is False and input_answer.isprintable() is True:
            self.illegal_characters_found = self.contains_illegal_characters(
                input_answer,
                self.illegal_characters_nb
            )
            status1 = self._first_chunk(input_answer, answer_type_cleaned)
            if status1 == self.answer_was_found:
                return self._display_accordingly(input_answer, "", self.answer_was_found)
            status2 = self._second_chunk(input_answer, answer_type_cleaned)
            if status2 == self.answer_was_found:
                return self._display_accordingly(input_answer, "", self.answer_was_found)
            status3 = self._third_chunk(input_answer, answer_type_cleaned)
            if status3 == self.answer_was_found:
                return self._display_accordingly(input_answer, "", self.answer_was_found)
            self.usr_answer = ""
            response = "Please enter a response of type '"
            if answer_type_cleaned in self.human_type:
                response += f"{self.human_type[answer_type_cleaned]}'"
            else:
                response += "Unknown demanded type"
            return self._display_accordingly(input_answer, response, self.answer_was_not_found)
        self.usr_answer = ""
        response = "Response must not be empty or only contain spaces or any non visible character."
        return self._display_accordingly(input_answer, response, self.answer_was_not_found)

    def ask_question(self, question: str, answer_type: str) -> Union[str, int, float, bool]:
        """ Ask a question and continue asking until type met """
        answer_found = False
        usr_answer = ""
        self.usr_answer = ""
        while answer_found != self.answer_was_found:
            usr_answer = input(str(question))
            answer_found: Union[bool, Dict] = self.test_input(
                usr_answer,
                answer_type
            )
            if isinstance(answer_found, dict):
                if answer_found[self._answer_found_key] is False:
                    print(answer_found[self._message_key])
                answer_found = answer_found[self._answer_found_key]
        return self.usr_answer

    def pause(self, pause_message: str = "Press enter to continue...") -> None:
        """ Act like the windows batch pause function """
        empty = ""
        pause_response = input(pause_message)
        empty += pause_response


if __name__ == "__main__":
    AQI = AskQuestion({}, "", tui=True)
    answer = AQI.ask_question("How old are you?", "uint")
    ADD_S = ""
    if isinstance(answer, int) and answer > 1:
        ADD_S = "s"
    print(f"You are {answer} year{ADD_S} old")
    answer = AQI.ask_question("Enter a ufloat:", "ufloat")
    print(f"You entered {answer}")
    AQI.pause()
