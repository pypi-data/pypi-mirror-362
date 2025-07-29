hello and welcome to the custombox module, in this module you can add custom messages
with custom commands and buttons, so your not forced on only "Ok", "Cancel", "Yes", "No"
and the others, you can put it custom example

import custombox

def hello_world():
print("Hello from a custom command!")

show_custombox(
title="my custom title",
message="my custom text",
buttons=[
{"text": "Say Hello", "command": hello_world},
{"text": "Download tismiy", "command": "download_tismiy"}
],
use_enhancer=False
)
