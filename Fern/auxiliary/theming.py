from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.color_definitions import colors


def apply_default_theme(app: MDApp) -> None:
    app.theme_cls.theme_style = 'Dark'

    app.theme_cls.primary_palette = 'Cyan'
    app.theme_cls.primary_hue = '600'

    app.success_color = app.theme_cls.colors['LightGreen']['A400']
    app.failure_color = app.theme_cls.colors['Red']['A700']
    app.neutral_color = app.theme_cls.text_color


def get_siemens_color(type: str, color: str):
    SIEMENS_COLORS = {
        'Primary': {
            'SiemensPetrol': '009999',
            'DeepBlue': '000028',
            'DeepBlueNews': '041739',
            'LightSand': 'F3F3F0',
            'White': 'FFFFFF',
            'BoldDynamicPetrol': '00FFB9',
            'SoftDynamicPetrol': '00D7A0',
        },
        'Secondary': {
            'DeepBlue80': '333353',
            'DeepBlue60': '66667E',
            'DeepBlue40': '9999A9',
            'DeepBlue20': 'CCCCD4',
            'DeepBlue10': 'E5E5E9',
            'DarkGray': '66667E',
            'SoftGray': 'CCCCD4',
            'DarkBlue': '00557C',
            'Blue': '0087BE',
            'SoftBlue': '00BEDC',
            'DarkGreen': '00646E',
            'Green': '00AF8E',
            'SoftGreen': '00D7A0',
            'BoldBlue': '00e6dc',
            'BoldGreen': '00FFB9',
            'DarkPurple': '500078',
            'DarkOrange': 'EC6602',
            'DarkSand': 'AAAA96',
            'Purple': 'AA32BE',
            'Yellow': 'FFD732',
            'Orange': 'FF9000',
            'Red': 'EF0137',
            'SoftRed': 'FE8389',
            'SoftSand': 'C5C5B8',
            'BrightSand': 'DFDFD9',
        },
        'InteractionDark': {
            'InteractiveCoral': '00CCCC',
            'InteractiveCoral50db': '007082',
            'InteractiveCoral20db': '002949',
            'InteractiveCoral12db': '00183B',
            'InteractiveCoral8db': '001034',
            'DeepBlue30': 'B3B3BE',
            'DeepBlue55': '737389',
            'DeepBlue85': '262648',
            'LightGreen40': 'C5FFEF',
            'BoldGreen12db': '001F39',
            'MediumRed': 'FF5454',
            'DarkRed': '331131',
        },
        'InteractionLight': {
            'InteractiveCyan': '0098A6',
            'InteractiveCyan8': 'EBF7F8',
            'InteractiveBlue': '007993',
            'InteractiveBlue55': '73BAC9',
            'InteractiveBlue12': 'E0F1F4',
            'Teal': '005159',
            'Teal90': '196269',
            'LightGreen': '62EEC7',
            'BoldGreen20': 'C2FFEE',
            'BoldGreen18': 'D1FFF2',
            'BoldGreen10': 'E0FFF6',
            'DeepBlue70': '4C4C68',
            'DeepBlue50': '7D8099',
            'DeepBlue8': 'EBEBEE',
            'LightRed': 'FCCCD7',
            'LightGrey': 'D9D9D6',
        },
        'FeedbackDark': {
            'Blue': '00BEDC',
            'Green': '01D65A',
            'Red': 'FF2640',
            'Yellow': 'FFD732',
            'Orange': 'FF9000',
            'RedText': 'FF7687',
        },
        'FeedbackLight': {
            'Blue': '007EB1',
            'Green': '01893A',
            'GreenText': '018136',
            'Red': 'D72339',
            'Yellow': 'E9C32A',
            'Orange': 'E96401',
        },
    }

    return get_color_from_hex(SIEMENS_COLORS[type][color])


def apply_siemens_theme(app: MDApp) -> None:
    app.theme_cls.theme_style = 'Dark'

    colors['Cyan']['600'] = '00FFB9'
    colors['Dark']['Background'] = '000028'
    colors['Dark']['CardsDialogs'] = '23233c'

    app.theme_cls.primary_palette = 'Cyan'
    app.theme_cls.primary_hue = '600'

    app.success_color = get_siemens_color('FeedbackDark', 'Green')
    app.failure_color = get_siemens_color('FeedbackDark', 'Red')
    app.neutral_color = app.theme_cls.text_color
