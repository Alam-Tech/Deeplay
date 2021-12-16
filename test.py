from pynput import keyboard

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        # print('special key {0} pressed'.format(key))
        if key == key.up:
            print('1')
        elif key == key.right:
            print('2')
        elif key == key.left:
            print('0')

def on_release(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

print('Hello, this is key listener!')
choice = input('Enter \'yes\' to continue: ')
if choice == 'yes':    
# Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
print('Thank you!')