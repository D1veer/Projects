import xlrd
import arabic_reshaper
from bidi.algorithm import get_display





for i in range(worksheet.nrows):
    reshaped_text = arabic_reshaper.reshape(worksheet.cell_value(i, 0))    
    bidi_text = get_display(reshaped_text)  
    print(f"{bidi_text} : ", end=" ")
    reshaped_text2 = arabic_reshaper.reshape(worksheet.cell_value(i, 2))    
    bidi_text2 = get_display(reshaped_text2)  
    print(bidi_text2)
    newlist.update({f"{bidi_text}": f"{bidi_text2}"})
print(newlist)    