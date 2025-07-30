from __future__ import annotations
from typing import Dict, Type

import re
import urllib.parse


class Url:
    """
    Balderhub object to work with URLs.
    This object also supports schema parameters. You can define a schema parameter by using the following syntax:
    ``<int:var_name>``, while the first statement needs to be `int` for integer or `str` for strings. The second
    statement describes a variable name, that needs to start with an upper or lower case letter and can be followed by
    `_` or any digits.
    """

    #: regular expression schema parameter syntax
    RE_PARAMETER_STATEMENT = r'^<(int|str):([a-zA-Z_]+[a-zA-Z0-9_]+)>$'

    def __init__(self, url: str):
        if not isinstance(url, str):
            raise TypeError('url must be a string')
        self._url = url

    def __name__(self):
        return self._url

    def __str__(self):
        return self._url

    def __eq__(self, other: Url | str):
        """
        :param other: the other :class:`Url` instance (or url as string)
        :return: returns true in case the url objects are identically
        """
        other_as_str = other.as_string() if isinstance(other, Url) else other
        return self._url == other_as_str

    def __hash__(self):
        return hash(self._url)

    def get_urlparse(self) -> urllib.parse.ParseResult:
        """
        :return: returns the :class:`urllib.parse.ParseResult` of the url
        """
        return urllib.parse.urlparse(self.as_string())

    def as_string(self) -> str:
        """
        :return: returns the URL as a string
        """
        return self._url

    def is_schema(self):
        """
        :return: True in case this url is a schema (has internal unfilled parameters), otherwise False
        """
        return len(self.get_unfilled_parameters()) > 0

    def get_query_parameters(self) -> Dict[str, str]:
        """
        This method returns all query parameter that are mentioned in the url.
        :return: a list of all query parameter as a dictionary
        """
        query = self.get_urlparse().query
        if not query:
            return {}
        return {elem.split('=')[0]:elem.split('=')[1] for elem in query.split('&')}

    def get_unfilled_parameters(self)-> Dict[str, Type[int | str]]:
        """
        This method returns a dictionary with schema parameter names as key and the defined `Type[int]` or `Type[str]`
        as value.

        :return: returns the unfilled parameters as a dictionary
        """
        result = {}

        parsed_schema = self.get_urlparse()
        path_schema = parsed_schema.path.split('/')
        for part_in_schema in path_schema:
            # check if this part of the path is variable (int or string)
            match = re.match(self.RE_PARAMETER_STATEMENT, part_in_schema)
            if match:
                parameter_name = match.group(2)
                parse_method = int if match.group(1) == "int" else str
                result[parameter_name] = parse_method
        for cur_query_param in self.get_query_parameters().values():
            match = re.match(self.RE_PARAMETER_STATEMENT, cur_query_param)
            if match:
                parameter_name = match.group(2)
                parse_method = int if match.group(1) == "int" else str
                result[parameter_name] = parse_method
        return result

    def fill_parameters(self, **kwargs) -> Url:
        """
        This method allows to fill internal defined schema parameters. For that, you need to provide the parameter name
        as parameter and its value as value. This method will validate the typing before inserting any values.

        .. note::
            Please note, this object will not be changed. The method returns a new :class:`Url` instance with the
            filled schema parameters.

        :param kwargs: all schema parameters that should be filled
        :return: a new :class:`Url` instance with the filled parameters
        """
        remaining_parameter = kwargs.copy()
        parsed_schema = self.get_urlparse()
        path_schema = parsed_schema.path.split('/')
        for idx, part_in_schema in enumerate(path_schema):
            # check if this part of the path is variable (int or string)
            match = re.match(self.RE_PARAMETER_STATEMENT, part_in_schema)
            if match:
                parameter_name = match.group(2)
                path_schema[idx] = str(kwargs[parameter_name])
                del remaining_parameter[parameter_name]

        new_query_parts = []
        for cur_query_key, cur_query_param in self.get_query_parameters().items():
            match = re.match(self.RE_PARAMETER_STATEMENT, cur_query_param)
            if match:
                parameter_name = match.group(2)
                new_query_parts.append(f"{cur_query_key}={str(kwargs[parameter_name])}")
                del remaining_parameter[parameter_name]

        assert len(remaining_parameter) == 0, f"can not find parameter {remaining_parameter} in schema"
        return Url(parsed_schema._replace(path='/'.join(path_schema), query='&'.join(new_query_parts)).geturl())

    def extract_parameters(self, by_using_schema_url: Url) -> Dict[str, int | str]:
        """
        This method extracts the schema parameter values of that URL for the schema parameters from the provided schema
        URL.

        :param by_using_schema_url: the url that holds all the schema parameters that should be extracted
        :return: a dictionary with the schema parameter name as key and the schema parameter value as value
        """
        parameter = {}

        parsed_schema = by_using_schema_url.get_urlparse()
        parsed_url = self.get_urlparse()
        assert parsed_schema.scheme == parsed_url.scheme
        assert parsed_schema.netloc == parsed_url.netloc
        path_schema = parsed_schema.path.split('/')
        path_url = parsed_url.path.split('/')

        assert len(path_schema) == len(path_url)

        for part_in_schema, part_in_path in zip(path_schema, path_url):
            # check if this part of the path is variable (int or string)
            match = re.match(self.RE_PARAMETER_STATEMENT, part_in_schema)
            if match:
                parse_method = int if match.group(1) == "int" else str
                parameter[match.group(2)] = parse_method(part_in_path)
            else:
                assert part_in_schema == part_in_path

        # now also check GET parameters
        schema_query_params = by_using_schema_url.get_query_parameters()
        url_query_params = self.get_query_parameters()

        assert len(schema_query_params) == len(url_query_params)
        for key, val_in_schema in schema_query_params.items():
            if key not in url_query_params.keys():
                raise KeyError(f"key {key} not in url query")
            val_in_url = url_query_params[key]

            # check if this part of the path is variable (int or string)
            match = re.match(self.RE_PARAMETER_STATEMENT, val_in_schema)
            if match:
                parse_method = int if match.group(1) == "int" else str
                parameter[match.group(2)] = parse_method(val_in_url)
            else:
                assert val_in_schema == val_in_url

        return parameter

    def compare(self, other: Url | str, allow_schemas: bool = False) -> bool:
        """
        This method compares two :class:`Url` instances. If `allow_schemas` is `True`, it considers two urls as equal
        if the schema parameter description matches the schema parameter value of the other url.

        :param other: the other url
        :param allow_schemas: True if the method should match urls, in that one url holds a schema description and the
                              other holds a matching value for it, otherwise False
        :return: true in case that both urls are equal
        """
        other = other if isinstance(other, Url) else Url(other)

        if not allow_schemas and (self.is_schema() or other.is_schema()):
            raise ValueError('cannot compare urls because schemas are not allowed and at least one url is a schema')

        parsed_self = self.get_urlparse()
        parsed_other = other.get_urlparse()

        if parsed_self.scheme != parsed_other.scheme:
            return False
        if parsed_self.netloc != parsed_other.netloc:
            return False

        path_self = parsed_self.path.split('/')
        path_other = parsed_other.path.split('/')

        # check if path is similar in case of `allow_schemas=True`
        for part_in_self_path, part_in_other_path in zip(path_self, path_other):

            # first check if both are the same
            if part_in_self_path == part_in_other_path:
                continue

            # check if one side is variable (int or string)
            match_self = re.match(self.RE_PARAMETER_STATEMENT, part_in_self_path)
            match_other = re.match(self.RE_PARAMETER_STATEMENT, part_in_other_path)
            if match_self and match_other:
                # two different matches - don't accept
                return False

            if match_self or match_other:
                match, text = (match_self, part_in_other_path) if match_self else (match_other, part_in_self_path)
                parse_method = int if match.group(1) == "int" else str
                # make sure that part in path can be parsed according schema
                try:
                    _ = parse_method(text)
                except ValueError:
                    return False
            else:
                return False
        # check if query params are similar in case of `allow_schemas=True`
        query_prams_self = self.get_query_parameters()
        query_prams_other = other.get_query_parameters()
        if len(query_prams_self) != len(query_prams_other):
            return False

        for key, val_in_self in query_prams_self.items():
            if key not in query_prams_self.keys():
                raise KeyError(f"key {key} not in url query")
            val_in_other = query_prams_other[key]

            # first check if both are the same
            if val_in_self == val_in_other:
                continue
            # check if one side is variable (int or string)
            match_self = re.match(self.RE_PARAMETER_STATEMENT, val_in_self)
            match_other = re.match(self.RE_PARAMETER_STATEMENT, val_in_other)
            if match_self and match_other:
                # two different matches - don't accept
                return False

            if match_self or match_other:
                match, text = (match_self, val_in_other) if match_self else (match_other, val_in_self)
                parse_method = int if match.group(1) == "int" else str
                # make sure that part in path can be parsed according schema
                try:
                    _ = parse_method(text)
                except ValueError:
                    return False
            else:
                return False
        return True
