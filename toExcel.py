from openpyxl import Workbook
w = Workbook()

sheet = w.active

w.save("C:/Users/qkrth/newsInput/xlsx")
w.close()

