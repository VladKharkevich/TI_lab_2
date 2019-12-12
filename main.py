from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.properties import (
    ObjectProperty, StringProperty, DictProperty, BooleanProperty)
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserIconView
from methods import *
import os


class Container(BoxLayout):

    def start(self):
        try:
            self.output_key.text = ''
            self.output_text.text = ''
            self.input_text.text = ''
            filename = self.input_file_name.text
            with open(filename, 'rb') as f:
                input_text = f.read()
            if self.type_of_code.text == 'LFSR':
                key = ''
                for letter in self.key.text:
                    if letter == '0' or letter == '1':
                        key += letter
                if len(key) != 29 or len(self.key.text) != 29:
                    raise ValueError
                arr_key = lfsr(self.input_file_name.text,
                               int(key, 2))
                if filename[len(filename) - 4:] == '.cph':
                    filetemp = filename[:(len(filename) - 4)]
                    file_out = open(filetemp, 'rb')
                else:
                    file_out = open(filename + '.cph', 'rb')
                for i in range(min(len(arr_key), 32)):
                    temp = str(bin(input_text[i]))[2:]
                    temp = '0' * (8 - len(temp)) + temp
                    self.input_text.text += temp
                    temp = str(bin(arr_key[i]))[2:]
                    temp = '0' * (8 - len(temp)) + temp
                    self.output_key.text += temp
                    chunk = file_out.read(1)
                    temp = str(bin(chunk[0]))[2:]
                    temp = '0' * (8 - len(temp)) + temp
                    self.output_text.text += temp
            else:
                if not self.check_rc4_key(self.key.text):
                    raise ValueError
                arr_key = RC4(self.input_file_name.text,
                              self.key.text)
                if filename[len(filename) - 5:] == '.cphr':
                    filetemp = filename[:(len(filename) - 5)]
                    file_out = open(filetemp, 'rb')
                else:
                    file_out = open(filename + '.cphr', 'rb')
                for i in range(min(len(arr_key), 32)):
                    self.input_text.text += str(input_text[i]) + ' '
                    self.output_key.text += str(arr_key[i]) + ' '
                    chunk = file_out.read(1)
                    self.output_text.text += str(chunk[0]) + ' '
            file_out.close()

        except ValueError:
            self.lbl_error_key.color = (1, 0, 0, 1)
        except FileNotFoundError:
            self.lbl_error_file.color = (1, 0, 0, 1)

    def change_text(self):
        if self.type_of_code.text == 'LFSR':
            temp = 0
            for letter in self.key.text:
                if letter == '0' or letter == '1':
                    temp += 1
            self.lbl_len.text = '(%d из 29)' % temp
            self.lbl_register.text = 'Начальное состояние регистра'
        else:
            self.lbl_len.text = '%d' % len(self.key.text)
            self.lbl_register.text = 'Начальный ключ:'

    @staticmethod
    def check_rc4_key(key):
        if len(key) == 0:
            return False
        key = key.split(' ')
        for elem in key:
            if not elem.isdigit():
                return False
            if not (0 <= int(elem) < 256):
                return False
        return True


class InputKey(TextInput):
    pass


class MethodSpinner(Spinner):

    active_method = StringProperty('LFSR')

    def clean_input(self):
        root = App.get_running_app().root.get_screen('main').container
        if self.active_method != self.text:
            self.active_method = self.text
            root.key.text = ''
            root.output_key.text = ''
            root.output_text.text = ''
            root.input_file_name.text = ''
            root.input_text.text = ''
        if self.active_method == 'LFSR':
            root.lbl_len.text = '(%d из 29)' % len(root.key.text)
            root.lbl_register.text = 'Начальное состояние регистра'
        else:
            root.lbl_len.text = '%d' % len(root.key.text)
            root.lbl_register.text = 'Начальный ключ:'


class MainScreen(Screen):
    pass


class FileChooserScreen(Screen):
    pass


class BtnOpenFile(Button):

    def get_path(self):
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests/')


class ChoosingFile(FileChooserIconView):

    def fill_text(self):
        self._update_files()
        root = App.get_running_app().root
        root.current = 'main'
        if self.selection != []:
            print(self.selection)
            root.get_screen('main').container.input_file_name.text = (
                self.selection[0].replace('tests/', '', 1))


class MyApp(App):

    def build(self):
        sm = ScreenManager()
        self.sm = sm
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(FileChooserScreen(name='filechooser'))
        return self.sm


if __name__ == '__main__':
    MyApp().run()
