__author__ = 'django'
import re
date = 'date'
city = 'city'
univers = 'univers'
real = {}
analyzed = {}
s = "(('23.2.1991', [('1991', 27), ('1992', 19), ('1990', 10)]), ('ОГУ\r\n', [('ОГУ\r\n', 18), ('ОГАУ\r\n', 3), ('ОГПУ', 1)]), ('Оренбург', [['Оренбург', 122], (0, 23), ['Москва', 11]]), 78358450)"

p = re.compile('') # тут закидка в именованные словари!