import datetime
import time
from enum import Enum, auto
from typing import Optional

from robot.api.deco import keyword
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import faker


class NS_Common_Keywords(object):

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "ROBOT"
    ROBOT_EXIT_ON_FAILURE = True

    SLEEP_TIME = 0.05

    def __init__(self) -> None:
        self.builtin = BuiltIn()

    @keyword('Selecteer Waarde In Combobox')
    def selecteer_waarde_in_combobox(self, xpath: str, value: str) -> None:
        """
        Selects a value in a combobox by clicking, typing the value, and pressing Enter.

        Args:
            xpath (str): The xpath to the combobox element.
            value (str): The value to select.
        """
        browser_lib = self.builtin.get_library_instance('Browser')
        browser_lib.click(f'{xpath}')
        logger.info(f"Type van xpath: {type(xpath)}, waarde: {xpath}")
        logger.info(f"Type van value: {type(value)}, waarde: {value}")
        browser_lib.type_text(f'{xpath}', f'{value}', delay=0.01)
        logger.info(f"typen klaar.. op naar enter")
        name = self.creeer_willekeurig_woord()
        logger.info(f"Naam voor screenshot: {name}")
        browser_lib.take_screenshot()
        browser_lib.keyboard_key(KeyAction.press, "Enter")

    @keyword('Selecteer Waarde In Multiselect Combobox')
    def selecteer_waarde_in_multiselect_combobox(self, xpath: str, value: str) -> None:
        """
        Selects a value in a multiselect combobox by clicking, typing, and using keyboard navigation.

        Args:
            xpath (str): The xpath to the multiselect combobox element.
            value (str): The value to select.
        """
        browser_lib = self.builtin.get_library_instance('Browser')
        browser_lib.click(f'{xpath}')
        time.sleep(0.1)
        browser_lib.type_text(f'{xpath}', f'{value}')
        time.sleep(0.1)
        browser_lib.keyboard_key(KeyAction.press, "ArrowDown")
        time.sleep(0.1)
        browser_lib.keyboard_key(KeyAction.press, "Enter")
        time.sleep(0.1)
        browser_lib.keyboard_key(KeyAction.press, "Tab")
        browser_lib.keyboard_key(KeyAction.press, "Tab")

    @keyword('Get Modal Container')
    def get_modal_container(self, title: str):
        """
        Returns the modal container element for a given modal title.

        Args:
            title (str): The title of the modal dialog.
        Returns:
            The modal container element.
        """
        browser_lib = self.builtin.get_library_instance('Browser')
        xpath = f'//h4[contains(text(),"{title}")]/ancestor::div[contains(@class, "modal-dialog")]'
        return browser_lib.get_element(xpath)

    @keyword('Close Modal')
    def close_modal(self, title: str, action: str) -> None:
        """
        Closes a modal dialog by clicking the specified action button and waits until it is invisible.

        Args:
            title (str): The title of the modal dialog.
            action (str): The button text to click for closing.
        """
        browser_lib = self.builtin.get_library_instance('Browser')
        container = self.get_modal_container(title)
        browser_lib.click(f'{container}//button[text()="{action}"]')
        self.wacht_tot_element_onzichtbaar_is(container)

    @keyword('Wait For Modal')
    def wait_for_modal(self, title: str) -> None:
        """
        Waits until a modal dialog with the given title is visible.

        Args:
            title (str): The title of the modal dialog.
        """
        browser_lib = self.builtin.get_library_instance('Browser')
        xpath = f'//h4[contains(text(),"{title}")]/ancestor::div[contains(@class, "modal-dialog")]'
        browser_lib.wait_for_elements_state(xpath, ElementState.visible)

    @keyword('Dismiss Modal')
    def dismiss_modal(self, title: str) -> None:
        """
        Dismisses a modal dialog by clicking the close button in the header.

        Args:
            title (str): The title of the modal dialog.
        """
        self.close_modal(title, '.modal-header > .close')

    @keyword('Pas Format Aan Van Datum')
    def pas_format_aan_van_datum(self, datum: str, input_format: str = '%d-%m-%Y', output_format: str = '%Y-%m-%d') -> str:
        """
        Converts a date string from one format to another.

        Args:
            datum (str): The date string to convert.
            input_format (str): The format of the input date string.
            output_format (str): The desired output format.
        Returns:
            str: The formatted date string.
        """
        return datetime.datetime.strptime(datum, input_format).strftime(output_format)

    @keyword('Bepaal Huidige Datum')
    def bepaal_huidige_datum(self, format: str = '%d-%m-%Y') -> str:
        """
        Returns the current date as a string in the specified format.

        Args:
            format (str): The desired date format.
        Returns:
            str: The current date as a string.
        """
        return datetime.datetime.now().strftime(format)

    @keyword('Bepaal Datum Plus Extra Dagen')
    def bepaal_datum_plus_extra_dagen(self, aantal_dagen: int, begin_datum: Optional[str] = None, format: str = '%d-%m-%Y') -> str:
        """
        Returns a date string for a date that is a number of days after a given start date.

        Args:
            aantal_dagen (int): Number of days to add.
            begin_datum (Optional[str]): The start date string. If None, uses today.
            format (str): The desired date format.
        Returns:
            str: The calculated date as a string.
        """
        if begin_datum:
            start = datetime.datetime.strptime(begin_datum, format)
        else:
            start = datetime.datetime.now()
        nieuwe_datum = start + datetime.timedelta(days=int(aantal_dagen))
        return nieuwe_datum.strftime(format)

    @keyword('Creeer Willekeurige Zin')
    def creeer_willekeurige_zin(self) -> str:
        """
        Generates a random Dutch sentence with 8 words.

        Returns:
            str: The generated sentence.
        """
        fake = faker.Faker('nl_NL')
        return fake.sentence(nb_words=8)

    @keyword('Creeer Willekeurig Woord')
    def creeer_willekeurig_woord(self, min_length: int = 5) -> str:
        """
        Generates a random French word with at least min_length characters.

        Args:
            min_length (int): Minimum length of the generated word (default: 5).
        Returns:
            str: The generated word.
        """
        fake = faker.Faker('fr_FR')
        word = fake.word()
        while len(word) < min_length:
            word = fake.word()
        return word

    @keyword('Wacht Tot Element Onzichtbaar Is')
    def wacht_tot_element_onzichtbaar_is(self, xpath: str) -> None:
        """
        Waits until the element at the given xpath is no longer visible, or times out after 100 tries.

        Args:
            xpath (str): The xpath to the element.
        Raises:
            TimeoutError: If the element is still visible after 100 tries.
        """
        browser_lib = self.builtin.get_library_instance('Browser')
        count = browser_lib.get_element_count(f'{xpath}')
        tries = 0
        while count and tries < 100:
            time.sleep(self.SLEEP_TIME)
            count = browser_lib.get_element_count(f'{xpath}')
            logger.info(f"Poging {tries + 1}: element met xpath '{xpath}' is nog steeds zichtbaar.")
            tries += 1
        if count:
            raise TimeoutError(f"Element met xpath '{xpath}' is na 100 pogingen nog steeds zichtbaar.")

    @keyword('Wacht Op Laden Element')
    def wacht_op_laden_element(self, xpath: str, state: str = 'visible', wachttijd: str = '10s') -> None:
        """
        Waits for an element to reach a specific state (e.g., visible, hidden) within a timeout.

        Args:
            xpath (str): The xpath to the element.
            state (str): The desired state (default 'visible').
            wachttijd (str): The timeout duration (default '10s').
        Raises:
            AttributeError: If the Browser library does not support wait_for_elements_state.
            ValueError: If the state is not valid.
            Exception: If waiting fails for another reason.
        """
        browser_lib = self.builtin.get_library_instance('Browser')

        # Probeer de Browser library state enums te gebruiken
        try:
            state_mapping = {
                'attached': ElementState.attached,
                'detached': ElementState.detached,
                'visible': ElementState.visible,
                'hidden': ElementState.hidden,
                'enabled': ElementState.enabled,
                'disabled': ElementState.disabled,
                'editable': ElementState.editable
            }
        except ImportError:
            # Fallback naar string waarden
            logger.info("ElementState enum niet beschikbaar, gebruik string waarden")
            state_mapping = {
                "attached": "attached",
                "detached": "detached",
                "visible": "visible",
                "hidden": "hidden",
                "enabled": "enabled",
                "disabled": "disabled",
                "editable": "editable"
            }

        if state not in state_mapping:
            geldige_statussen = list(state_mapping.keys())
            raise ValueError(f"'{state}' is geen geldige state. Kies uit: {', '.join(geldige_statussen)}")

        # Gebruik de juiste state parameter
        try:
            browser_lib.wait_for_elements_state(f'{xpath}', state=state_mapping[state], timeout=wachttijd)
        except Exception as e:
            logger.error(f"❌ Fout bij wachten op element: {str(e)}")
            raise

    @keyword('Wacht Op Het Laden Van Een Tabel')
    def wacht_op_het_laden_van_een_tabel(self, xpath: str) -> None:
        """
        Waits until a table is loaded by checking for the presence of a paging-status div.

        Args:
            xpath (str): The xpath to the table element.
        Raises:
            TimeoutError: If the table is not loaded after 10 tries.
        """
        browser_lib = self.builtin.get_library_instance('Browser')
        aantal = 0
        tries = 0
        while not aantal and tries < 10:
            time.sleep(self.SLEEP_TIME)
            aantal = browser_lib.get_element_count(f'{xpath}//div[@class="paging-status"]')
            logger.info(f"Poging {tries + 1}: aantal regels in tabel is {aantal}")
            tries += 1
        if not aantal:
            raise TimeoutError(f"Tabel met xpath '{xpath}' is niet geladen na 10 pogingen.")

    @keyword('Tel Aantal Regels Van Tabel')
    def tel_aantal_regels_van_tabel(self, xpath: str) -> int:
        """
        Counts the number of rows in a table identified by the given xpath.

        Args:
            xpath (str): The xpath to the table element.
        Returns:
            int: The number of rows found.
        """
        browser_lib = self.builtin.get_library_instance('Browser')
        return browser_lib.get_element_count(f'{xpath}//div[@role="row"]')

    @keyword('Wacht Op Herladen Data Tabel')
    def wacht_op_herladen_data_tabel(self, xpath: str, aantal_regels: int) -> None:
        """
        Waits until the number of rows in the table changes, indicating data reload.

        Args:
            xpath (str): The xpath to the table element.
            aantal_regels (int): The initial number of rows to wait for a change from.
        Raises:
            TimeoutError: If the number of rows does not change after 20 tries.
        """
        nieuw_aantal = aantal_regels
        tries = 0
        while nieuw_aantal == aantal_regels and tries < 20:
            time.sleep(self.SLEEP_TIME)
            nieuw_aantal = self.tel_aantal_regels_van_tabel(f'{xpath}')
            logger.info(f"Poging {tries + 1}: aantal regels in tabel is nog {nieuw_aantal}")
            tries += 1
            if nieuw_aantal == 1:
                break
        if nieuw_aantal == aantal_regels and nieuw_aantal != 1:
            raise TimeoutError(f"Aantal regels in tabel met xpath '{xpath}' is niet veranderd na 20 pogingen.")

    @keyword('Formatteer Bedrag')
    def formatteer_bedrag(self, amount: float) -> str:
        """
        Formats a number as a Dutch currency string (e.g., 1234.56 -> '1.234,56').

        Args:
            amount (float): The amount to format.
        Returns:
            str: The formatted amount as a string.
        """
        return '{:,.2f}'.format(float(amount)).replace(',', 'X').replace('.', ',').replace('X', '.')

