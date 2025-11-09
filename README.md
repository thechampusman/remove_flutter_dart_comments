![Visitor Count](https://visitor-badge.laobi.icu/badge?page_id=thechampusman.remove_flutter_dart_comments)

# Remove Flutter/Dart Comments

A robust Python tool to remove all comments from Flutter/Dart source code files. This tool is useful for cleaning up code before publishing, sharing, or analyzing.

## ✨ Features
- 🎯 **Smart Comment Removal**: Removes single-line (`// ...`) and multi-line (`/* ... */`) comments from Dart files
- 🛡️ **String Preservation**: Preserves string literals and character escapes
- 📁 **Flutter Project Detection**: Automatically validates Flutter project structure
- �️ **GUI Folder Selection**: Windows Explorer popup for easy folder selection
- 💬 **Interactive Dialogs**: User-friendly confirmation and result dialogs
- 🔧 **Robust Error Handling**: Comprehensive error checking with fallback options
- 📊 **Progress Reporting**: Shows processing statistics and results

## 🚀 Quick Start

### Option 1: Use the Batch File (Windows - Recommended)
1. **Download or clone the repository**
2. **Double-click `run_flutter_comment_remover.bat`**
3. **A Windows Explorer dialog will open - select your Flutter project folder**
4. **Confirm the operation in the dialog boxes**

### Option 2: Command Line
1. **Clone the repository:**
   ```sh
   git clone https://github.com/thechampusman/remove_flutter_dart_comments.git
   cd remove_flutter_dart_comments
   ```

2. **Run the script:**
   ```sh
   python remove_flutter_dart_comments.py
   ```

3. **A Windows Explorer dialog will open to select your Flutter project folder**

## 📋 Requirements
- Python 3.6 or higher
- Tkinter (usually included with Python on Windows)
- Flutter project with `pubspec.yaml` and/or `lib/` directory

## ⚠️ Important Notes
- **Always backup your project before running this tool!**
- The script modifies files in-place (overwrites original files)
- Works best with properly structured Flutter projects

## 🛠️ Additional Tools

### GitHub Repository Creator
This project also includes a handy tool for quickly setting up new GitHub repositories:

- **Windows**: Double-click `create_github_repo.bat`
- **Command Line**: `python create_github_repo.py`

This tool automatically:
- Creates a README.md file
- Initializes git repository
- Sets up remote origin
- Makes initial commit and push

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📄 License
[MIT](LICENSE)

---

*Created with ❤️ for the Flutter/Dart community.*

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE)

---

*Created with ❤️ for the Flutter/Dart community.*
