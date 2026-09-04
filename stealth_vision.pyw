import keyboard
import threading
import requests
import base64
import io
import tkinter as tk
from PIL import ImageGrab
import ctypes 

#dpi awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

#cloud congif
API_URL = "https://openrouter.ai/api/v1/chat/completions" 

#key bhai saab
API_KEY = "Your Api Key" 

#model bhai saab
MODEL = "openrouter/free" 

#stealth overlay
class StealthOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True) 
        self.root.attributes("-topmost", True) 
        
        #Multitasking
        WS_EX_NOACTIVATE = 0x08000000
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, style | WS_EX_NOACTIVATE)
        
       #ghost gayab invisible
        self.root.attributes("-alpha", 1.0) 
        self.root.wm_attributes("-transparentcolor", '#000000') 
        
        w, h = 300, 100 
        x = self.root.winfo_screenwidth() - w - 20
        y = self.root.winfo_screenheight() - h - 60 
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.configure(bg='#000000') 
        
        # HD Font
        self.text = tk.Text(self.root, wrap=tk.WORD, bg='#000000', fg='#000000', 
                           font=("Segoe UI", 7, "bold"), borderwidth=0, highlightthickness=0)
        self.text.pack(expand=True, fill='both', padx=5, pady=5)
        
        self.is_visible = False

    def log(self, msg):
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, msg)
        self.text.config(state=tk.DISABLED)
        # Result aane par text visible
        self.text.config(fg='#cbcbcb') 
        self.is_visible = True

    def toggle(self):
        if self.is_visible:
            self.text.config(fg='#000000') # Gayab
            self.is_visible = False
        else:
            self.text.config(fg='#cbcbcb') # Wapas visible
            self.is_visible = True

#brain
def process_screen(overlay):
    if not overlay.is_visible:
        overlay.log("Scan")

    try:
        ss = ImageGrab.grab()
        img_byte_arr = io.BytesIO()
        ss.save(img_byte_arr, format='PNG')
        base64_str = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Give ONLY the final correct answer option. No explanation, no extra words. Max 10 words."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_str}"}}
                    ]
                }
            ]
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=45)
        if response.status_code == 200:
            result = response.json()['choices'][0]['message']['content']
            overlay.log(result.strip())
        else:
            # Detailed Error handling 
            error_msg = response.json().get('error', {}).get('message', 'Unknown Error')
            overlay.log(f"API Error {response.status_code}: {error_msg[:40]}...")

    except Exception as e:
        overlay.log("Connection Failed.")

#hotieeee key binds
if __name__ == "__main__":
    ui = StealthOverlay()
    keyboard.add_hotkey('alt+4', lambda: threading.Thread(target=process_screen, args=(ui,), daemon=True).start())
    keyboard.add_hotkey('alt+3', ui.toggle)
    ui.root.mainloop()