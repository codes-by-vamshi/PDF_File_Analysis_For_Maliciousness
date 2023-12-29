from typing import Any

from marshmallow import Schema, fields


class Count(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return 0
        return len(value)

    def _deserialize(self, value, attr, data, **kwargs):
        return len(value)


class ListStr(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return {}
        return {str(i): True for i in value}

    def _deserialize(self, value, attr, data, **kwargs):
        return {str(i): True for i in value}


class Scripts(Schema):
    urls = Count()
    iframe = Count()
    script_types = fields.Dict(keys=fields.String(), values=Count())


class FileFeatureSpec(Schema):
    file_size = fields.Float()
    yara_signatures = ListStr()
    scripts = fields.Nested(Scripts)

    def load(self, data: Any, **kwargs):
        data = super().load({
            k: v for k, v in data.items() if k in self.fields
        })
        return self.flatten_json(data)

    def dump(self, obj, **kwargs):
        data = super().dump(obj, **kwargs)
        return self.flatten_json(data)

    @staticmethod
    def flatten_json(y):
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(y)
        return out


class Signatures(Schema):
    name = fields.String()
    description = fields.String()
    families = fields.List(fields.String())
    severity = fields.Integer()
    references = fields.List(fields.String())
    marks = fields.List(fields.String())

    def load(self, data, **kwargs):
        data = super().load(data)
        return {'severity': data.get('severity')} if data else {}

    def dump(self, obj, **kwargs):
        data = super().dump(obj)
        return {'severity': data.get('severity')} if data else {}


class SignaturesMeta(Schema):
    sigCount = fields.Integer()
    severityCount = fields.Integer()

    def load(self, data, **kwargs):
        if data:
            data.update(self.count_sigs(data))
        data = super().load(data)
        return data

    def dump(self, obj, **kwargs):
        data = super().dump(obj)
        if data:
            data.update(self.count_sigs(data))
        return data

    def count_sigs(self, data):
        sig_count, severity_count = 0, 0
        for field, val in self.fields.items():
            if hasattr(val, 'nested') and val.nested.__name__ == 'Signatures':
                if field in data:
                    sig_count += 1
                    if data[field].get('severity', 0) > 4:
                        severity_count += 1
        return {'sigCount': sig_count, 'severityCount': severity_count} if any([sig_count, severity_count]) else {}
