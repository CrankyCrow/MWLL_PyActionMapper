from pynput import keyboard, mouse
import time

class KeyboardTracker:
    def __init__(self):
        self.keyPressed = ""

    def on_press(self, key):
        keyDir = keyboard.Key
        # print(type(key))
        # convert key names to actionmapper-friendly terms
        try:
            print(f"Key pressed: {key}", key.vk)
            if key == "\\":
                self.keyPressed = "backslash"
            elif key.char == "`":
                self.keyPressed = "tilde"
            elif key.char == "'":
                self.keyPressed = "apostrophe"
            elif key.char == ";":
                self.keyPressed = "semicolon"
            elif key.char == ".":
                self.keyPressed = "period"
            elif key.char == ",":
                self.keyPressed = "comma"
            elif key.char == "/":
                self.keyPressed = "slash"
            elif key.char == "-":
                self.keyPressed = "minus"
            elif key.char == "=":
                self.keyPressed = "equals"
            elif key.char == "[":
                self.keyPressed = "lbracket"
            elif key.char == "]":
                self.keyPressed = "rbracket"
            elif hasattr(key, "vk") and key.vk == 96:
                self.keyPressed = "np_0"
            elif hasattr(key, "vk") and key.vk == 97:
                self.keyPressed = "np_1"
            elif hasattr(key, "vk") and key.vk == 98:
                self.keyPressed = "np_2"
            elif hasattr(key, "vk") and key.vk == 99:
                self.keyPressed = "np_3"
            elif hasattr(key, "vk") and key.vk == 100:
                self.keyPressed = "np_4"
            elif hasattr(key, "vk") and key.vk == 101:
                self.keyPressed = "np_5"
            elif hasattr(key, "vk") and key.vk == 102:
                self.keyPressed = "np_6"
            elif hasattr(key, "vk") and key.vk == 103:
                self.keyPressed = "np_7"
            elif hasattr(key, "vk") and key.vk == 104:
                self.keyPressed = "np_8"
            elif hasattr(key, "vk") and key.vk == 105:
                self.keyPressed = "np_9"
            elif hasattr(key, "vk") and key.vk == 106:
                self.keyPressed = "np_multiply"
            elif hasattr(key, "vk") and key.vk == 107:
                self.keyPressed = "np_add"
            elif hasattr(key, "vk") and key.vk == 109:
                self.keyPressed = "np_subtract"
            elif hasattr(key, "vk") and key.vk == 110:
                self.keyPressed = "np_period"
            elif hasattr(key, "vk") and key.vk == 111:
                self.keyPressed = "np_divide"
            else:
                self.keyPressed = key.char
        except AttributeError:
            print(f"Key pressed: {key}")
            if key is keyDir.enter:
                # ignoring "np_enter", as it seems vk numbers for both "enter" and "np_enter" are the same?
                self.keyPressed = "enter"
            elif key is keyDir.cmd:
                self.keyPressed = "lwin"
            elif key is keyDir.print_screen:
                self.keyPressed = "print"
            elif key is keyDir.pause:
                self.keyPressed = "pause"
            elif key is keyDir.scroll_lock:
                self.keyPressed = "scrolllock"
            elif key is keyDir.num_lock:
                self.keyPressed = "numlock"
            elif key is keyDir.space:
                self.keyPressed = "space"
            elif key is keyDir.alt_r or key is keyDir.alt_gr:
                self.keyPressed = "ralt"
            elif key is keyDir.alt_l:
                self.keyPressed = "lalt"
            elif key is keyDir.ctrl_r:
                self.keyPressed = "rctrl"
            elif key is keyDir.ctrl_l:
                self.keyPressed = "lctrl"
            elif key is keyDir.shift_r:
                self.keyPressed = "rshift"
            elif key is keyDir.shift_l:
                self.keyPressed = "lshift"
            elif key is keyDir.page_up:
                self.keyPressed = "pgup"
            elif key is keyDir.page_down:
                self.keyPressed = "pgdn"
            elif key is keyDir.end:
                self.keyPressed = "end"
            elif key is keyDir.delete:
                self.keyPressed = "delete"
            elif key is keyDir.home:
                self.keyPressed = "home"
            elif key is keyDir.insert:
                self.keyPressed = "insert"
            elif key is keyDir.tab:
                self.keyPressed = "tab"
            elif key is keyDir.f1:
                self.keyPressed = "f1"
            elif key is keyDir.f2:
                self.keyPressed = "f2"
            elif key is keyDir.f3:
                self.keyPressed = "f3"
            elif key is keyDir.f4:
                self.keyPressed = "f4"
            elif key is keyDir.f5:
                self.keyPressed = "f5"
            elif key is keyDir.f6:
                self.keyPressed = "f6"
            elif key is keyDir.f7:
                self.keyPressed = "f7"
            elif key is keyDir.f8:
                self.keyPressed = "f8"
            elif key is keyDir.f9:
                self.keyPressed = "f9"
            elif key is keyDir.f10:
                self.keyPressed = "f10"
            elif key is keyDir.f11:
                self.keyPressed = "f11"
            elif key is keyDir.f12:
                self.keyPressed = "f12"
            elif key is keyDir.f13:
                self.keyPressed = "f13"
            elif key is keyDir.f14:
                self.keyPressed = "f14"
            elif key is keyDir.f15:
                self.keyPressed = "f15"
            elif key is keyDir.f16:
                self.keyPressed = "f16"
            elif key is keyDir.f17:
                self.keyPressed = "f17"
            elif key is keyDir.f18:
                self.keyPressed = "f18"
            elif key is keyDir.f19:
                self.keyPressed = "f19"
            elif key is keyDir.f20:
                self.keyPressed = "f20"
            elif key is keyDir.left:
                self.keyPressed = "left"
            elif key is keyDir.right:
                self.keyPressed = "right"
            elif key is keyDir.up:
                self.keyPressed = "up"
            elif key is keyDir.down:
                self.keyPressed = "down"
            elif key is keyDir.caps_lock:
                self.keyPressed = "capslock"

        print(f"Converted key name to {self.keyPressed}")
        return False

    def get_keyPressed(self):
        return self.keyPressed

    def start_tracking(self):
        kListener = keyboard.Listener(on_press=self.on_press)
        kListener.start()
        kListener.join()

