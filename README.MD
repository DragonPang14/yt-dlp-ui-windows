以下是根据您的文件名调整后的README文件：


# YouTube 视频下载工具 (基于 yt-dlp)

一个简单易用的 Windows 桌面 UI 工具，用于通过 yt-dlp 下载 YouTube 视频，支持自定义下载参数、代理设置及播放列表处理。

## 功能特点

- 📥 支持下载单个 YouTube 视频或完整播放列表/合集
- 🔍 自动识别播放列表链接，可选择下载整个合集或单个视频
- 🌐 内置代理设置（默认支持 socks5 代理）
- 🔐 **新增 Cookie 支持**：通过导入浏览器 Cookie 绕过年龄限制和机器人验证
- 🎨 可自定义视频质量（从 144p 到 2160p 及自动最佳/最差）
- 🎞️ 自动转换下载内容为 MP4 格式
- 📂 支持自定义下载目录
- 🎵 可选仅下载音频（自动转换为 MP3）
- 📊 实时显示下载进度和日志信息


## 前置要求

- Windows 操作系统
- Python 3.9 及以上版本
- yt-dlp（会自动检查并提示安装）
- 推荐安装 ffmpeg（用于格式转换，需添加到系统环境变量）

## 安装与使用

1. 克隆本仓库：
   ```bash
   git clone https://github.com/你的用户名/your-repo-name.git
   cd your-repo-name
   ```

2. 安装依赖（如提示缺少组件）：
   ```bash
   pip install yt-dlp
   ```

3. 运行工具：
   ```bash
   python yt-dlp-ui-win.py
   ```

4. 使用步骤：
   - 输入 YouTube 视频或播放列表 URL
   - （可选）点击「验证 URL」确认是否为播放列表
   - **如需绕过年龄限制或机器人验证**：
     1. 启用「使用 Cookie」选项
     2. 粘贴从浏览器导出的 Cookie 字符串
   - 配置其他下载参数（代理、目录、质量等）
   - 点击「开始下载」即可

## Cookie 使用说明

### 如何获取 YouTube Cookie

1. 打开 Chrome 或 Firefox 浏览器并登录 YouTube
2. 安装 "EditThisCookie" 扩展程序：
   - [Chrome 应用商店](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)
   - [Firefox 附加组件](https://addons.mozilla.org/en-US/firefox/addon/editthiscookie/)
3. 访问 YouTube 网站
4. 点击扩展图标，选择「Export」导出完整 Cookie
5. 复制导出的 SSID 字符串
6. 粘贴到工具的 Cookie 输入框中

### 注意事项

- Cookie 有有效期，过期后需要重新获取
- 不要分享你的 Cookie 给他人，避免账号安全风险
- 某些受版权保护的视频可能仍然无法下载
- 使用 Cookie 下载的内容请遵守相关法律法规

## 注意事项

- 部分视频可能因版权限制无法下载
- 大文件下载速度取决于网络状况和视频质量
- 播放列表下载时，文件名将自动添加序号（如「1 - 视频标题.mp4」）
- 代理设置默认为 `socks5://127.0.0.1:7890`，可根据实际代理修改

## 项目结构

```
youtube-downloader/
├── yt-dlp-ui-win.py       # 主程序文件
├── .gitignore             # Git忽略配置
└── README.md              # 说明文档
```

## 许可证

本项目基于 [MIT 许可证](LICENSE) 开源

## 声明

- 本工具仅用于学习和研究目的，下载视频请遵守 YouTube 服务条款及相关法律法规
- 视频版权归原作者所有，请勿用于商业用途

## 关于

本项目由 **豆包** 编写，基于 yt-dlp 开发，旨在提供更便捷的 YouTube 视频下载体验。

如有问题或建议，欢迎提交 Issue 或 Pull Request。