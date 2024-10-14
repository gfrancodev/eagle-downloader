# Eagle Downloader ![GitHub Actions](https://img.shields.io/github/workflow/status/gfrancodev/eagle-downloader/CI?label=CI&logo=github) ![Coverage](https://img.shields.io/codecov/c/github/gfrancodev/eagle-downloader?logo=codecov) ![License](https://img.shields.io/github/license/gfrancodev/eagle-downloader?color=blue&logo=github) ![GitHub Release](https://img.shields.io/github/v/release/gfrancodev/eagle-downloader?label=latest%20release&logo=github) ![GitHub issues](https://img.shields.io/github/issues/gfrancodev/eagle-downloader) ![GitHub pull requests](https://img.shields.io/github/issues-pr/gfrancodev/eagle-downloader) ![GitHub last commit](https://img.shields.io/github/last-commit/gfrancodev/eagle-downloader) ![Top Language](https://img.shields.io/github/languages/top/gfrancodev/eagle-downloader) ![Repo Size](https://img.shields.io/github/repo-size/gfrancodev/eagle-downloader)

## 📦 Overview

**Eagle Downloader** is a robust and user-friendly **YouTube Downloader** Command-Line Interface (CLI) tool designed to effortlessly download high-quality videos and audios from YouTube. Whether you're looking to save your favorite YouTube videos, convert them to different formats, or manage your media library, Eagle Downloader provides a seamless and efficient experience with powerful features tailored for both casual users and power users.

## 🚀 Features

- **YouTube Focused**: Specially optimized for downloading videos and audios from YouTube with high reliability.
- **High-Quality Downloads**: Supports downloading videos in various resolutions, including 1080p, 720p, and higher.
- **Audio Extraction**: Easily extract audio from YouTube videos and save them in formats like MP3.
- **Interactive Prompts**: User-friendly prompts guide you through the download process, making it accessible for all users.
- **Progress Indicators**: Real-time progress bars to monitor download status and estimated completion time.
- **Customizable Output**: Specify download locations, file names, and formats to suit your preferences.
- **Batch Downloads**: Download multiple videos at once by providing a list of URLs.
- **Comprehensive Logging**: Detailed logs for troubleshooting and tracking download activities.
- **Automated Testing & CI/CD**: Ensures high-quality builds and reliable releases across different operating systems.
- **Cross-Platform Support**: Available for Windows, Linux, and macOS, ensuring accessibility for all users.

## 🛠 Installation

### 🔹 Download Pre-built Binaries

Eagle Downloader provides pre-built binaries for **Windows**, **Linux**, and **macOS**. You can download the latest release from the [Releases Page](https://github.com/gfrancodev/eagle-downloader/releases).

1. **Windows**: `eagle.exe`
2. **Linux**: `eagle`
3. **macOS**: `eagle`

#### 🖥️ Running on Linux/macOS

1. **Make the file executable**:
   ```bash
   chmod +x eagle
   ```
2. **Move to a directory in your PATH** (optional):
   ```bash
   sudo mv eagle /usr/local/bin/
   ```
3. **Run the application**:
   ```bash
   eagle
   ```

#### 🪟 Running on Windows

1. **Move the executable to a directory in your PATH** or add its location to the PATH environment variable.
2. **Run the application**:
   ```cmd
   eagle.exe
   ```

### 🔹 Building from Source

If you prefer to build **Eagle Downloader** yourself or wish to contribute to the project, follow these steps:

#### 🛠 Prerequisites

- **Python 3.11.10**: Ensure you have Python 3.11.10 installed. You can manage Python versions using [pyenv](https://github.com/pyenv/pyenv).
- **Git**: For cloning the repository.

#### 📥 Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/gfrancodev/eagle-downloader.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd eagle-downloader
   ```
3. **Create and Activate Virtual Environment**:
   ```bash
   make venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install Dependencies**:
   ```bash
   make install
   ```
5. **Build the Executable**:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   make build
   ```
6. **Find the Executable**:
   The built executable will be located in the `dist/` directory, named `eagle` (Linux/macOS) or `eagle.exe` (Windows).

## 📖 Usage

**Eagle Downloader** offers a straightforward interface to download your desired YouTube media. Here's how to get started:

1. **Run the Application**:
   ```bash
   eagle  # On Windows: eagle.exe
   ```
2. **Follow the Interactive Prompts**:
   - **Enter the YouTube URL**: Provide the URL of the YouTube video you wish to download.
   - **Choose Format**: Select the desired format (e.g., MP4 for video, MP3 for audio).
   - **Specify Download Location**: Choose where to save the downloaded file.

3. **Monitor the Download**:
   - Real-time progress bars will display the download status.
   - Upon completion, you'll receive a confirmation message with the file location.

### 🔍 **Example Commands**

- **Download a YouTube Video**:
  ```bash
  eagle
  ```
  Follow the prompts to enter the video URL, select the format, and choose the download location.

- **Batch Download YouTube Videos**:
  Create a text file (e.g., `urls.txt`) with one YouTube URL per line, then run:
  ```bash
  eagle --batch urls.txt
  ```

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
