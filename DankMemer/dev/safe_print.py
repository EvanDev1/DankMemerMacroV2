import json

def safe_print(obj):
    # Safely print things without utf-8 errors
    try:
        print(obj.encode('ascii', 'backslashreplace').decode('ascii'))
    except UnicodeEncodeError as e:
        print(f"UnicodeEncodeError: {e}")