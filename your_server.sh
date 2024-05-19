#!/bin/sh
#
# DON'T EDIT THIS!
#
# CodeCrafters uses this file to test your code. Don't make any changes here!
#
# DON'T EDIT THIS!
exec pipenv run python3 -m app.main "$@"
hex_string = "1f8b0800a8f0486602ffcbcbcc0600065757d303000000"  # Example hex string
decoded_string = ''.join([chr(int(hex_string[i:i+2], 16)) for i in range(0, len(hex_string), 2)])
print("Decoded String:", decoded_string)