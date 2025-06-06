'''
Taken from salt: salt/utils/jinja.py

Copyright (c) 2015 - 2024 Rob "N3X15" Nelson <nexisentertainment@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


MODIFICATIONS:

Jan 16 2021:
 * Converted PyYAML to ruamel.yaml.

'''

# Import python libs
from __future__ import absolute_import
import json
import pprint
import logging
from functools import wraps

# Import third party libs
import six
from jinja2 import nodes
from jinja2.environment import TemplateModule
from jinja2.ext import Extension
from jinja2.exceptions import TemplateRuntimeError
import jinja2
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO
from ruamel.yaml.representer import RoundTripRepresenter

try:
    from markupsafe import Markup
except ImportError:
    # jinja < 3.1
    from jinja2 import Markup

try:
    contextfunction = jinja2.contextfunction
except AttributeError:
    contextfunction = jinja2.pass_context

yaml = YAML(typ='safe', pure=True)

from collections import OrderedDict

log = logging.getLogger(__name__)

__all__ = [
    'SerializerExtension',
    'salty_jinja_envs'
]

def salty_jinja_envs(trim_blocks=False,lstrip_blocks=False):
    env_args = {'extensions': []}

    if hasattr(jinja2.ext, 'with_'):
        env_args['extensions'].append('jinja2.ext.with_')
    if hasattr(jinja2.ext, 'do'):
        env_args['extensions'].append('jinja2.ext.do')
    if hasattr(jinja2.ext, 'loopcontrols'):
        env_args['extensions'].append('jinja2.ext.loopcontrols')
    env_args['extensions'].append(SerializerExtension)

    # Pass through trim_blocks and lstrip_blocks Jinja parameters
    # trim_blocks removes newlines around Jinja blocks
    # lstrip_blocks strips tabs and spaces from the beginning of
    # line to the start of a block.
    if trim_blocks:
        log.debug('Jinja2 trim_blocks is enabled')
        env_args['trim_blocks'] = True
    if lstrip_blocks:
        log.debug('Jinja2 lstrip_blocks is enabled')
        env_args['lstrip_blocks'] = True

    return env_args

# To dump OrderedDict objects as regular dicts. Used by the yaml
# template filter.
class ODRepresenter(RoundTripRepresenter):
    pass

yaml = YAML(typ='safe')
yaml.representer.add_representer(OrderedDict,
                                 ODRepresenter.represent_dict)




class PrintableDict(OrderedDict):
    '''
    Ensures that dict str() and repr() are YAML friendly.

    .. code-block:: python

        mapping = OrderedDict([('a', 'b'), ('c', None)])
        print mapping
        # OrderedDict([('a', 'b'), ('c', None)])

        decorated = PrintableDict(mapping)
        print decorated
        # {'a': 'b', 'c': None}
    '''
    def __str__(self):
        output = []
        for key, value in six.iteritems(self):
            if isinstance(value, six.string_types):
                # keeps quotes around strings
                output.append('{0!r}: {1!r}'.format(key, value))
            else:
                # let default output
                output.append('{0!r}: {1!s}'.format(key, value))
        return '{' + ', '.join(output) + '}'

    def __repr__(self):  # pylint: disable=W0221
        output = []
        for key, value in six.iteritems(self):
            output.append('{0!r}: {1!r}'.format(key, value))
        return '{' + ', '.join(output) + '}'


def ensure_sequence_filter(data):
    '''
    Ensure sequenced data.

    **sequence**

        ensure that parsed data is a sequence

    .. code-block:: yaml

        {% set my_string = "foo" %}
        {% set my_list = ["bar", ] %}
        {% set my_dict = {"baz": "qux"} %}

        {{ my_string|sequence|first }}
        {{ my_list|sequence|first }}
        {{ my_dict|sequence|first }}


    will be rendered as:

    .. code-block:: yaml

        foo
        bar
        baz
    '''
    if not isinstance(data, (list, tuple, set, dict)):
        return [data]
    return data


@contextfunction
def show_full_context(ctx):
    return ctx

# REMOVED SaltCacheLoader.

