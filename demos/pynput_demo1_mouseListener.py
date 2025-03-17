from pynput import mouse
import time

# the mouse move handler will get passed the screen space coordinates that the mouse
# has moved to,
# you may notice that all mouse callbacks will give you the mouse position
def on_mouse_move(mouse_position_x, mouse_position_y):
    print("The mouse has moved to (%s, %s)"%(mouse_position_x, mouse_position_y))

# so the mouse scroll callback will give you 2 sets of scroll changes, one for the x
# axis and one for the y. Most of the time the one you care about is the y axis change
def on_mouse_scroll(mouse_position_x, mouse_position_y, scroll_x_change, scroll_y_change):
    if scroll_x_change < 0:
        print("user is scrolling to the left")
    elif scroll_x_change > 0:
        print("user is scrolling to the right")
    if scroll_y_change > 0:
        print("user is scrolling up the page")
    elif scroll_y_change < 0:
        print("user is scrolling down the page")
        print("scroll change deltas: ", scroll_x_change, scroll_y_change)

# the mouse click callback will give you the button pressed and its status, the
# callback will be triggered once when the button is pushed and again when released
# the is_pressed will tell you which state it's in
# there are several types of buttons it can recognize, but for the most part
# you'll just need the main 3: left, right and middle
def on_mouse_click(mouse_position_x, mouse_position_y, button, is_pressed):
    # example of how to listen for a specific button
    if button == mouse.Button.middle and is_pressed:
        print("middle mouse button pressed! it's special!")
    else:
        print("Mouse button pressed: ", button)
        print("Mouse button is pressed?: ", is_pressed)

# create a listener and setup our call backs
mouse_listener = mouse.Listener(
        on_move=on_mouse_move,
        on_scroll=on_mouse_scroll,
        on_click=on_mouse_click)

# start the listener
print("starting the mouse listener, will be active for 5 seconds...")
mouse_listener.start()
# let the main thread sleep for 5 seconds, then stop the listener
time.sleep(5)
print("Time's up, stopping the mouse listener")
mouse_listener.stop()
mouse_listener.join()