class ElementState(Enum):
    """Enum that defines the state an element can have.

    The following ``states`` are possible:
    | =State=        | =Description= |
    | ``attached``   | to be present in DOM. |
    | ``detached``   | to not be present in DOM. |
    | ``visible``    | to have non or empty bounding box and no visibility:hidden. |
    | ``hidden``     | to be detached from DOM, or have an empty bounding box or visibility:hidden. |
    | ``enabled``    | to not be ``disabled``. |
    | ``disabled``   | to be ``disabled``. Can be used on <button>, <fieldset>, <input>, <optgroup>, <option>, <select> and <textarea>. |
    | ``editable``   | to not be ``readOnly``. |
    | ``readonly``   | to be ``readOnly``. Can be used on <input> and <textarea>. |
    | ``selected``   | to be ``selected``. Can be used on <option>. |
    | ``deselected`` | to not be ``selected``. |
    | ``focused``    | to be the ``activeElement``. |
    | ``defocused``  | to not be the ``activeElement``. |
    | ``checked``    | to be ``checked``. Can be used on <input>. |
    | ``unchecked``  | to not be ``checked``. |
    | ``stable``     | to be both ``visible`` and ``stable``. |
    """

    attached = 1
    detached = 2
    visible = 4
    hidden = 8
    enabled = 16
    disabled = 32
    editable = 64
    readonly = 128
    selected = 256
    deselected = 512
    focused = 1024
    defocused = 2048
    checked = 4096
    unchecked = 8192
    stable = 16384

class KeyAction(Enum):
    """Enum that defines the action to be performed on a key.

    The following actions are possible:
    | =Action= | =Description= |
    | ``down`` | to press the key down. |
    | ``up``   | to release the key. |
    | ``press``| to press and release the key. |
    """
    down = auto()
    up = auto()
    press = auto()