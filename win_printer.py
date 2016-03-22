import os
import json
import subprocess

import requests
import win32
import win32api
import win32print


class WinPrinter:

    def __init__(self, printer_name=None, config_file_path=None,
                 tmp_location=None):
        if config_file_path is None:
            self.config_file_path = os.path.dirname(os.path.realpath(__file__))
            self.config_file_path += '\\config.json'
        else:
            self.config_file_path = config_file_path
        with open(self.config_file_path, 'r') as config_file:
            config = json.load(config_file, strict=False)
        self.ghost_script_path = config['win_printer']['ghost_script_path']
        self.gs_print_path = config['win_printer']['gs_print_path']
        if printer_name is None:
            self.printer_name = win32print.GetDefaultPrinter()
        else:
            self.printer_name = printer_name
        if tmp_location is None:
            self.tmp_location = config['win_printer']['tmp_location']
        else:
            self.tmp_location = tmp_location
        self.tmp_path = self.tmp_location + 'win_print_tmp_file'

    def print_file(self, filepath):
        command = '"' + self.gs_print_path + '" -ghostscript '
        command += '"' + self.ghost_script_path
        command += '" -printer "' + self.printer_name
        command += '" "' + filepath + '"'
        try:
            call_response = subprocess.run(command, shell=True, check=True)
        except:
            return self.print_failed(command)
        return self.print_success(command)

    def print_failed(self, command):
        print(command)
        print("FAILED")
        return False

    def print_success(self, command):
        return True

    def print_url(self, url):
        response = requests.get(url)
        response.raise_for_status()
        with open(self.tmp_path, 'wb') as tmp_file:
            tmp_file.write(response.content)
        self.print_file(self.tmp_path)
