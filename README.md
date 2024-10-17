<div align="center">
   <h1>🦅 Eagle Downloader </h1>
</div>

![Coverage](https://img.shields.io/codecov/c/github/gfrancodev/eagle-downloader?logo=codecov) ![License](https://img.shields.io/github/license/gfrancodev/eagle-downloader?color=blue&logo=github) ![GitHub Release](https://img.shields.io/github/v/release/gfrancodev/eagle-downloader?label=latest%20release&logo=github) ![GitHub issues](https://img.shields.io/github/issues/gfrancodev/eagle-downloader) ![GitHub pull requests](https://img.shields.io/github/issues-pr/gfrancodev/eagle-downloader) ![GitHub last commit](https://img.shields.io/github/last-commit/gfrancodev/eagle-downloader) ![Top Language](https://img.shields.io/github/languages/top/gfrancodev/eagle-downloader) ![Repo Size](https://img.shields.io/github/repo-size/gfrancodev/eagle-downloader)

## 📦 Overview

**Eagle Downloader** is a robust and user-friendly **YouTube Downloader** Command-Line Interface (CLI) tool designed to effortlessly download high-quality videos and audios from YouTube. Whether you're looking to save your favorite YouTube videos, convert them to different formats, or manage your media library, Eagle Downloader provides a seamless and efficient experience with powerful features tailored for both casual users and power users.

## 🚀 Features

- **YouTube Focused**: Specially optimized for downloading videos and audios from YouTube with high reliability.
- **High-Quality Downloads**: Supports downloading videos in various resolutions, including 1080p, 720p, and higher.
- **Audio Extraction**: Easily extract audio from YouTube videos and save them in formats like MP3.
- **Interactive Prompts**: User-friendly prompts guide you through the download process, making it accessible for all users.
- **Progress Indicators**: Real-time progress bars to monitor download status and estimated completion time.
- **Customizable Output**: Specify download locations, file names, and formats to suit your preferences.
- **Comprehensive Logging**: Detailed logs for troubleshooting and tracking download activities.
- **Automated Testing & CI/CD**: Ensures high-quality builds and reliable releases across different operating systems.
- **Cross-Platform Support**: Available for Windows, Linux, and macOS, ensuring accessibility for all users.

---

## 🛠 Installation Guide

Welcome to the **Eagle Downloader** installation guide! Follow the steps below to install the binary on your preferred operating system.

### 📦 Downloading the Binary

Before proceeding with the installation, download the appropriate binary for your operating system from the [**Releases**](https://github.com/gfrancodev/eagle-downloader/releases) page.


You can install Eagle Downloader either via pip (for Python users) or by downloading the binary for your platform directly from the releases page.

---
### 📦 Installing via pip

If you're familiar with Python, you can install Eagle Downloader using pip:
```bash
pip install eagle-downloader
```
---

### 💻 Linux

#### 🔹 **Installation Steps**

1. **Download the Binary**

   Visit the [**Releases**](https://github.com/gfrancodev/eagle-downloader/releases) page and download the latest Linux binary (`eagle-linux`).

   Alternatively, you can use `wget` to download directly:
   ```bash
   wget https://github.com/gfrancodev/eagle-downloader/releases/download/1.0.2.1/eagle-linux-v1.0.2.1-x64.zip
   ```

2. **Make the Binary Executable**
   ```bash
   chmod +x eagle-linux
   ```

3. **Move the Binary to a Directory in Your PATH**
   ```bash
   sudo mv eagle-linux /usr/local/bin/eagle
   ```

4. **Run the Eagle Downloader**
   ```bash
   eagle
   ```

---

### 🪟 Windows

#### 🔹 **Installation Steps**

1. **Download the Binary**

   Visit the [**Releases**](https://github.com/gfrancodev/eagle-downloader/releases) page and download the latest Windows binary (`eagle-windows.exe`).

   Alternatively, use PowerShell to download directly:
   ```powershell
   Invoke-WebRequest -Uri https://github.com/gfrancodev/eagle-downloader/releases/download/v1.0.2.1/eagle-windows-v1.0.2.1-x64.zip -OutFile eagle.exe
   ```

2. **Move the Binary to a Directory in Your PATH**

   - **Create a Directory for Executables** (if it doesn't exist):
     ```powershell
     mkdir "C:\Program Files\EagleDownloader"
     ```
   - **Move the `eagle.exe` to the Directory**:
     ```powershell
     Move-Item -Path .\eagle.exe -Destination "C:\Program Files\EagleDownloader\eagle.exe"
     ```
   - **Add the Directory to Your System PATH**:
     - **Via GUI**:
       1. Right-click on **This PC** and select **Properties**.
       2. Click on **Advanced system settings**.
       3. Click on **Environment Variables**.
       4. Under **System variables**, find and select **Path**, then click **Edit**.
       5. Click **New** and add `C:\Program Files\EagleDownloader`.
       6. Click **OK** on all dialogs to apply changes.
     - **Via PowerShell**:
       ```powershell
       [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\EagleDownloader", [EnvironmentVariableTarget]::Machine)
       ```

3. **Run the Eagle Downloader**
   ```powershell
   eagle
   ```

---

### 🍎 macOS

#### 🔹 **Installation Steps**

1. **Download the Binary**

   Visit the [**Releases**](https://github.com/gfrancodev/eagle-downloader/releases) page and download the latest macOS binary (`eagle-macos`).

   Alternatively, you can use `curl` to download directly:
   ```bash
   curl -L -o eagle-darwin https://github.com/gfrancodev/eagle-downloader/releases/download/v1.0.2.1/eagle-darwin-v1.0.2.1-x64.zip
   ```

2. **Make the Binary Executable**
   ```bash
   chmod +x eagle-darwin
   ```

3. **Move the Binary to a Directory in Your PATH**
   ```bash
   sudo mv eagle-darwin /usr/local/bin/eagle
   ```

4. **Run the Eagle Downloader**
   ```bash
   eagle
   ```
---

For more details and the latest updates, visit the [**Eagle Downloader GitHub repository**](https://github.com/gfrancodev/eagle-downloader).

### 🔍 **Example Commands**

- **Download a YouTube Video**:
  ```bash
  eagle
  ```
  Follow the prompts to enter the video URL, select the format, and choose the download location.
---

### ❓ **Troubleshooting**

- **Permission Denied Errors**: Ensure you have the necessary permissions to move binaries to system directories. Use `sudo` where appropriate.
- **Command Not Found**: Make sure the installation directory is added to your system PATH and that the terminal session is restarted or reloaded to recognize the new PATH settings.
- **Binary Not Executing Properly**: Verify that the binary was downloaded correctly and that it's compatible with your operating system version.

---

### 📚 **Additional Resources**

- **Eagle Downloader Repository**: [GitHub - gfrancodev/eagle-downloader](https://github.com/gfrancodev/eagle-downloader)
- **GitHub Releases Documentation**: [Creating Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)

---

Feel free to reach out if you encounter any issues during the installation process. Happy downloading! 🦅😊

---

## 📝 Summary of Changes

- **Removed Python Prerequisites**: Since the binaries are standalone, users no longer need Python 3.11+ installed.
- **Simplified Installation Steps**: Focused solely on downloading, making executable, moving to PATH, and verifying the installation.
- **Enhanced Clarity**: Provided clear and concise instructions for each operating system without unnecessary prerequisites.

## 🧑‍🤝‍🧑 Contributing

We welcome contributions from the community to enhance **Eagle Downloader**. Here's how you can get involved:

### 🔧 How to Contribute

1. **Fork the Repository**:
   Click the "Fork" button at the top-right corner of the repository page to create your own fork.

2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/gfrancodev/eagle-downloader.git
   cd eagle-downloader
   ```

3. **Create a New Branch**:
   ```bash
   git checkout -b feature/YourFeatureName
   ```

4. **Make Your Changes**:
   Implement your feature or bug fix. Ensure your code adheres to the project's coding standards.

5. **Run Tests and Ensure Coverage**:
   ```bash
   make test-coverage
   ```
   Make sure all tests pass and coverage remains high.

6. **Commit Your Changes**:
   ```bash
   git commit -m "Add feature: Your Feature Description"
   ```

7. **Push to Your Fork**:
   ```bash
   git push origin feature/YourFeatureName
   ```

8. **Create a Pull Request**:
   Navigate to the original repository and click "Compare & pull request". Provide a clear description of your changes.

### 📝 Guidelines

- **Code Quality**: Follow PEP 8 standards. Use `flake8` and `black` for linting and formatting.
- **Testing**: Write tests for new features and ensure existing tests pass.
- **Documentation**: Update the `README.md` and inline comments as necessary.
- **Commit Messages**: Use clear and descriptive commit messages.

### 📚 Resources

- [Contributing Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

## 📝 License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.

## 📣 Acknowledgements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for powerful YouTube media downloading capabilities.
- [PyInstaller](https://www.pyinstaller.org/) for packaging Python applications into standalone executables.
- [GitHub Actions](https://github.com/features/actions) for continuous integration and deployment.

## 📫 Contact

For any inquiries or support, please open an [issue](https://github.com/gfrancodev/eagle-downloader/issues) on GitHub or contact [contact@gfrancodev.com](mailto:contact@gfrancodev.com).

---

![GitHub followers](https://img.shields.io/github/followers/gfrancodev?label=Follow&style=social) ![GitHub stars](https://img.shields.io/github/stars/gfrancodev/eagle-downloader?style=social)
