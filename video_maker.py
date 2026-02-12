import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading
import os
import sys

class VideoMakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("簡易動画作成ツール")
        self.root.geometry("600x450")
        
        # スタイル設定
        style = ttk.Style()
        style.theme_use('clam')
        
        # 変数
        self.audio_path = tk.StringVar()
        self.image_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.status_var = tk.StringVar(value="準備完了")
        self.is_processing = False

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # タイトル
        title_label = ttk.Label(main_frame, text="画像と音声から動画を作成", font=("Meiryo", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # 音声ファイル選択
        ttk.Label(main_frame, text="1. 音声ファイルを選択 (mp3, wav, etc.)").pack(anchor=tk.W)
        audio_frame = ttk.Frame(main_frame)
        audio_frame.pack(fill=tk.X, pady=(5, 15))
        ttk.Entry(audio_frame, textvariable=self.audio_path).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(audio_frame, text="参照...", command=self.select_audio).pack(side=tk.RIGHT)

        # 画像ファイル選択
        ttk.Label(main_frame, text="2. 画像ファイルを選択 (jpg, png, etc.)").pack(anchor=tk.W)
        image_frame = ttk.Frame(main_frame)
        image_frame.pack(fill=tk.X, pady=(5, 15))
        ttk.Entry(image_frame, textvariable=self.image_path).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(image_frame, text="参照...", command=self.select_image).pack(side=tk.RIGHT)

        # 出力ファイル設定（オプション）
        ttk.Label(main_frame, text="3. 保存先 (指定しない場合は自動で名前を付けます)").pack(anchor=tk.W)
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=(5, 20))
        ttk.Entry(output_frame, textvariable=self.output_path).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(output_frame, text="参照...", command=self.select_output).pack(side=tk.RIGHT)

        # 実行ボタン
        self.run_button = ttk.Button(main_frame, text="動画を作成する", command=self.start_processing)
        self.run_button.pack(fill=tk.X, pady=10, ipady=5)

        # ステータス表示
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=(5, 5))
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

    def select_audio(self):
        file_path = filedialog.askopenfilename(
            title="音声ファイルを選択",
            filetypes=[("Audio Files", "*.mp3 *.wav *.aac *.m4a *.flac *.wma"), ("All Files", "*.*")]
        )
        if file_path:
            self.audio_path.set(file_path)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="画像ファイルを選択",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"), ("All Files", "*.*")]
        )
        if file_path:
            self.image_path.set(file_path)

    def select_output(self):
        file_path = filedialog.asksaveasfilename(
            title="保存先を指定",
            defaultextension=".mp4",
            filetypes=[("MP4 Video", "*.mp4")]
        )
        if file_path:
            self.output_path.set(file_path)

    def start_processing(self):
        if self.is_processing:
            return

        audio = self.audio_path.get()
        image = self.image_path.get()
        output = self.output_path.get()

        if not audio or not os.path.exists(audio):
            messagebox.showerror("エラー", "有効な音声ファイルが選択されていません。")
            return
        if not image or not os.path.exists(image):
            messagebox.showerror("エラー", "有効な画像ファイルが選択されていません。")
            return

        if not output:
            # 音声ファイルのファイル名を使って出力パスを自動生成
            base_name = os.path.splitext(os.path.basename(audio))[0]
            output = os.path.join(os.path.dirname(audio), f"{base_name}_video.mp4")
            self.output_path.set(output)

        self.is_processing = True
        self.run_button.configure(state=tk.DISABLED)
        self.status_var.set("処理中... (ffmpegを実行しています)")
        
        # 別スレッドで実行
        thread = threading.Thread(target=self.run_ffmpeg, args=(image, audio, output))
        thread.start()

    def run_ffmpeg(self, image, audio, output):
        # 実行ファイル（またはスクリプト）のあるディレクトリを取得
        if getattr(sys, 'frozen', False):
            # PyInstallerでexe化された場合
            application_path = os.path.dirname(sys.executable)
        else:
            # 通常のスクリプト実行の場合
            application_path = os.path.dirname(os.path.abspath(__file__))

        ffmpeg_cmd = 'ffmpeg'
        # 同じディレクトリに ffmpeg.exe があればそれを使う
        local_ffmpeg = os.path.join(application_path, 'ffmpeg.exe')
        if os.path.exists(local_ffmpeg):
            ffmpeg_cmd = local_ffmpeg

        # ffmpeg -loop 1 -i <image> -i <audio> -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest <output>
        cmd = [
            ffmpeg_cmd, '-y',
            '-loop', '1',
            '-i', image,
            '-i', audio,
            '-c:v', 'libx264',
            '-tune', 'stillimage',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-pix_fmt', 'yuv420p',
            '-shortest',
            output
        ]

        try:
            # Windowsでコンソールウィンドウを表示させないための設定
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                startupinfo=startupinfo,
                encoding='utf-8' # エンコーディングを指定
            )
            
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                self.root.after(0, self.on_success, output)
            else:
                self.root.after(0, self.on_error, stderr)

        except Exception as e:
            self.root.after(0, self.on_error, str(e))

    def on_success(self, output_path):
        self.is_processing = False
        self.run_button.configure(state=tk.NORMAL)
        self.status_var.set(f"完了: {output_path}")
        messagebox.showinfo("成功", f"動画の作成が完了しました！\n\n{output_path}")

    def on_error(self, error_msg):
        self.is_processing = False
        self.run_button.configure(state=tk.NORMAL)
        self.status_var.set("エラーが発生しました")
        # エラーメッセージが長すぎる場合は切り詰める
        if len(error_msg) > 500:
            error_msg = error_msg[-500:]
        messagebox.showerror("エラー", f"動画作成中にエラーが発生しました。\n\n{error_msg}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoMakerApp(root)
    root.mainloop()
