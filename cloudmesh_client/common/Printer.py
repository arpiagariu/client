"""Convenient methods and classes to print tables"""
from __future__ import print_function

import json

from prettytable import PrettyTable
import yaml
from cloudmesh_client.util import convert_from_unicode
from pprint import pprint
from cloudmesh_client.shell.console import Console

class Printer (object):

    @classmethod
    def write(cls,   table,
                     order=None,
                     header=None,
                     output="table",
                     sort_keys=True,
                     show_none="",
                     key="name"):
        if type(table) == dict:
            return cls.list(table, order=order, header=header, output=output,
                            sort_keys=sort_keys, show_none=show_none, key=key)

        elif type(table) == list:

            return cls.list(table,
                            order=order, header=header, output=output,
                            sort_keys=sort_keys, show_none=show_none, key=key)
        else:
            Console.error("unkown type")

    @classmethod
    def list(cls,
                     l,
                     order=None,
                     header=None,
                     output="table",
                     sort_keys=True,
                     show_none="",
                     key="name"):
        """
        :param l: l is a lsit not a dict
        :param order:
        :param header:
        :param output:
        :param sort_keys:
        :param show_none:
        :param key:
        :return:
        """
        d = {}
        count = 0
        for entry in l:
            name = str(count)
            d[name] = entry
            count += 1
        return cls.dict(d,
                        order=order,
                        header=header,
                        sort_keys=sort_keys,
                        output=output,
                        show_none=show_none)


    @classmethod
    def dict(cls,
             d,
             order=None,
             header=None,
             output="table",
             sort_keys=True,
             show_none=""):
        """
        TODO
        :param d: A a dict with dicts of the same type.
        :type d: dict
        :param order:The order in which the columns are printed.
                    The order is specified by the key names of the dict.
        :type order:
        :param header: The Header of each of the columns
        :type header: list or tuple of field names
        :param output: type of output (table, csv, json, yaml or dict)
        :type output: string
        :param sort_keys:
        :type sort_keys: bool
        :return:
        """
        if output == "table":
            if d == {}:
                return None
            else:
                return cls.dict_table(d,
                                      order=order,
                                      header=header,
                                      sort_keys=sort_keys)
        elif output == "csv":
            return cls.csv(d,
                           order=order,
                           header=header,
                           sort_keys=sort_keys)
        elif output == "json":
            return json.dumps(d, sort_keys=sort_keys, indent=4)
        elif output == "yaml":
            return yaml.dump(convert_from_unicode(d), default_flow_style=False)
        elif output == "dict":
            return d
        else:
            return "UNKOWN FORMAT. Please use table, csv, json, yaml, dict."


    @classmethod
    def csv(cls,
            d,
            order=None,
            header=None,
            sort_keys=True):
        """
        prints a table in csv format

        :param d: A a dict with dicts of the same type.
        :type d: dict
        :param order:The order in which the columns are printed.
                    The order is specified by the key names of the dict.
        :type order:
        :param header: The Header of each of the columns
        :type header: list or tuple of field names
        :param sort_keys: TODO: not yet implemented
        :type sort_keys: bool
        :return: a string representing the table in csv format
        """
        first_element = list(d)[0]

        def _keys():
            return list(d[first_element])

        # noinspection PyBroadException
        def _get(element, key):
            try:
                tmp = str(d[element][key])
            except:
                tmp = ' '
            return tmp

        if d is None or d == {}:
            return None

        if order is None:
            order = _keys()

        if header is None and order is not None:
            header = order
        elif header is None:
            header = _keys()

        table = ""
        content = []
        for attribute in order:
            content.append(attribute)
        table = table + ",".join([str(e) for e in content]) + "\n"

        for job in d:
            content = []
            for attribute in order:
                try:
                    content.append(d[job][attribute])
                except:
                    content.append("None")
            table = table + ",".join([str(e) for e in content]) + "\n"
        return table

    @classmethod
    def dict_table(cls,
                   d,
                   order=None,
                   header=None,
                   sort_keys=True,
                   show_none="",
                   max_width=40):
        """prints a pretty table from an dict of dicts
        :param d: A a dict with dicts of the same type.
                      Each key will be a column
        :param order: The order in which the columns are printed.
                      The order is specified by the key names of the dict.
        :param header:  The Header of each of the columns
        :type header:   A list of string
        :param sort_keys:   Key(s) of the dict to be used for sorting.
                            This specify the column(s) in the table for sorting.
        :type sort_keys:    string or a tuple of string (for sorting with multiple columns)
        """

        def _keys():
            all_keys = []
            for e in d:
                keys = d[e].keys()
                all_keys.extend(keys)
            return list(set(all_keys))

        # noinspection PyBroadException
        def _get(item, key):
            try:
                tmp = str(d[item][key])
                if tmp == "None":
                    tmp = show_none
            except:
                tmp = ' '
            return tmp

        if d is None or d == {}:
            return None

        if order is None:
            order = _keys()

        if header is None and order is not None:
            header = order
        elif header is None:
            header = _keys()

        x = PrettyTable(header)
        x.max_width = max_width

        if sort_keys:
            if type(sort_keys) is str:
                sorted_list = sorted(d, key = lambda x: d[x][sort_keys])
            elif type(sort_keys) == tuple:
                sorted_list = sorted(d, key = lambda x: tuple([d[x][sort_key] for sort_key in sort_keys]))
            else:
                sorted_list = d
        else:
            sorted_list = d

        for element in sorted_list:
            values = []
            for key in order:
                values.append(_get(element, key))
            x.add_row(values)
        x.align = "l"
        #    if "node;ist" in header:
        #    x.max_width["nodelist"] = 25
        return x

    @classmethod
    def attribute(cls,
                  d,
                  header=None,
                  sort_keys=True,
                  output="table"):
        if header is None:
            header = ["Attribute", "Value"]
        if output == "table":
            x = PrettyTable(header)
            if sort_keys:
                sorted_list = sorted(list(d))
            else:
                sorted_list = list(d)

            for key in sorted_list:
                x.add_row([key, d[key] or ""])
            x.align = "l"
            return x
        else:
            return cls.dict({output: d}, output=output)

    @classmethod
    def print_list(cls, l, output='table'):
        def dict_from_list(l):
            d = dict([(idx, item) for idx, item in enumerate(l)])
            return d

        if output == 'table':
            x = PrettyTable(["Index", "Host"])
            for (idx, item) in enumerate(l):
                x.add_row([idx, item])
            x.align = "l"
            x.align["Index"] = "r"
            return x
        elif output == 'csv':
            return ",".join(l)
        elif output == 'dict':
            d = dict_from_list(l)
            return d
        elif output == 'json':
            d = dict_from_list(l)
            result = json.dumps(d, indent=4)
            return result
        elif output == 'yaml':
            d = dict_from_list(l)
            result = yaml.dump(d, default_flow_style=False)
            return result
        elif output == 'txt':
            return "\n".join(l)

    @classmethod
    def row_table(cls, d, order=None, labels=None):
        """prints a pretty table from data in the dict.
        :param d: A dict to be printed
        :param order: The order in which the columns are printed.
                      The order is specified by the key names of the dict.
        """
        # header
        header = list(d)
        x = PrettyTable(labels)
        if order is None:
            order = header
        for key in order:
            value = d[key]
            if type(value) == list:
                x.add_row([key, value[0]])
                for element in value[1:]:
                    x.add_row(["", element])
            elif type(value) == dict:
                value_keys = list(value)
                first_key = value_keys[0]
                rest_keys = value_keys[1:]
                x.add_row([key, "{0} : {1}".format(first_key, value[first_key])])
                for element in rest_keys:
                    x.add_row(["", "{0} : {1}".format(element, value[element])])
            else:
                x.add_row([key, value])

        x.align = "l"
        return x
