from django import forms


class AppModForm(forms.Form):
    APP_MODE_CHOICES = (
        (1, 'Умножение'),
        (2, 'Сложение'),
        (3, 'Вычитание'),
    )
    # CHOICES = (('a', 'a'),
    #            ('b', 'b'),
    #            ('c', 'c'),
    #            ('d', 'd'),)
    # picked = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple())

    # app_mode=[]

    app_mode = forms.MultipleChoiceField(
         label='Выберите режим упражнения:',
         required=True,
         widget=forms.CheckboxSelectMultiple(attrs={'checked': True}),
         choices=APP_MODE_CHOICES,
    )
    #
    # class UserForm(forms.Form):
    #     name = forms.CharField(label="Имя")
    #     comment = forms.CharField(label="Комментарий", widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control2'
            field.help_text = ''




class Ans_Form(forms.Form):
    answer = forms.CharField(label='Ваш ответ:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control2'
            qt="\'"
            field.widget.attrs['onfocus'] = f"this.value={qt}{qt}"
            field.widget.attrs['autocomplete'] = "off"
            field.widget.attrs['value'] = f"сюда"
            field.widget.attrs['autofocus'] = "autofocus"
            field.help_text = ''


    def clean_answer(self):
        data=""
        data = self.cleaned_data['answer']
        if data.isdigit() == True:
            if int(data) < 18:
                pass#
        else:
            raise forms.ValidationError("только цифры!")

        return data