class MouseTracker:
    def __init__(self):
        self.last_time = time.time()
        self.last_pos = mouse.Controller().position
        self.moveCoordsList_x = []
        self.moveCoordsList_y = []
        self.buttonPressed = ""

    def on_move(self, x, y):
        print(f"Pointer moved {(x, y)}")
        current_time = time.time()
        current_pos = [x, y]
        time_diff = current_time - self.last_time
        pos_diff = [current_pos[0] - self.last_pos[0], current_pos[1] - self.last_pos[1]]
        self.moveCoordsList_x.append(current_pos[0])
        self.moveCoordsList_y.append(current_pos[1])
        print(f"Time since last move: {time_diff:.2f}s\nMoved: {pos_diff[0]}px, {pos_diff[1]}px")
        self.last_time = current_time
        self.last_pos = current_pos

    def on_click(self, x, y, button, pressed):
        print("{0} {1} at {2}".format(button, 'Pressed' if pressed else 'Released', (x, y)))
        if button == mouse.Button.right:
            self.buttonPressed = "mouse2"
        elif button == mouse.Button.left:
            self.buttonPressed = "mouse1"
        elif button == mouse.Button.middle:
            self.buttonPressed = "mouse3"
        elif button == mouse.Button.x1:
            self.buttonPressed = "mouse4"
        elif button == mouse.Button.x2:
            self.buttonPressed = "mouse5"
        elif button == mouse.Button.x3:
            self.buttonPressed = "mouse6"

    def get_buttonPressed(self):
        return self.buttonPressed

    def on_scroll(self, x, y, dx, dy):
        print(f"Scrolled {(dx, dy)} at {(x, y)}")
        if dy > 0:
            self.buttonPressed = "mwheel_up"
        elif dy < 0:
            self.buttonPressed = "mwheel_down"

    def get_larger_moveAxis(self):
        try:
            max_moveAxis_x = max(self.moveCoordsList_x)
            min_moveAxis_x = min(self.moveCoordsList_x)
            max_moveAxis_y = max(self.moveCoordsList_y)
            min_moveAxis_y = min(self.moveCoordsList_y)
            if (max_moveAxis_x - min_moveAxis_x) > (max_moveAxis_y - min_moveAxis_y):
                print("mouse movement on x-axis detected")
                return "maxis_x"
            elif (max_moveAxis_y - min_moveAxis_y) > (max_moveAxis_x - min_moveAxis_x):
                print("mouse movement on y-axis detected")
                return "maxis_y"
            elif (max_moveAxis_y - min_moveAxis_y) == (max_moveAxis_x - min_moveAxis_x) and (
                    max_moveAxis_x - min_moveAxis_x) == (max_moveAxis_y - min_moveAxis_y):
                print("no input detected")
                return "none"

        except ValueError:
            print("no input detected")
            return "none"

    def start_tracking(self, waittime):
        mListener = mouse.Listener(on_move=self.on_move, on_scroll=self.on_scroll, on_click=self.on_click)
        mListener.start()
        time.sleep(waittime)
        mListener.stop()
        mListener.join()

