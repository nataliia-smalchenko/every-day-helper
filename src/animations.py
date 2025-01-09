from prompt_toolkit import print_formatted_text, HTML
import time
import sys

def running_text_animation():
    greeting = "     Welcome to the assistant bot!     "

    for i in range(len(greeting) * 1):
        display_text = (greeting * 1)[i:i+len(greeting)]
        
        print_formatted_text(HTML(f'<cyan>{display_text}</cyan>'), end='', flush=True)
        
        time.sleep(0.05)
        
        sys.stdout.write('\r')
        
    print() 
