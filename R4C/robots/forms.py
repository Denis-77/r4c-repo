from datetime import datetime
import json

from django import forms
from django.core.exceptions import ValidationError


class NewRobotForm(forms.Form):
    json_string = forms.CharField(label='JSON', required=True, widget=forms.TextInput(attrs={"size": "50"}))

    def clean(self):
        cleaned_data = super(NewRobotForm, self).clean()
        json_str = cleaned_data.get('json_string')
        try:
            data = json.loads(json_str)
            if not ('model' in data and 'version' in data and 'created' in data):
                raise ValidationError('one or more of fields are missing')
            if (not isinstance(data['model'], str)) or len(data['model']) != 2:
                raise ValidationError('value of model is not correct')
            if (not isinstance(data['version'], str)) or len(data['version']) != 2:
                raise ValidationError('value of version is not correct')
            try:
                date_string = data['created']
                date_format = "%Y-%m-%d %H:%M:%S"
                self.date_object = datetime.strptime(date_string, date_format)
            except TypeError:
                raise ValidationError('date must be string')
            except ValueError:
                raise ValidationError('wrong date/time format correct: yyyy-mm-dd hh:mm:ss')
        except json.JSONDecodeError:
            raise ValidationError('incorrect json string')
        return cleaned_data


