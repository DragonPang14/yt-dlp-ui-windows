import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import sys
from threading import Thread
import re

class YtDlpDownloader:
    def __init__(self, root):
        # 窗口基本设置
        self.root = root
        self.root.title("YouTube 视频下载工具")
        self.root.geometry("650x550")
        self.root.resizable(True, True)
        self.root.iconbitmap(default="")  # 可替换为自定义图标路径

        # 确保中文字体正常显示
        self.style = ttk.Style()
        self.style.configure(".", font=("SimHei", 10))

        # 下载进程控制
        self.download_process = None
        self.is_downloading = False

        # 创建UI组件
        self.create_widgets()

    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. 视频URL输入
        ttk.Label(main_frame, text="视频URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=60)
        url_entry.grid(row=0, column=1, columnspan=2, sticky=tk.W+tk.E, pady=5)
        
        # 验证URL按钮
        self.verify_btn = ttk.Button(
            main_frame, text="验证URL", command=self.verify_url, width=12
        )
        self.verify_btn.grid(row=0, column=3, sticky=tk.W, pady=5, padx=5)

        # 2. 代理设置
        ttk.Label(main_frame, text="代理地址:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.proxy_var = tk.StringVar(value="socks5://127.0.0.1:7890")
        proxy_entry = ttk.Entry(main_frame, textvariable=self.proxy_var, width=40)
        proxy_entry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)
        
        self.use_proxy_var = tk.BooleanVar(value=True)
        proxy_check = ttk.Checkbutton(
            main_frame, text="使用代理", variable=self.use_proxy_var
        )
        proxy_check.grid(row=1, column=2, sticky=tk.W, pady=5)

        # 3. 下载目录设置
        ttk.Label(main_frame, text="下载目录:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.path_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads", "YouTube"))
        path_entry = ttk.Entry(main_frame, textvariable=self.path_var, width=40)
        path_entry.grid(row=2, column=1, sticky=tk.W+tk.E, pady=5)
        
        browse_btn = ttk.Button(main_frame, text="浏览", command=self.browse_directory)
        browse_btn.grid(row=2, column=2, sticky=tk.W, pady=5, padx=5)

        # 4. 转换选项
        ttk.Label(main_frame, text="格式转换:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.convert_mp4_var = tk.BooleanVar(value=True)
        convert_check = ttk.Checkbutton(
            main_frame, text="自动转换为MP4", variable=self.convert_mp4_var
        )
        convert_check.grid(row=3, column=1, sticky=tk.W, pady=5)

        # 5. 视频质量选择
        ttk.Label(main_frame, text="视频质量:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.StringVar(value="best")
        quality_options = [
            "best", "worst", "144p", "240p", "360p", 
            "480p", "720p", "1080p", "1440p", "2160p"
        ]
        quality_combo = ttk.Combobox(
            main_frame, textvariable=self.quality_var, values=quality_options, state="readonly"
        )
        quality_combo.grid(row=4, column=1, sticky=tk.W, pady=5)

        # 6. 播放列表选项（新增）
        self.is_playlist_var = tk.BooleanVar(value=False)
        self.playlist_frame = ttk.LabelFrame(main_frame, text="播放列表选项", padding="10")
        self.playlist_frame.grid(row=5, column=0, columnspan=3, sticky=tk.W+tk.E, pady=5)
        
        self.download_all_var = tk.BooleanVar(value=True)
        self.playlist_radio_all = ttk.Radiobutton(
            self.playlist_frame, text="下载整个合集", variable=self.download_all_var, value=True
        )
        self.playlist_radio_all.pack(anchor=tk.W, pady=2)
        
        self.playlist_radio_single = ttk.Radiobutton(
            self.playlist_frame, text="仅下载当前视频", variable=self.download_all_var, value=False
        )
        self.playlist_radio_single.pack(anchor=tk.W, pady=2)
        
        # 默认隐藏播放列表选项
        self.playlist_frame.grid_remove()

        # 7. 下载选项
        ttk.Label(main_frame, text="下载选项:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.download_video_var = tk.BooleanVar(value=True)
        video_check = ttk.Checkbutton(
            main_frame, text="下载视频", variable=self.download_video_var
        )
        video_check.grid(row=6, column=1, sticky=tk.W, pady=5)

        # 8. 操作按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=7, column=0, columnspan=3, pady=15)
        
        self.download_btn = ttk.Button(
            btn_frame, text="开始下载", command=self.start_download, width=15
        )
        self.download_btn.pack(side=tk.LEFT, padx=10)
        
        self.cancel_btn = ttk.Button(
            btn_frame, text="取消下载", command=self.cancel_download, width=15, state=tk.DISABLED
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=10)
        
        self.clear_btn = ttk.Button(
            btn_frame, text="清空输入", command=self.clear_inputs, width=15
        )
        self.clear_btn.pack(side=tk.LEFT, padx=10)

        # 9. 进度显示
        ttk.Label(main_frame, text="下载进度:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame, variable=self.progress_var, maximum=100
        )
        self.progress_bar.grid(row=8, column=1, columnspan=2, sticky=tk.W+tk.E, pady=5)

        # 10. 日志显示
        ttk.Label(main_frame, text="输出日志:").grid(row=9, column=0, sticky=tk.NW, pady=5)
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=9, column=1, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S, pady=5)
        
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        self.log_text.config(state=tk.DISABLED)

        # 设置列权重（让输入框随窗口拉伸）
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(9, weight=1)

    def browse_directory(self):
        """打开文件浏览器选择下载目录"""
        directory = filedialog.askdirectory(title="选择下载目录")
        if directory:
            self.path_var.set(directory)

    def log(self, message):
        """在日志区域显示信息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # 滚动到最新内容
        self.log_text.config(state=tk.DISABLED)

    def clear_inputs(self):
        """清空输入框"""
        self.url_var.set("")
        self.is_playlist_var.set(False)
        self.playlist_frame.grid_remove()
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.progress_var.set(0)

    def verify_url(self):
        """验证URL是否为播放列表"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("错误", "请输入视频URL")
            return
        
        self.log("正在验证URL...")
        
        # 检查URL是否包含播放列表参数
        if "playlist" in url or "list=" in url:
            self.is_playlist_var.set(True)
            self.playlist_frame.grid()
            self.log("检测到播放列表URL")
            return
        
        # 检查是否为单个视频但属于合集
        cmd = ["yt-dlp", "--no-colors", "--flat-playlist", "--print", "playlist", url]
        if self.use_proxy_var.get() and self.proxy_var.get():
            cmd.extend(["--proxy", self.proxy_var.get()])
        
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            
            if "playlist" in result.stdout.lower():
                self.is_playlist_var.set(True)
                self.playlist_frame.grid()
                self.log("检测到该视频属于合集")
            else:
                self.is_playlist_var.set(False)
                self.playlist_frame.grid_remove()
                self.log("这是一个单视频URL")
                
        except subprocess.CalledProcessError as e:
            self.log(f"URL验证失败: {e.stderr.strip()}")
            messagebox.showerror("错误", f"URL验证失败: {e.stderr.strip()}")
            self.is_playlist_var.set(False)
            self.playlist_frame.grid_remove()

    def build_command(self):
        """构建yt-dlp命令"""
        # 基础命令
        cmd = ["yt-dlp"]
        
        # 代理设置
        if self.use_proxy_var.get() and self.proxy_var.get():
            cmd.extend(["--proxy", self.proxy_var.get()])
        
        # 下载目录
        download_path = self.path_var.get()
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        cmd.extend(["-P", download_path])
        
        # 格式转换
        if self.convert_mp4_var.get():
            cmd.extend(["--merge-output-format", "mp4"])
        
        # 视频质量
        quality = self.quality_var.get()
        if quality == "best":
            cmd.extend(["-f", "bestvideo+bestaudio/best"])
        elif quality == "worst":
            cmd.extend(["-f", "worstvideo+worstaudio/worst"])
        else:
            cmd.extend(["-f", f"bestvideo[height<={quality[:-1]}]+bestaudio/best[height<={quality[:-1]}]"])
        
        # 仅下载音频
        if not self.download_video_var.get():
            cmd.extend(["-x", "--audio-format", "mp3"])
        
        # 播放列表选项（新增）
        if self.is_playlist_var.get():
            if self.download_all_var.get():
                # 下载整个合集
                cmd.extend(["--yes-playlist"])
                # 格式化文件名，包含序号
                cmd.extend(["-o", "%(playlist_index)s - %(title)s.%(ext)s"])
            else:
                # 仅下载当前视频
                cmd.extend(["--no-playlist"])
        
        # 视频URL
        cmd.append(self.url_var.get())
        
        return cmd

    def start_download(self):
        """开始下载（在新线程中执行）"""
        # 输入验证
        if not self.url_var.get().strip():
            messagebox.showerror("错误", "请输入视频URL")
            return

        # 如果是播放列表但未验证，提示用户
        if ("playlist" in self.url_var.get() or "list=" in self.url_var.get()) and not self.is_playlist_var.get():
            if messagebox.askyesno("确认", "检测到可能是播放列表URL，是否验证？"):
                self.verify_url()
                return

        # 更新UI状态
        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.log("开始准备下载...")
        self.progress_var.set(0)

        # 在新线程中执行下载（避免UI卡死）
        Thread(target=self.run_download, daemon=True).start()

    def run_download(self):
        """执行下载命令"""
        try:
            cmd = self.build_command()
            self.log(f"执行命令: {' '.join(cmd)}")

            # 启动子进程
            self.download_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            # 实时读取输出并更新日志
            for line in self.download_process.stdout:
                if not self.is_downloading:  # 检查是否已取消
                    break
                self.log(line.strip())
                # 简单解析进度（yt-dlp输出中包含百分比）
                if "%" in line:
                    try:
                        progress = float(line.split("%")[0].split()[-1])
                        self.progress_var.set(progress)
                    except:
                        pass

            # 等待进程结束
            self.download_process.wait()

            if self.is_downloading:  # 如果不是被取消的
                if self.download_process.returncode == 0:
                    self.log("下载完成!")
                    self.progress_var.set(100)
                    messagebox.showinfo("成功", "视频下载完成!")
                else:
                    self.log(f"下载失败，返回代码: {self.download_process.returncode}")
                    messagebox.showerror("失败", "下载过程中出现错误")

        except Exception as e:
            self.log(f"错误: {str(e)}")
            messagebox.showerror("错误", f"发生异常: {str(e)}")

        finally:
            # 恢复UI状态
            self.is_downloading = False
            self.download_btn.config(state=tk.NORMAL)
            self.cancel_btn.config(state=tk.DISABLED)
            self.download_process = None

    def cancel_download(self):
        """取消下载"""
        if messagebox.askyesno("确认", "确定要取消下载吗?"):
            self.is_downloading = False
            if self.download_process:
                self.log("正在取消下载...")
                # 终止进程（Windows使用terminate，Linux/Mac使用kill）
                if sys.platform.startswith("win32"):
                    self.download_process.terminate()
                else:
                    self.download_process.kill()

if __name__ == "__main__":
    # 检查yt-dlp是否安装
    try:
        subprocess.run(
            ["yt-dlp", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except FileNotFoundError:
        messagebox.showerror(
            "错误", 
            "未找到yt-dlp，请先安装：\n"
            "1. 打开命令提示符\n"
            "2. 运行：pip install yt-dlp"
        )
        sys.exit(1)

    # 启动应用
    root = tk.Tk()
    app = YtDlpDownloader(root)
    root.mainloop()