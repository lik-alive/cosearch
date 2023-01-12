import re
import requests
from bs4 import BeautifulSoup
from .info import Info
from app.actions.helper import sstr

"""Parse paper title and authors in Russian."""


def parse_paper_title_and_authors_ru(info: Info):
    # Find by link (1-5, 12-15, 31+)
    if info._issue.vol > 30 or (info._issue.vol < 16 and info._issue.vol > 11) or info._issue.vol < 6:
        links = info.info_td.select('a')

        i = 0
        while i < len(links):
            link = links[i]
            i += 1

            # Skip staff links
            if 'staff' in link['href'].lower():
                continue

            # HOT FIXES
            if info.issue == '42-2' and 'Котляр' in link.text:
                continue
            if info.issue == '35-3' and 'В.А.' in link.text:
                continue
            if info.issue == '35-2' and info.no == 1 and 'А' == link.text:
                continue
            if info.issue == '34-1' and 'Досколович' in link.text:
                continue
            if info.issue == '33-4' and 'Досколович' in link.text:
                continue
            if info.issue == '31-1' and 'Хонина' in link.text:
                continue

            title = link.text

            # HOT FIXES
            if info.issue == '45-2' and info.no == 8:
                title += '3'
            if info.issue == '35-2' and info.no == 1:
                title = 'Анализ и распознавание наномасштабных изображений: традиционные подходы и новые постановки задач'

            # Sanitize
            title = sstr(title, True, True)

            # Check locale
            if re.search(r'[А-ЯЁа-яё]', title) is None:
                info.title_en = title
            else:
                info.title_ru = title

            # Parse authors
            info_str = sstr(info.info_td.text)

            # Fix dots
            info_str = re.sub(r'\.([A-ZА-ЯЁ])', r'. \1', info_str)

            # Fix quote
            info_str = info_str.replace('’', '\'')

            # Merge initials (three and two initials in separate cases since re.sub looks only once)
            info_str = re.sub(
                r'([A-ZА-ЯЁ][a-zа-яё]?\.) ([A-ZА-ЯЁ][a-zа-яё]?\.) ([A-ZА-ЯЁ][a-zа-яё]?\.)', r'\1\2\3', info_str)
            info_str = re.sub(
                r'([A-ZА-ЯЁ][a-zа-яё]?\.) ([A-ZА-ЯЁ][a-zа-яё]?\.)', r'\1\2', info_str)

            # Remove space before comma
            info_str = info_str.replace(' ,', ',')

            # Get first 'word' of the title
            word = title[0:5]

            # Initials last
            if (info.issue != '40-5' and info._issue.vol > 16) or (info.issue == '13' and info.no == 2) or (info.issue == '13' and info.no == 3) or (info.issue == '13' and info.no == 4):
                items = re.findall(
                    r"^(([A-ZА-ЯЁÁ][\w'-]+ [A-ZА-ЯЁ][a-zа-яё]?\.(-?[A-ZА-ЯЁ][a-zа-яё]?\.)*,? ?)+)\.? ?" + word, info_str)
            # Initials first
            else:
                items = re.findall(
                    r"^(([A-ZА-ЯЁ][a-zа-яё]?\.(-?[A-ZА-ЯЁ][a-zа-яё]?\.)* [A-ZА-ЯЁ][\w'-]+,? ?)+)\.? ?" + word, info_str)

            if len(items) > 0 and len(items[0]) > 2:
                authors = sstr(items[0][0])

                # Check locale
                if re.search(r'[А-ЯЁа-яё]', title) is None:
                    info.authors_en = authors
                else:
                    info.authors_ru = authors
            else:
                if info.issue == '1' and info.no == 19:
                    info.authors_ru = "М.А. Манько, Б.И. Махсудов, Фам Ван Хой"
                elif info.issue == '2' and info.no == 2:
                    info.authors_ru = sstr('М.А. Отливанчик')
                elif info.issue == '2' and info.no == 14:
                    info.authors_ru = sstr('В.В. Пархаев. В.С. Ющенко')
                elif info.issue == '3' and info.no == 8:
                    info.authors_ru = sstr(
                        'М.М. Вайнбранд, С.В. Ермолаев, Б.Е. Кинбер, О.Р. Рачко, М.Ю. Червенко')
                elif info.issue == '3' and info.no == 14:
                    info.authors_ru = sstr(
                        'С.Ф. Агешин, А.А. Азаров, В.В. Попов, И.Н. Сисакян')
                elif info.issue == '3' and info.no == 19:
                    info.authors_ru = sstr(
                        'Д.Д. Кловский, И.Н. Сисакян, А.Б. Шварцбург, А.Ю. Шерман, С.М. Широков')
                elif info.issue == '13' and info.no == 9:
                    info.authors_ru = sstr(
                        'А.Е. Баронов')
                elif info.issue == '31-1' and info.no == 8:
                    info.authors_ru = sstr(
                        'Дмитриев А.Ю., Харитонов С.И., Дюндик В.К.')
                elif info.issue == '32-1' and info.no == 1:
                    info.authors_ru = None
                elif info.issue == '32-1' and info.no == 2:
                    info.authors_ru = None
                elif info.issue == '32-3' and info.no == 4:
                    info.authors_ru = sstr(
                        'Безус Е.А., Досколович Л.Л., Кадомин И.И., Казанский Н.Л., Pierluigi Civera, Marco Pizzi')
                elif info.issue == '32-4' and info.no == 1:
                    info.authors_ru = sstr(
                        "Котляр В.В., Триандафилов Я.Р., Ковалев А.А., Котляр М.И., Волков А.В., Володкин Б.О., Сойфер В.А., О'Фелон Лим, Краусс Томас")
                elif info.issue == '33-1' and info.no == 1:
                    info.authors_ru = None
                elif info.issue == '33-2' and info.no == 2:
                    info.authors_en = sstr(
                        "P. Vacas-Jacques, V. Ryabukho, M. Strojnik, V. Tuchin, G. Paez")
                    info.title_en = sstr(
                        "Theoretical Diffractive Filter Performance for Ballistic Transillumination")
                elif "Правила подготовки рукописей" in title:
                    info.authors_ru = None
                elif info.issue == '33-2' and "Памяти Вольдемара" in title:
                    info.authors_ru = None
                elif info.issue == '33-3' and info.no == 4:
                    info.authors_en = sstr(
                        "Irina G. Palchikova, Sergey G. Rautian")
                elif info.issue == '35-2' and info.no == 1:
                    info.authors_ru = sstr(
                        "Сойфер В.А., Куприянов А.В.")
                elif info.issue == '35-4' and info.no == 12:
                    info.authors_ru = sstr(
                        "Баврина А.Ю., Мясников В.В., Сергеев А.В.")
                elif info.issue == '36-1' and info.no == 9:
                    info.authors_ru = sstr(
                        "Котляр В.В., Налимов А.Г., Шанина М.И., Сойфер В.А., О'Фаолайн Л., Минеев Е.В., Якимчук И.В., Асадчиков В.Е.")
                elif info.issue == '36-3' and info.no == 10:
                    info.authors_ru = sstr(
                        "Скиданов Р.В., Морозов А.А., Порфирьев А.П.")
                elif info.issue == '37-4' and "Памяти" in title:
                    info.authors_ru = None
                elif info.issue == '38-2' and info.no == 11:
                    info.authors_ru = sstr(
                        "Налимов А.Г., О'Фаолейн Л., Стафеев С.С., Шанина М.И., Котляр В.В.")
                elif info.issue == '39-3' and info.no == 16:
                    info.authors_ru = sstr(
                        "Лисин А.В., Файзуллин Р.Т.")
                elif info.issue == '40-2' and info.no == 16:
                    info.authors_ru = sstr(
                        "Спицын В.Г., Болотова Ю.А., Фан Нгок Хоанг, Буй Тхи Тху Чанг")
                elif info.issue == '40-5' and "Editorial" in title:
                    info.authors_en = None
                elif info.issue == '40-5' and info.no == 1:
                    info.authors_en = sstr(
                        "V.A. Soifer, O. Korotkova, S.N. Khonina, E.A. Shchepakina")
                elif info.issue == '40-5' and info.no == 4:
                    info.authors_en = sstr(
                        "Xi Chen, O. Korotkova")
                elif info.issue == '41-1' and info.no == 1:
                    info.authors_ru = sstr(
                        "Котляр В.В., Налимов А.Г., Стафеев С.С., О'Фаолейн Лим, Котляр М.В.")
                elif info.issue == '41-3' and info.no == 1:
                    info.authors_ru = sstr(
                        "Стафеев С.С., Налимов А.Г., О'Фаолейн Л., Котляр М.В.")
                elif info.issue == '42-6' and info.no == 18:
                    info.authors_ru = sstr(
                        "Кочегурова Е.А., У Д.")
                elif info.issue == '42-6' and info.no == 21:
                    info.authors_ru = None
                elif info.issue == '43-2' and info.no == 12:
                    info.authors_en = sstr(
                        "Thanh D.N.H., Prasath V.B.S., Son N.V., Hieu L.M.")
                elif info.issue == '43-2' and info.no == 20:
                    info.authors_en = sstr(
                        "Arhid K., Zakani F.R., Bouksim M., Sirbal B., Aboulfatah M., Gadi T.")
                elif info.issue == '43-3' and info.no == 13:
                    info.authors_en = sstr(
                        "Bettaieb A., Filali N., Filali T., Ben Aissia H.")
                elif info.issue == '44-3' and info.no == 7:
                    info.authors_en = sstr(
                        "Bettaieb A., Filali N., Filali T., Ben Aissia H.")
                elif info.issue == '45-1' and info.no == 10:
                    info.authors_en = sstr(
                        "Petrova O., Bulatov K., Arlazarov V.V., Arlazarov V.L.")
                elif info.issue == '45-4' and "От редакции" in title:
                    info.authors_ru = None
                elif info.issue == '45-4' and info.no == 6:
                    info.authors_ru = sstr("Стафеев С.С.")
                elif info.issue == '45-6' and info.no == 10:
                    info.authors_en = sstr(
                        "Rodiah, Madenda S., Susetianingtias D.T., Fitrianingsih, Adlina D., Arianty R.")
                elif info.issue == '46-1' and info.no == 4:
                    info.authors_en = sstr(
                        "Correa-Rojas N.A., Gallego-Ruiz R.D., Álvarez-Castaño M.I.")
                elif info.issue == '46-2' and info.no == 20:
                    info.authors_ru = None
                else:
                    print("!!!Parsing failed", info.issue,
                          info.no, info_str, word)

            break

        # HOT FIXES
        if info.issue == '36-1' and info.no == 14:
            info.title_ru = 'Метод расчёта зеркал для формирования заданных двумерных распределений освещённости'
            info.authors_ru = 'Бызов Е.В., Моисеев М.А., Досколович Л.Л.'
            return
        if info.issue == '37-4' and 'Боброва' in info.info_td.text:
            info.title_ru = 'Памяти С.Т. Боброва'
            info.authors_ru = None
            return

        # NO FIX
        if info.issue == '1' and 'Аннотации' in info.info_td.text:
            info.title_ru = 'Аннотации к сборнику'
            return
        if info.issue == '2' and 'Аннотации' in info.info_td.text:
            info.title_ru = 'Аннотации к сборнику «Компьютерная оптика», вып. 2. «Автоматизация проектирования и технологии» на русском и английском языках'
            return
        if (info.issue == '3' or info.issue == '4' or info.issue == '13' or info._issue.vol == 31 or info._issue.vol == 32 or info.issue == '33-1') and 'Аннотации' in info.info_td.text:
            info.title_ru = 'Аннотации'
            info.title_en = 'Abstracts'
            return
        if (info._issue.vol == 31 or info._issue.vol == 32) and 'Правила подготовки' in info.info_td.text:
            info.title_ru = 'Правила подготовки рукописей для журнала «Компьютерная оптика»'
            return
        if info.issue == '5' and 'Аннотации' in info.info_td.text:
            info.title_ru = 'Аннотации к сборнику «Компьютерная оптика» вып. 5 на русском и английском языках'
            return
        if info.issue == '34-3' and 'Микаэляна' in info.info_td.text:
            info.title_ru = 'Памяти Андрея Леоновича Микаэляна'
            return

    # Parse by regex (6-11, 16-30)
    else:
        info_str = sstr(info.info_td.text)

        # HOT FIXES
        if info._issue.vol == 24 and info.no == 2:
            info_str = re.sub(r'С\..?И Харитонов', 'С.И. Харитонов', info_str)
        if info._issue.vol == 9 and info.no == 6:
            info_str = info_str.replace('Е. К Завриева', 'Е.К. Завриева')
        if info._issue.vol == 8 and info.no == 1:
            info_str = info_str.replace('И.Н.Сисакян', 'И.Н. Сисакян')
            info_str = info_str.replace('В.А Сойфер', 'В.А. Сойфер')
        if info._issue.vol == 7 and info.no == 2:
            info_str = info_str.replace('СТ. Бобров', 'С.Т. Бобров')
        if info._issue.vol == 7 and info.no == 4:
            info_str = info_str.replace('СИ. Харитонов', 'С.И. Харитонов')
        if info._issue.vol == 7 and info.no == 15:
            info_str = info_str.replace('Ю.А, Михайлов', 'Ю.А. Михайлов')

        # Fix dots
        info_str = re.sub(r'\.([A-ZА-ЯЁ])', r'. \1', info_str)

        # Merge initials (three and two initials in separate cases since re.sub looks only once)
        info_str = re.sub(
            r'([A-ZА-ЯЁ][a-z]?\.) ([A-ZА-ЯЁ][a-z]?\.) ([A-ZА-ЯЁ][a-z]?\.)', r'\1\2\3', info_str)
        info_str = re.sub(
            r'([A-ZА-ЯЁ][a-z]?\.) ([A-ZА-ЯЁ][a-z]?\.)', r'\1\2', info_str)

        # Initials last
        if info._issue.vol == 16 or info._issue.vol == 21 or info._issue.vol > 24:
            items = re.findall(
                r"^(([A-ZА-ЯЁ]\w+ [A-ZА-ЯЁ][a-z]?\.([A-ZА-ЯЁ]\.)?,? ?)+)\.? ?(.+)$", info_str)
        # Initials first
        else:
            items = re.findall(
                r"^(([A-ZА-ЯЁ][a-z]?\.([A-ZА-ЯЁ][a-z]?\.)? [A-ZА-ЯЁ]\w+,? ?)+)\.? ?(.+)$", info_str)

        if len(items) > 0 and len(items[0]) > 3:
            title = sstr(items[0][3], True, True)
            authors = sstr(items[0][0])

            # Check locale
            if re.search(r'[А-ЯЁа-яё]', title) is None:
                info.title_en = title
                info.authors_en = authors
            else:
                info.title_ru = title
                info.authors_ru = authors

        # HOT FIXES
        if info.issue == '27' and info.no == 1:
            info.title_ru = sstr(
                'Микаэляну А.Л. - 80 лет')
            info.authors_ru = None
        elif info.issue == '27' and info.no == 2:
            info.title_ru = sstr(
                'Сойферу В.А. - 60 лет')
            info.authors_ru = None
        elif info.issue == '26' and info.no == 1:
            info.title_ru = sstr(
                'Академику Ю.И. Журавлеву - 70 лет')
            info.authors_ru = None
        elif info.issue == '26' and info.no == 15:
            info.title_ru = sstr(
                'Алгоритм многомерного гиперкомплексного ДПФ, реализуемый в кодах Гамильтона-Эйзенштейна')
            info.authors_ru = sstr(
                'Алиев М.В., Чичева М.А., Алиева М.Ф.')
        elif info.issue == '21' and info.no == 20:
            info.title_en = sstr(
                'Experimental investigation of multimode dispersionless beams')
            info.authors_en = sstr(
                'Vladimir S. Pavelyev, Michael Duparre, Barbara Luedge')
        elif info.issue == '21' and info.no == 33:
            info.title_en = sstr(
                'Matrix arithmetic based on Fibonacci matrices')
            info.authors_en = sstr('Alexey Stakhov')
        elif info.issue == '21' and info.no == 34:
            info.title_en = sstr(
                'Ternary mirror-symmetrical arithmetic and its application to digital signal processing')
            info.authors_en = sstr('Alexey Stakhov')
        elif info.issue == '20' and info.no == 14:
            info.title_en = sstr(
                'Laser beam characterization by means of diffractive optical correlation filters')
            info.authors_en = sstr(
                'V.S. Pavelyev, V.A. Soifer, M. Duparre,  B. Luedge')
        elif info.issue == '20' and info.no == 17:
            info.title_ru = sstr(
                'Гибридная рефракционно-дифракционная нулевая система для интерферометрического контроля светосильных асферических поверхностей')
            info.authors_ru = sstr(
                'А.Г. Полещук, Е.Г. Чурин, В.П. Корольков, Жан-Мишель Асфор')
        elif info.issue == '20' and info.no == 21:
            info.title_en = sstr(
                'The influence of the grain size of microstructure of the surface layer material of a hypersonic body on the properties of air plasma')
            info.authors_en = sstr('Oleg V. Minin, Igor V. Minin')
        elif info.issue == '20' and info.no == 26:
            info.title_ru = sstr(
                'Многофункциональная цифровая модель системы искажения и восстановления изображений')
            info.authors_ru = sstr(
                'А.В. Карнаухов, Н.С. Мерзляков, О.П. Милюкова')
        elif info.issue == '19' and info.no == 21:
            info.title_en = sstr(
                'Experimental selection of spatial Gauss-Laguerre modes')
            info.authors_en = sstr(
                'S.N. Khonina, R.V. Skidanov, V.V. Kotlyar, Y. Wang')
        elif info.issue == '19' and info.no == 22:
            info.title_ru = sstr(
                'Граничные структуры жидкости и голографические регистрирующие среды')
            info.authors_ru = sstr(
                'Ю.В. Аграфонов, А.Г. Балахчи, Т.В., Бирюлина, Ю.Н. Выговский, Я.С. Дорогобид, Л.Е. Кручинин, А.Н. Малов, Ф.Е. Ушаков, В.В. Черный')
        elif info.issue == '19' and info.no == 29:
            info.title_en = sstr(
                'Non-stability of mm-wave radar imaging of the car in dynamics')
            info.authors_en = sstr('I.V.Minin, O.V.Minin')
        elif info.issue == '19' and info.no == 37:
            info.title_ru = sstr(
                'Цифровые методы обработки изображений в задачах идентификации средневековых водяных знаков')
            info.authors_ru = sstr(
                'В.Н. Карнаухов, Н.С. Мерзляков, Э. Венгер, А. Хайдингер')
        elif info.issue == '18' and info.no == 8:
            info.title_en = sstr(
                'Phase reconstruction using a Zernike decomposition filter')
            info.authors_en = sstr(
                'S.N.Khonina, V.V. Kotlyar, V.A.Soifer, Y.Wang, D.Zhao')
        elif info.issue == '18' and info.no == 18:
            info.title_en = sstr(
                'Изготовление высокоэффективных ДОЭ с помощью полутоновых фотошаблонов на основе LDW-стекол')
            info.authors_en = sstr(
                'В.П.Корольков, А.И.Малышев, Н.Г.Никитин, А.Г.Полищук, А.А.Харисов, В.В.Черкашин, Ву Чак')
        # NO FIX
        elif info.issue == '10-11' and info.no == 3:
            info.title_en = sstr('Computer Optics and Its Development')
            info.authors_en = sstr('Yang-Xun, Yang-Xiao')
        elif info.issue == '9' and info.no == 2:
            info.title_ru = sstr(
                'Трехмерная реконструкция человеческого мозга')
            info.authors_ru = sstr('Р. Таллер, Л. Димитров, Э. Венджер')
            info.title_en = sstr('3D-Reconstruction of the Human Brain')
            info.authors_en = sstr('R. Thaller, L. Dimitrov, E. Wenger')
        elif info.issue == '8' and info.no == 2:
            info.title_ru = sstr(
                'Микроволновые киноформы, созданные компьютером')
            info.authors_ru = sstr('Н. Галлагер, Д. Свиней')
            info.title_en = sstr('Computer Generated Vicrowave Kinoforms')
            info.authors_en = sstr('N.C. Gallagher, D.W. Sweeney')
        elif 'Аннотации' in info_str:
            info.title_ru = sstr('Аннотации')
            info.title_en = sstr('Abstracts')
        elif ('Президиума' in info_str and 'Сойфер' not in info_str) or 'оформлению' in info_str or 'От составителей' in info_str or 'лет профессору' in info_str or 'Памяти' in info_str:
            info.title_ru = sstr(info_str, True, True)
        elif info.authors_ru is None and info.authors_en is None:
            print('Unparsable authors', info.no, info_str)
            pass

    return 1
