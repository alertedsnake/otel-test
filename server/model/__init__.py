import datetime
import pynamodb.attributes as attributes

from pynamodb.models             import Model
from pynamodb.attributes         import (UnicodeAttribute, UTCDateTimeAttribute)
from google.protobuf.json_format import ParseDict


class BaseModel(Model):
    def to_protobuf(self, cls):

        d = {}

        for field in cls.DESCRIPTOR.fields:
            key = field.name

            try:
                val = getattr(self, key)
            except AttributeError:
                continue

            try:
                newval = self.__convert_field_protobuf(val)
                if newval is not None:
                    d[key] = newval

                # map empty list types to empty lists
                elif isinstance(val, (attributes.SetMixin, attributes.ListAttribute)):
                    d[key] = []

            except AttributeError:
                continue

        return ParseDict(d, cls(), ignore_unknown_fields=True)


    def __convert_field_protobuf(self, value):

        if isinstance(value, (attributes.MapAttribute, attributes.JSONAttribute)):
            return value.as_dict()
        elif isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        # note that with these we recursively call ourself on
        # each item
        elif isinstance(value, (set, list)):
            return list(self.__convert_field_protobuf(v) for v in value)

        else:
            return value


class Widget(BaseModel):
    """A widget!"""

    class Meta:
        table_name = 'Widget'
        write_capacity_units = 1
        read_capacity_units = 1

    name = UnicodeAttribute(hash_key=True)
    description = UnicodeAttribute()
    create_time = UTCDateTimeAttribute()
