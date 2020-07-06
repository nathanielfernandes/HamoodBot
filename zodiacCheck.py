
# Subprogram to determin Zodiac Sign 
def getZodiac(month, day):
    if (month == "mar"):
        if (day >= 21):
            result = 'Aries'
        else:
            result = 'Pisces'
    elif (month == "apr"):
        if (day >= 21):
            result = 'Taurus'
        else:
            result = 'Aries'
    elif (month == 'may'):
        if (day >= 22):
            result = 'Gemini'
        else:
            result = 'Taurus'
    elif (month == 'jun'):
        if (day >= 22):
            result = 'Cancer'
        else:
            result = 'Gemini'
    elif (month == 'jul'):
        if (day >= 24):
            result = 'Leo'
        else:
            result = 'Cancer'
    elif (month == 'aug'):
        if (day >= 24):
            result = 'Virgo'
        else:
            result = 'Leo'
    elif (month == 'sep'):
        if (day >= 24):
            result = 'Libra'
        else:
            result = 'Virgo'
    elif (month == 'oct'):
        if (day >= 24):
            result = 'Scorpio'
        else:
            result = 'Libra'
    elif (month == 'nov'):
        if (day >= 23):
            result = 'Sagittarus'
        else:
            result = 'Scorpio'
    elif (month == 'dec'):
        if (day >= 22):
            result = 'Capicorn'
        else:
            result = 'Sagittarus'
    elif (month == 'jan'):
        if (day >= 21):
            result = 'Aquarius'
        else:
            result = 'Capicorn'
    elif (month == 'feb'):
        if (day >= 20):
            result = 'Pisces'
        else:
            result = 'Aquarius'
    else:
        result = True
    return result

