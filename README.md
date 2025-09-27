# Remove Flutter/Dart Comments

A simple Python script to remove all comments from Flutter/Dart source code files. This tool is useful for cleaning up code before publishing, sharing, or analyzing.

## Features
- Removes single-line (`// ...`) and multi-line (`/* ... */`) comments from Dart files
- Processes individual files or entire directories
- Outputs cleaned files or overwrites originals (configurable)

## Usage

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/remove_flutter_dart_comments.git
   cd remove_flutter_dart_comments
   ```

2. **Run the script:**
   ```sh
   python remove_flutter_dart_comments.py <path-to-dart-file-or-directory>
   ```
   - Replace `<path-to-dart-file-or-directory>` with the path to your Dart file or folder.

3. **Options:**
   - By default, the script overwrites the original files. You can modify the script to output to a different location if needed.

## Example
```sh
python remove_flutter_dart_comments.py ./lib/
```

## Requirements
- Python 3.6 or higher

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE)

---

*Created with ❤️ for the Flutter/Dart community.*
