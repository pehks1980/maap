from django import forms


# Начальная форма выбора упражнений
class AppModForm(forms.Form):
    APP_MODE_CHOICES = (
        (1, 'Умножение (таблица 1-12)'),
        (2, 'Сложение'),
        (3, 'Вычитание'),
        (4, 'Деление (по таблице)'),
        (5, 'Примеры столбиком'),
        (6, 'Примеры с дробями'),
    )

    app_mode = forms.MultipleChoiceField(
        label='Выберите режим упражнения:',
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'checked': False}),
        choices=APP_MODE_CHOICES,
        initial=[3, 4, 5, 6]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control2'
            field.help_text = ''


# Форма-вопрос-ответ для примеров 1-4 типа
class Ans_Form(forms.Form):
    answer = forms.CharField(label='Ваш ответ:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control2'
            qt = "\'"
            field.widget.attrs['onfocus'] = f"this.value={qt}{qt}"
            field.widget.attrs['autocomplete'] = "off"
            field.widget.attrs['value'] = f"сюда"
            field.widget.attrs['autofocus'] = "autofocus"
            field.help_text = ''

    def clean_answer(self):
        data = self.cleaned_data['answer']
        if not data.isdigit():
            raise forms.ValidationError("только цифры!")

        return data