class SerializerExtension(Extension, object):
    '''
    Yaml and Json manipulation.

    **Format filters**

    Allows to jsonify or yamlify any data structure. For example, this dataset:

    .. code-block:: python

        data = {
            'foo': True,
            'bar': 42,
            'baz': [1, 2, 3],
            'qux': 2.0
        }

    .. code-block:: jinja

        yaml = {{ data|yaml }}
        json = {{ data|json }}
        python = {{ data|python }}

    will be rendered as::

        yaml = {bar: 42, baz: [1, 2, 3], foo: true, qux: 2.0}
        json = {"baz": [1, 2, 3], "foo": true, "bar": 42, "qux": 2.0}
        python = {'bar': 42, 'baz': [1, 2, 3], 'foo': True, 'qux': 2.0}

    The yaml filter takes an optional flow_style parameter to control the
    default-flow-style parameter of the YAML dumper.

    .. code-block:: jinja

        {{ data|yaml(False) }}

    will be rendered as:

    .. code-block:: yaml

        bar: 42
        baz:
          - 1
          - 2
          - 3
        foo: true
        qux: 2.0

    **Load filters**

    Strings and variables can be deserialized with **load_yaml** and
    **load_json** tags and filters. It allows one to manipulate data directly
    in templates, easily:

    .. code-block:: jinja

        {%- set yaml_src = "{foo: it works}"|load_yaml %}
        {%- set json_src = "{'bar': 'for real'}"|load_json %}
        Dude, {{ yaml_src.foo }} {{ json_src.bar }}!

    will be rendered has::

        Dude, it works for real!

    **Load tags**

    Salt implements **import_yaml** and **import_json** tags. They work like
    the `import tag`_, except that the document is also deserialized.

    Syntaxes are {% load_yaml as [VARIABLE] %}[YOUR DATA]{% endload %}
    and {% load_json as [VARIABLE] %}[YOUR DATA]{% endload %}

    For example:

    .. code-block:: jinja

        {% load_yaml as yaml_src %}
            foo: it works
        {% endload %}
        {% load_json as json_src %}
            {
                "bar": "for real"
            }
        {% endload %}
        Dude, {{ yaml_src.foo }} {{ json_src.bar }}!

    will be rendered has::

        Dude, it works for real!

    **Import tags**

    External files can be imported and made available as a Jinja variable.

    .. code-block:: jinja

        {% import_yaml "myfile.yml" as myfile %}
        {% import_json "defaults.json" as defaults %}
        {% import_text "completeworksofshakespeare.txt" as poems %}

    **Catalog**

    ``import_*`` and ``load_*`` tags will automatically expose their
    target variable to import. This feature makes catalog of data to
    handle.

    for example:

    .. code-block:: jinja

        # doc1.sls
        {% load_yaml as var1 %}
            foo: it works
        {% endload %}
        {% load_yaml as var2 %}
            bar: for real
        {% endload %}

    .. code-block:: jinja

        # doc2.sls
        {% from "doc1.sls" import var1, var2 as local2 %}
        {{ var1.foo }} {{ local2.bar }}

    .. _`import tag`: http://jinja.pocoo.org/docs/templates/#import
    '''

    tags = set(['load_yaml', 'load_json', 'import_yaml', 'import_json',
                'load_text', 'import_text'])

    def __init__(self, environment):
        super(SerializerExtension, self).__init__(environment)
        self.environment.filters.update({
            'yaml': self.format_yaml,
            'json': self.format_json,
            'python': self.format_python,
            'load_yaml': self.load_yaml,
            'load_json': self.load_json,
            'load_text': self.load_text,
        })

        if self.environment.finalize is None:
            self.environment.finalize = self.finalizer
        else:
            finalizer = self.environment.finalize

            @wraps(finalizer)
            def wrapper(self, data):
                return finalizer(self.finalizer(data))
            self.environment.finalize = wrapper

    def finalizer(self, data):
        '''
        Ensure that printed mappings are YAML friendly.
        '''
        def explore(data):
            if isinstance(data, (dict, OrderedDict)):
                return PrintableDict(
                    [(key, explore(value)) for key, value in six.iteritems(data)]
                )
            elif isinstance(data, (list, tuple, set)):
                return data.__class__([explore(value) for value in data])
            return data
        return explore(data)

    def format_json(self, value, sort_keys=True, indent=None):
        return Markup(json.dumps(value, sort_keys=sort_keys, indent=indent).strip())

    def format_yaml(self, value, flow_style=True):
        if not flow_style:
            yaml.indent()
        else:
            yaml.compact()
        s = StringIO()
        yaml.dump(value, s)
        yaml_txt = s.getvalue().strip()
        if yaml_txt.endswith('\n...\n'):
            # Changed to warning. - N3X
            log.warn('Yaml filter ended with "\n...\n". This trailing string '
                     'will be removed in Boron.')
        return Markup(yaml_txt)

    def format_python(self, value):
        return Markup(pprint.pformat(value).strip())

    def load_yaml(self, value):
        if isinstance(value, TemplateModule):
            value = str(value)
        try:
            return yaml.load(value)
        except AttributeError:
            raise TemplateRuntimeError(
                'Unable to load yaml from {0}'.format(value))

    def load_json(self, value):
        if isinstance(value, TemplateModule):
            value = str(value)
        try:
            return json.loads(value)
        except (ValueError, TypeError, AttributeError):
            raise TemplateRuntimeError(
                'Unable to load json from {0}'.format(value))

    def load_text(self, value):
        if isinstance(value, TemplateModule):
            value = str(value)

        return value

    _load_parsers = set(['load_yaml', 'load_json', 'load_text'])

    def parse(self, parser):
        if parser.stream.current.value == 'import_yaml':
            return self.parse_yaml(parser)
        elif parser.stream.current.value == 'import_json':
            return self.parse_json(parser)
        elif parser.stream.current.value == 'import_text':
            return self.parse_text(parser)
        elif parser.stream.current.value in self._load_parsers:
            return self.parse_load(parser)

        parser.fail('Unknown format ' + parser.stream.current.value,
                    parser.stream.current.lineno)

    # pylint: disable=E1120,E1121
    def parse_load(self, parser):
        filter_name = parser.stream.current.value
        lineno = next(parser.stream).lineno
        if filter_name not in self.environment.filters:
            parser.fail('Unable to parse {0}'.format(filter_name), lineno)

        parser.stream.expect('name:as')
        target = parser.parse_assign_target()
        macro_name = '_' + parser.free_identifier().name
        macro_body = parser.parse_statements(
            ('name:endload',), drop_needle=True)

        return [
            nodes.Macro(
                macro_name,
                [],
                [],
                macro_body
            ).set_lineno(lineno),
            nodes.Assign(
                target,
                nodes.Filter(
                    nodes.Call(
                        nodes.Name(macro_name, 'load').set_lineno(lineno),
                        [],
                        [],
                        None,
                        None
                    ).set_lineno(lineno),
                    filter_name,
                    [],
                    [],
                    None,
                    None
                ).set_lineno(lineno)
            ).set_lineno(lineno)
        ]

    def parse_yaml(self, parser):
        import_node = parser.parse_import()
        target = import_node.target
        lineno = import_node.lineno

        return [
            import_node,
            nodes.Assign(
                nodes.Name(target, 'store').set_lineno(lineno),
                nodes.Filter(
                    nodes.Name(target, 'load').set_lineno(lineno),
                    'load_yaml',
                    [],
                    [],
                    None,
                    None
                )
                .set_lineno(lineno)
            ).set_lineno(lineno)
        ]

    def parse_json(self, parser):
        import_node = parser.parse_import()
        target = import_node.target
        lineno = import_node.lineno

        return [
            import_node,
            nodes.Assign(
                nodes.Name(target, 'store').set_lineno(lineno),
                nodes.Filter(
                    nodes.Name(target, 'load').set_lineno(lineno),
                    'load_json',
                    [],
                    [],
                    None,
                    None
                )
                .set_lineno(lineno)
            ).set_lineno(lineno)
        ]

    def parse_text(self, parser):
        import_node = parser.parse_import()
        target = import_node.target
        lineno = import_node.lineno

        return [
            import_node,
            nodes.Assign(
                nodes.Name(target, 'store').set_lineno(lineno),
                nodes.Filter(
                    nodes.Name(target, 'load').set_lineno(lineno),
                    'load_text',
                    [],
                    [],
                    None,
                    None
                )
                .set_lineno(lineno)
            ).set_lineno(lineno)
        ]
    # pylint: enable=E1120,E1121
