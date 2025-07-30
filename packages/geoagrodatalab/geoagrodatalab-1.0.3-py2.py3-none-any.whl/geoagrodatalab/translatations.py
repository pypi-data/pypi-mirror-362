#############################
# TRANSLATIONS 
#############################


from .language import translate_dict

def translate(string, language):

    try:
        return translate_dict[string][language]
    except:
        return "Unknown"