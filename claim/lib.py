# -*- coding: utf-8 -*- 
# $Id: TimedeltaField.py 1787 2011-04-20 07:09:57Z tguettler $
# $HeadURL: svn+ssh://svnserver/svn/djangotools/trunk/dbfields/TimedeltaField.py $

# http://djangosnippets.org/snippets/1060/

# Python
import datetime

# Django
from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

#Djangotools
#from djangotools.utils.southutils import add_introspection_rules_from_baseclass

SECS_PER_DAY=3600*24

class TimedeltaField(models.Field):
    u'''
    Store Python's datetime.timedelta in an integer column.
    Most databasesystems only support 32 Bit integers by default.
    '''
    __metaclass__=models.SubfieldBase
    def __init__(self, *args, **kwargs):
        super(TimedeltaField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if (value is None) or isinstance(value, datetime.timedelta):
            return value
        assert isinstance(value, long), (value, type(value))
        return datetime.timedelta(seconds=value)

    def get_internal_type(self):
        return 'IntegerField'

    def get_db_prep_lookup(self, lookup_type, value, connection=None, prepared=False):
        raise NotImplementedError()  # SQL WHERE

    def get_db_prep_save(self, value, connection=None, prepared=False):
        if (value is None) or isinstance(value, long):
            return value
        return SECS_PER_DAY*value.days+value.seconds

    def formfield(self, *args, **kwargs):
        defaults={'form_class': TimedeltaFormField}
        defaults.update(kwargs)
        return super(TimedeltaField, self).formfield(*args, **defaults)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

#South Plugin registrieren
#add_introspection_rules_from_baseclass(TimedeltaField, ["^djangotools\.dbfields\.TimedeltaField"])

class TimedeltaFormField(forms.Field):
    default_error_messages = {
        'invalid':  _(u'Enter a whole number.'),
        }

    def __init__(self, *args, **kwargs):
        defaults={'widget': TimedeltaWidget}
        defaults.update(kwargs)
        super(TimedeltaFormField, self).__init__(*args, **defaults)

    def clean(self, value):
        # value comes from Timedelta.Widget.value_from_datadict(): tuple of strings
        super(TimedeltaFormField, self).clean(value)
        assert len(value)==len(self.widget.inputs), (value, self.widget.inputs)
        i=0
        for value, multiply in zip(value, self.widget.multiply):
            try:
                i+=int(value)*multiply
            except ValueError, TypeError:
                raise forms.ValidationError(self.error_messages['invalid'])
        return i

class TimedeltaWidget(forms.Widget):
    INPUTS=['days', 'hours', 'minutes', 'seconds']
    MULTIPLY=[60*60*24, 60*60, 60, 1]
    def __init__(self, attrs=None):
        self.widgets=[]
        if not attrs:
            attrs={}
        inputs=attrs.get('inputs', self.INPUTS)
        multiply=[]
        for input in inputs:
            assert input in self.INPUTS, (input, self.INPUT)
            self.widgets.append(forms.TextInput(attrs=attrs))
            multiply.append(self.MULTIPLY[self.INPUTS.index(input)])
        self.inputs=inputs
        self.multiply=multiply
        super(TimedeltaWidget, self).__init__(attrs)

    def render(self, name, value, attrs):
        if value is None:
            values=[0 for i in self.inputs]
        elif isinstance(value, datetime.timedelta):
            values=split_seconds(value.days*SECS_PER_DAY+value.seconds, self.inputs, self.multiply)
        elif isinstance(value, long):
            # initial data from model
            values=split_seconds(value, self.inputs, self.multiply)
        else:
            assert isinstance(value, tuple), (value, type(value))
            assert len(value)==len(self.inputs), (value, self.inputs)
            values=value
        id=attrs.pop('id')
        assert not attrs, attrs
        rendered=[]
        for input, widget, val in zip(self.inputs, self.widgets, values):
            rendered.append(u'%s %s' % (_(input), widget.render('%s_%s' % (name, input), val)))
        return mark_safe('<div id="%s">%s</div>' % (id, ' '.join(rendered)))

    def value_from_datadict(self, data, files, name):
        # Don't throw ValidationError here, just return a tuple of strings.
        ret=[]
        for input, multi in zip(self.inputs, self.multiply):
            ret.append(data.get('%s_%s' % (name, input), 0))
        return tuple(ret)

    def _has_changed(self, initial_value, data_value):
        # data_value comes from value_from_datadict(): A tuple of strings.
        if initial_value is None:
            return bool(set(data_value)!=set([u'0']))
        assert isinstance(initial_value, datetime.timedelta), initial_value
        initial=tuple([unicode(i) for i in split_seconds(initial_value.days*SECS_PER_DAY+initial_value.seconds, self.inputs, self.multiply)])
        assert len(initial)==len(data_value), (initial, data_value)
        return bool(initial!=data_value)

def main():
    assert split_seconds(1000000)==[11, 13, 46, 40]

    field=TimedeltaField()

    td=datetime.timedelta(days=10, seconds=11)
    s=field.get_db_prep_save(td)
    assert isinstance(s, long), (s, type(s))
    td_again=field.to_python(s)
    assert td==td_again, (td, td_again)

    td=datetime.timedelta(seconds=11)
    s=field.get_db_prep_save(td)
    td_again=field.to_python(s)
    assert td==td_again, (td, td_again)

    field=TimedeltaFormField()
    assert field.widget._has_changed(datetime.timedelta(seconds=0), (u'0', u'0', u'0', u'0',)) is False
    assert field.widget._has_changed(None, (u'0', u'0', u'0', u'0',)) is False
    assert field.widget._has_changed(None, (u'0', u'0')) is False
    assert field.widget._has_changed(datetime.timedelta(days=1, hours=2, minutes=3, seconds=4), (u'1', u'2', u'3', u'4',)) is False

    for secs, soll, kwargs in [
        (100, [0, 0, 1, 40], dict()),
        (100, ['0days', '0hours', '1minutes', '40seconds'], dict(with_unit=True)),
        (100, ['1minutes', '40seconds'], dict(with_unit=True, remove_leading_zeros=True)),
        (100000, ['1days', '3hours'], dict(inputs=['days', 'hours'], with_unit=True, remove_leading_zeros=True)),
        ]:
        ist=split_seconds(secs, **kwargs)
        if ist!=soll:
            raise Exception('geg=%s soll=%s ist=%s kwargs=%s' % (secs, soll, ist, kwargs))

    print "unittest OK"

def split_seconds(secs, inputs=TimedeltaWidget.INPUTS, multiply=TimedeltaWidget.MULTIPLY,
                  with_unit=False, remove_leading_zeros=False):
    ret=[]
    assert len(inputs)<=len(multiply), (inputs, multiply)
    for input, multi in zip(inputs, multiply):
        count, secs = divmod(secs, multi)
        if remove_leading_zeros and not ret and not count:
            continue
        if with_unit:
            ret.append('%s%s' % (count, input))
        else:
            ret.append(count)
    return ret

if __name__=='__main__':
    main()


ORDER_VAR = 'o'
ORDER_TYPE_VAR = 'ot'

class SortHeaders:
    """
    Handles generation of an argument for the Django ORM's
    ``order_by`` method and generation of table headers which reflect
    the currently selected sort, based on defined table headers with
    matching sort criteria.

    Based in part on the Django Admin application's ``ChangeList``
    functionality.
    """
    def __init__(self, request, headers, default_order_field=None,
            default_order_type='asc', additional_params=None):
        """
        request
            The request currently being processed - the current sort
            order field and type are determined based on GET
            parameters.

        headers
            A list of two-tuples of header text and matching ordering
            criteria for use with the Django ORM's ``order_by``
            method. A criterion of ``None`` indicates that a header
            is not sortable.

        default_order_field
            The index of the header definition to be used for default
            ordering and when an invalid or non-sortable header is
            specified in GET parameters. If not specified, the index
            of the first sortable header will be used.

        default_order_type
            The default type of ordering used - must be one of
            ``'asc`` or ``'desc'``.

        additional_params:
            Query parameters which should always appear in sort links,
            specified as a dictionary mapping parameter names to
            values. For example, this might contain the current page
            number if you're sorting a paginated list of items.
        """
        if default_order_field is None:
            for i, (header, query_lookup) in enumerate(headers):
                if query_lookup is not None:
                    default_order_field = i
                    break
        if default_order_field is None:
            raise AttributeError('No default_order_field was specified and none of the header definitions given were sortable.')
        if default_order_type not in ('asc', 'desc'):
            raise AttributeError('If given, default_order_type must be one of \'asc\' or \'desc\'.')
        if additional_params is None: additional_params = {}

        self.header_defs = headers
        self.additional_params = additional_params
        self.order_field, self.order_type = default_order_field, default_order_type

        # Determine order field and order type for the current request
        params = dict(request.GET.items())
        if ORDER_VAR in params:
            try:
                new_order_field = int(params[ORDER_VAR])
                if headers[new_order_field][1] is not None:
                    self.order_field = new_order_field
            except (IndexError, ValueError):
                pass # Use the default
        if ORDER_TYPE_VAR in params and params[ORDER_TYPE_VAR] in ('asc', 'desc'):
            self.order_type = params[ORDER_TYPE_VAR]

    def headers(self):
        """
        Generates dicts containing header and sort link details for
        all defined headers.
        """
        for i, (header, order_criterion) in enumerate(self.header_defs):
            th_classes = []
            new_order_type = 'asc'
            if i == self.order_field:
                th_classes.append('sorted %sending' % self.order_type)
                new_order_type = {'asc': 'desc', 'desc': 'asc'}[self.order_type]
            yield {
                'text': header,
                'sortable': order_criterion is not None,
                'url': self.get_query_string({ORDER_VAR: i, ORDER_TYPE_VAR: new_order_type}),
                'class_attr': (th_classes and ' class="%s"' % ' '.join(th_classes) or ''),
            }

    def get_query_string(self, params):
        """
        Creates a query string from the given dictionary of
        parameters, including any additonal parameters which should
        always be present.
        """
        params.update(self.additional_params)
        return '?%s' % '&amp;'.join(['%s=%s' % (param, value) \
                                     for param, value in params.items()])

    def get_order_by(self):
        """
        Creates an ordering criterion based on the current order
        field and order type, for use with the Django ORM's
        ``order_by`` method.
        """
        return '%s%s' % (
            self.order_type == 'desc' and '-' or '',
            self.header_defs[self.order_field][1],
        )