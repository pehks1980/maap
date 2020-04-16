from django import forms

class Ans_Form(forms.Form):
    answer = forms.CharField(label='Your answer')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            qt="\'"
            field.widget.attrs['onfocus'] = f"this.value={qt}{qt}"
            field.widget.attrs['autocomplete'] = "off"
            field.widget.attrs['value'] = f"вводить сюда"
            field.widget.attrs['autofocus'] = "autofocus"
            field.help_text = ''


    def clean_answer(self):
        data=""
        data = self.cleaned_data['answer']
        if data.isdigit() == True:
            if int(data) < 18:
                pass#raise forms.ValidationError("Вы слишком молоды!")
        else:
            raise forms.ValidationError("только цифры!")

        return data

APP_MODE_CHOICES = (
    (1, 'Умножение'),
    (2, 'Сложение'),
    (3, 'Вычитание'),
)

class AppModForm(forms.Form):
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
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
