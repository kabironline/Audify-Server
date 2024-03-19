# Write a function that checks if a given string is valid against
# sql injection attacks and returns True or False.
def validate_string(string):
    if string == None:
        return False
    if string == "":
        return False
    if string == " ":
        return False