# Subprogram to determine compatibility
def getCompatibility(sign1, sign2):
    
    if (sign1 == "Aries") and (sign2 == "Aries"):
        compatibility = "71%"
    elif (sign1 == "Aries") and (sign2 == "Cancer"):
        compatibility = "42%"
    elif (sign1 == "Aries") and (sign2 == "Libra"):
        compatibility = "69%"
    elif (sign1 == "Aries") and (sign2 == "Capicorn"):
        compatibility = "43%"
    elif (sign1 == "Aries") and (sign2 == "Taurus"):
        compatibility = "67%"
    elif (sign1 == "Aries") and (sign2 == "Leo"):
        compatibility = "76%"
    elif (sign1 == "Aries") and (sign2 == "Scorpio"):
        compatibility = "38%"
    elif (sign1 == "Aries") and (sign2 == "Aquarius"):
        compatibility = "82%"
    elif (sign1 =="Aries") and (sign2 == "Gemini"):
        compatibility = "61%"
    elif (sign1 == "Aries") and (sign2 == "Virgo"):
        compatibility = "28%"
    elif (sign1 == "Aries") and (sign2 == "Sagittarus"):
        compatibility = "86%"
    elif (sign1 == "Aries") and (sign2 == "Pisces"):
        compatibility = "54%"
        
    elif (sign1 == "Taurus") and (sign2 == "Cancer"):
        compatibility = "95%"
    elif (sign1 == "Taurus") and (sign2 == "Libra"):
        compatibility = "52%"
    elif (sign1 == "Taurus") and (sign2 == "Capicorn"):
        compatibility = "80%"
    elif (sign1 == "Taurus") and (sign2 == "Taurus"):
        compatibility = "89%"
    elif (sign1 == "Taurus") and (sign2 == "Leo"):
        compatibility = "39%"
    elif (sign1 == "Taurus") and (sign2 == "Scorpio"):
        compatibility = "52%"
    elif (sign1 == "Taurus") and (sign2 == "Aquarius"):
        compatibility = "22%"
    elif (sign1 == "Taurus") and (sign2 == "Gemini"):
        compatibility = "29%"
    elif (sign1 == "Taurus") and (sign2 == "Virgo"):
        compatibility = "73%"
    elif (sign1 == "Taurus") and (sign2 == "Sagittarus"):
        compatibility = "36%"
    elif (sign1 == "Taurus") and (sign2 == "Pisces"):
        compatibility = "92%"
        
    elif (sign1 == "Gemini") and (sign2 == "Cancer"):
        compatibility = "26%"
    elif (sign1 == "Gemini") and (sign2 == "Libra"):
        compatibility = "47%"
    elif (sign1 == "Gemini") and (sign2 == "Capicorn"):
        compatibility = "27%"
    elif (sign1 == "Gemini") and (sign2 == "Leo"):
        compatibility = "87%"
    elif (sign1 == "Gemini") and (sign2 == "Scorpio"):
        compatibility = "12%"
    elif (sign1 == "Gemini") and (sign2 == "Aquarius"):
        compatibility = "81%"
    elif (sign1 == "Gemini") and (sign2 == "Gemini"):
        compatibility = "81%"
    elif (sign1 == "Gemini") and (sign2 == "Virgo"):
        compatibility = "47%"
    elif (sign1 == "Gemini") and (sign2 == "Sagittarus"):
        compatibility = "94%"
    elif (sign1 == "Gemini") and (sign2 == "Pisces"):
        compatibility = "21%"
    
    elif (sign1 == "Cancer") and (sign2 == "Cancer"):
        compatibility = "90%"   
    elif (sign1 == "Cancer") and (sign2 == "Libra"):
        compatibility = "26%"   
    elif (sign1 == "Cancer") and (sign2 == "Capicorn"):
        compatibility = "75%"   
    elif (sign1 == "Cancer") and (sign2 == "Leo"):
        compatibility = "35%"   
    elif (sign1 == "Cancer") and (sign2 == "Scorpio"):
        compatibility = "89%"   
    elif (sign1 == "Cancer") and (sign2 == "Aquarius"):
        compatibility = "24%"
    elif (sign1 == "Cancer") and (sign2 == "Virgo"):
        compatibility = "79%"   
    elif (sign1 == "Cancer") and (sign2 == "Sagittarus"):
        compatibility = "28%"   
    elif (sign1 == "Cancer") and (sign2 == "Pisces"):
        compatibility = "75%" 
        
    elif (sign1 == "Leo") and (sign2 == "Libra"):
        compatibility = "75%" 
    elif (sign1 == "Leo") and (sign2 == "Capicorn"):
        compatibility = "30%" 
    elif (sign1 == "Leo") and (sign2 == "Leo"):
        compatibility = "82%" 
    elif (sign1 == "Leo") and (sign2 == "Scorpio"):
        compatibility = "29%" 
    elif (sign1 == "Leo") and (sign2 == "Aquarius"):
        compatibility = "86%" 
    elif (sign1 == "Leo") and (sign2 == "Virgo"):
        compatibility = "30%" 
    elif (sign1 == "Leo") and (sign2 == "Sagittarus"):
        compatibility = "86%" 
    elif (sign1 == "Leo") and (sign2 == "Pisces"):
        compatibility = "23%" 
        
    elif (sign1 == "Virgo") and (sign2 == "Libra"):
        compatibility = "28%" 
    elif (sign1 == "Virgo") and (sign2 == "Capicorn"):
        compatibility = "81%" 
    elif (sign1 == "Virgo") and (sign2 == "Scorpio"):
        compatibility = "74%" 
    elif (sign1 == "Virgo") and (sign2 == "Aquarius"):
        compatibility = "20%" 
    elif (sign1 == "Virgo") and (sign2 == "Virgo"):
        compatibility = "62%" 
    elif (sign1 == "Virgo") and (sign2 == "Sagittarus"):
        compatibility = "36%" 
    elif (sign1 == "Virgo") and (sign2 == "Pisces"):
        compatibility = "72%" 

    elif (sign1 == "Libra") and (sign2 == "Libra"):
        compatibility = "66%" 
    elif (sign1 == "Libra") and (sign2 == "Capicorn"):
        compatibility = "34%" 
    elif (sign1 == "Libra") and (sign2 == "Scorpio"):
        compatibility = "35%" 
    elif (sign1 == "Libra") and (sign2 == "Aquarius"):
        compatibility = "62%" 
    elif (sign1 == "Libra") and (sign2 == "Sagittarus"):
        compatibility = "84%" 
    elif (sign1 == "Libra") and (sign2 == "Pisces"):
        compatibility = "28%" 
        
    elif (sign1 == "Scorpio") and (sign2 == "Capicorn"):
        compatibility = "61%" 
    elif (sign1 == "Scorpio") and (sign2 == "Scorpio"):
        compatibility = "74%" 
    elif (sign1 == "Scorpio") and (sign2 == "Aquarius"):
        compatibility = "31%" 
    elif (sign1 == "Scorpio") and (sign2 == "Sagittarus"):
        compatibility = "44%" 
    elif (sign1 == "Scorpio") and (sign2 == "Pisces"):
        compatibility = "92%" 

    elif (sign1 == "Sagittarus") and (sign2 == "Capicorn"):
        compatibility = "22%" 
    elif (sign1 == "Sagittarus") and (sign2 == "Aquarius"):
        compatibility = "82%" 
    elif (sign1 == "Sagittarus") and (sign2 == "Sagittarus"):
        compatibility = "79%" 
    elif (sign1 == "Sagittarus") and (sign2 == "Pisces"):
        compatibility = "54%" 
    
    elif (sign1 == "Capicorn") and (sign2 == "Capicorn"):
        compatibility = "67%" 
    elif (sign1 == "Capicorn") and (sign2 == "Aquarius"):
        compatibility = "22%" 
    elif (sign1 == "Capicorn") and (sign2 == "Pisces"):
        compatibility = "78%" 

    elif (sign1 == "Aquarius") and (sign2 == "Aquarius"):
        compatibility = "68%" 
    elif (sign1 == "Aquarius") and (sign2 == "Pices"):
        compatibility = "34%" 

    elif (sign1 == "Pisces") and (sign2 == "Pisces"):
        compatibility = "83%" 




    elif (sign2 == "Aries") and (sign1 == "Aries"):
        compatibility = "71%"
    elif (sign2 == "Aries") and (sign1 == "Cancer"):
        compatibility = "42%"
    elif (sign2 == "Aries") and (sign1 == "Libra"):
        compatibility = "69%"
    elif (sign2 == "Aries") and (sign1 == "Capicorn"):
        compatibility = "43%"
    elif (sign2 == "Aries") and (sign1 == "Taurus"):
        compatibility = "67%"
    elif (sign2 == "Aries") and (sign1 == "Leo"):
        compatibility = "76%"
    elif (sign2 == "Aries") and (sign1 == "Scorpio"):
        compatibility = "38%"
    elif (sign2 == "Aries") and (sign1 == "Aquarius"):
        compatibility = "82%"
    elif (sign2 =="Aries") and (sign1 == "Gemini"):
        compatibility = "61%"
    elif (sign2 == "Aries") and (sign1 == "Virgo"):
        compatibility = "28%"
    elif (sign2 == "Aries") and (sign1 == "Sagittarus"):
        compatibility = "86%"
    elif (sign2 == "Aries") and (sign1 == "Pisces"):
        compatibility = "54%"
        
    elif (sign2 == "Taurus") and (sign1 == "Cancer"):
        compatibility = "95%"
    elif (sign2 == "Taurus") and (sign1 == "Libra"):
        compatibility = "52%"
    elif (sign2 == "Taurus") and (sign1 == "Capicorn"):
        compatibility = "80%"
    elif (sign2 == "Taurus") and (sign1 == "Taurus"):
        compatibility = "89%"
    elif (sign2 == "Taurus") and (sign1 == "Leo"):
        compatibility = "39%"
    elif (sign2 == "Taurus") and (sign1 == "Scorpio"):
        compatibility = "52%"
    elif (sign2 == "Taurus") and (sign1 == "Aquarius"):
        compatibility = "22%"
    elif (sign2 == "Taurus") and (sign1 == "Gemini"):
        compatibility = "29%"
    elif (sign2 == "Taurus") and (sign1 == "Virgo"):
        compatibility = "73%"
    elif (sign2 == "Taurus") and (sign1 == "Sagittarus"):
        compatibility = "36%"
    elif (sign2 == "Taurus") and (sign1 == "Pisces"):
        compatibility = "92%"
        
    elif (sign2 == "Gemini") and (sign1 == "Cancer"):
        compatibility = "26%"
    elif (sign2 == "Gemini") and (sign1 == "Libra"):
        compatibility = "47%"
    elif (sign2 == "Gemini") and (sign1 == "Capicorn"):
        compatibility = "27%"
    elif (sign2 == "Gemini") and (sign1 == "Leo"):
        compatibility = "87%"
    elif (sign2 == "Gemini") and (sign1 == "Scorpio"):
        compatibility = "12%"
    elif (sign2 == "Gemini") and (sign1 == "Aquarius"):
        compatibility = "81%"
    elif (sign2 == "Gemini") and (sign1 == "Gemini"):
        compatibility = "81%"
    elif (sign2 == "Gemini") and (sign1 == "Virgo"):
        compatibility = "47%"
    elif (sign2 == "Gemini") and (sign1 == "Sagittarus"):
        compatibility = "94%"
    elif (sign2 == "Gemini") and (sign1 == "Pisces"):
        compatibility = "21%"
    
    elif (sign2 == "Cancer") and (sign1 == "Cancer"):
        compatibility = "90%"   
    elif (sign2 == "Cancer") and (sign1 == "Libra"):
        compatibility = "26%"   
    elif (sign2 == "Cancer") and (sign1 == "Capicorn"):
        compatibility = "75%"   
    elif (sign2 == "Cancer") and (sign1 == "Leo"):
        compatibility = "35%"   
    elif (sign2 == "Cancer") and (sign1 == "Scorpio"):
        compatibility = "89%"   
    elif (sign2 == "Cancer") and (sign1 == "Aquarius"):
        compatibility = "24%"
    elif (sign2 == "Cancer") and (sign1 == "Virgo"):
        compatibility = "79%"   
    elif (sign2 == "Cancer") and (sign1 == "Sagittarus"):
        compatibility = "28%"   
    elif (sign2 == "Cancer") and (sign1 == "Pisces"):
        compatibility = "75%" 
        
    elif (sign2 == "Leo") and (sign1 == "Libra"):
        compatibility = "75%" 
    elif (sign2 == "Leo") and (sign1 == "Capicorn"):
        compatibility = "30%" 
    elif (sign2 == "Leo") and (sign1 == "Leo"):
        compatibility = "82%" 
    elif (sign2 == "Leo") and (sign1 == "Scorpio"):
        compatibility = "29%" 
    elif (sign2 == "Leo") and (sign1 == "Aquarius"):
        compatibility = "86%" 
    elif (sign2 == "Leo") and (sign1 == "Virgo"):
        compatibility = "30%" 
    elif (sign2 == "Leo") and (sign1 == "Sagittarus"):
        compatibility = "86%" 
    elif (sign2 == "Leo") and (sign1 == "Pisces"):
        compatibility = "23%" 
        
    elif (sign2 == "Virgo") and (sign1 == "Libra"):
        compatibility = "28%" 
    elif (sign2 == "Virgo") and (sign1 == "Capicorn"):
        compatibility = "81%" 
    elif (sign2 == "Virgo") and (sign1 == "Scorpio"):
        compatibility = "74%" 
    elif (sign2 == "Virgo") and (sign1 == "Aquarius"):
        compatibility = "20%" 
    elif (sign2 == "Virgo") and (sign1 == "Virgo"):
        compatibility = "62%" 
    elif (sign2 == "Virgo") and (sign1 == "Sagittarus"):
        compatibility = "36%" 
    elif (sign2 == "Virgo") and (sign1 == "Pisces"):
        compatibility = "72%" 

    elif (sign2 == "Libra") and (sign1 == "Libra"):
        compatibility = "66%" 
    elif (sign2 == "Libra") and (sign1 == "Capicorn"):
        compatibility = "34%" 
    elif (sign2 == "Libra") and (sign1 == "Scorpio"):
        compatibility = "35%" 
    elif (sign2 == "Libra") and (sign1 == "Aquarius"):
        compatibility = "62%" 
    elif (sign2 == "Libra") and (sign1 == "Sagittarus"):
        compatibility = "84%" 
    elif (sign2 == "Libra") and (sign1 == "Pisces"):
        compatibility = "28%" 
        
    elif (sign2 == "Scorpio") and (sign1 == "Capicorn"):
        compatibility = "61%" 
    elif (sign2 == "Scorpio") and (sign1 == "Scorpio"):
        compatibility = "74%" 
    elif (sign2 == "Scorpio") and (sign1 == "Aquarius"):
        compatibility = "31%" 
    elif (sign2 == "Scorpio") and (sign1 == "Sagittarus"):
        compatibility = "44%" 
    elif (sign2 == "Scorpio") and (sign1 == "Pisces"):
        compatibility = "92%" 

    elif (sign2 == "Sagittarus") and (sign1 == "Capicorn"):
        compatibility = "22%" 
    elif (sign2 == "Sagittarus") and (sign1 == "Aquarius"):
        compatibility = "82%" 
    elif (sign2 == "Sagittarus") and (sign1 == "Sagittarus"):
        compatibility = "79%" 
    elif (sign2 == "Sagittarus") and (sign1 == "Pisces"):
        compatibility = "54%" 
    
    elif (sign2 == "Capicorn") and (sign1 == "Capicorn"):
        compatibility = "67%" 
    elif (sign2 == "Capicorn") and (sign1 == "Aquarius"):
        compatibility = "22%" 
    elif (sign2 == "Capicorn") and (sign1 == "Pisces"):
        compatibility = "78%" 

    elif (sign2 == "Aquarius") and (sign1 == "Aquarius"):
        compatibility = "68%" 
    elif (sign2 == "Aquarius") and (sign1 == "Pices"):
        compatibility = "34%" 

    elif (sign2 == "Pisces") and (sign1 == "Pisces"):
        compatibility = "83%"        
        
    return compatibility
