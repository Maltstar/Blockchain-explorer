from flask import Markup
from router import manage_hyperlink


#################################################
#   Format Response to HTML Elements Functions
#################################################

# dynamically format the key/value pair of dict as html elements
# """ Example of Response:
# {'hash': '51e950fb5dae48e96b3e674205b312c05f154c4077ec22adbf15ad445ff1e833',
#  'block': 1687289,
#  'index': 0,
#  'timestamp': 1655137287,
#  'confirmations': 2,
#  'fees': -2.49347601,
#  'total_input': None,
#  'inputs': [], 
#  'total_output': 2.49347601,
#  'outputs': [
#      {'addr': 'XmzfivrzYQ7B7oBMZKwPRdhjB1iNvX71XZ',
#       'amount': 1.10460988,
#       'script': '76a9147c086eada12bdb10a265c16c08a7ae87366bd48188ac'},
#      {'addr': 'XoDo3w4ZUqn93uL3FeRNb9fgfXvgg7BvDC',
#       'amount': 1.27775684,
#       'script': '76a914897c151a6aa235b7880fb7d34dacaca178ca039588ac'},
#      {'addr': 'Xr421hEMiXCt67RC6K48jPR89mZMF5a7wD',
#       'amount': 0.11110929,
#       'script': '76a914a88b1eab808c8341fb2cbe2af192c76cab7a6d4b88ac'}
#       ]
# } """
def format_results(my_crypto_dict,coin,operator=""):

    result = ""
    
    # the input data are in form of a dictionary
    # value are either single element, a dictionary or a list of dictionary
    for key,value in my_crypto_dict.items():
            result += Markup("<br>")
            #print(result)
            #1 value the element is a list 
            if str(type(value)) == "<class 'list'>":
                result += Markup("<br> <strong>{0}:</strong> <br>".format(key))
                #print(result)
                # parsing each element of the list
                for element in value:
                    # format for each element of the list
                    result += Markup("<br>")
                    # so far result on the list have been only dictionnary but testing to be sure
                    if str(type(element)) == "<class 'dict'>":
                        for sub_key,sub_value in element.items():
                        # create an html element with all keys witin value
                            if str(type(sub_value)) == "<class 'dict'>":
                                result += Markup("<br> <strong >{0}:</strong>".format(sub_key))
                                for under_key,under_value in sub_value.items():
                                    result += manage_hyperlink(under_key,coin,under_value)
                            else:
                                result += manage_hyperlink(sub_key,coin,sub_value)
            #2- value is a dictionary 
            elif str(type(value)) == "<class 'dict'>":
                # parsing it
                for under_key,under_value in sub_value.items():
                    result += manage_hyperlink(under_key,coin,under_value)
            #3- value is a single element 
            else:
                result += Markup('<br> <strong>{0}:</strong> {1} <br>'.format(key,value))
                #print(result)

    return result