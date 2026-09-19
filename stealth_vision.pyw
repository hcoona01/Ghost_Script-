import keyboard
import threading
import requests
import base64
import io
import tkinter as tk
from PIL import ImageGrab
import ctypes 

# DPI awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# Cloud config
API_URL = "https://openrouter.ai/api/v1/chat/completions" 
API_KEY = "Khudki API key use kro" 

# List of reliable free vision models for fallback rotation
FREE_VISION_MODELS = [
    "nex-agi/nex-n2.5-pro:free",
    "inclusionai/ling-3.0-flash-vl:free",
    "google/gemma-4-26b-a4b-it:free",
    "google/gemma-4-31b-it:free",
    "qwen/qwen3.8-27b:free"
]

# Stealth overlay
class StealthOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True) 
        self.root.attributes("-topmost", True) 
        
        # Multitasking windows flags
        WS_EX_NOACTIVATE = 0x08000000
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, style | WS_EX_NOACTIVATE)
        
        # Invisible text background hack
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
        self.root.after(0, self._safe_log, msg)

    def _safe_log(self, msg):
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, msg)
        self.text.config(state=tk.DISABLED)
        self.text.config(fg='#cbcbcb') 
        self.is_visible = True

    def toggle(self):
        self.root.after(0, self._safe_toggle)

    def _safe_toggle(self):
        if self.is_visible:
            self.text.config(fg='#000000') # Hide
            self.is_visible = False
        else:
            self.text.config(fg='#cbcbcb') # Show
            self.is_visible = True

# Screen processor with automatic rate-limit failover
def process_screen(overlay):
    overlay.log("Scanning...")

    try:
        # Grab screenshot and compress to save API bandwidth
        ss = ImageGrab.grab()
        img_byte_arr = io.BytesIO()
        ss.convert('RGB').save(img_byte_arr, format='JPEG', quality=70)
        base64_str = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost", 
            "X-Title": "Vision Assistant"
        }

        # Iterate through the available free models if one fails or hits rate limits
        for index, model_name in enumerate(FREE_VISION_MODELS):
            short_name = model_name.split('/')[-1].split(':')[0]
            if index > 0:
                overlay.log(f"Retrying with {short_name}...")

            payload = {
                "model": model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Give ONLY the final correct answer option or short answer. No explanation, no extra words. Max 10 words."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_str}"}}
                        ]
                    }
                ]
            }
            
            try:
                response = requests.post(API_URL, headers=headers, json=payload, timeout=25)
                
                # If rate-limited (429) or bad gateway/overloaded (502/503), try next model
                if response.status_code in [429, 502, 503]:
                    continue 
                
                if response.status_code == 200:
                    res_data = response.json()
                    if 'choices' in res_data and len(res_data['choices']) > 0:
                        result = res_data['choices'][0]['message']['content']
                        overlay.log(result.strip())
                        return # Success, exit function
                else:
                    # Generic error fallback to next model
                    continue

            except (requests.exceptions.Timeout, requests.exceptions.RequestException):
                # Connection timeout or network blip, try next backup model
                continue
        
        # If the loop finishes without returning, all models failed
        overlay.log("All free models busy.")

    except Exception as e:
        overlay.log(f"Error: {str(e)[:30]}")

# Hotkeys
if __name__ == "__main__":
    ui = StealthOverlay()
    # Alt + 4 to capture and answer
    keyboard.add_hotkey('alt+4', lambda: threading.Thread(target=process_screen, args=(ui,), daemon=True).start())
    # Alt + 3 to toggle visibility manually
    keyboard.add_hotkey('alt+3', ui.toggle)
    ui.root.mainloop()
