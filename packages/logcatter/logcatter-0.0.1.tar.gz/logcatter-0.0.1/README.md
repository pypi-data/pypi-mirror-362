# Logcatter 🐱

**Brings the familiar convenience and readability of Android's Logcat to your Python projects.**

Tired of complex logger configurations? `Logcatter` lets you use intuitive methods like `Log.d()` and `Log.i()` right away. It automatically tags logs with the calling filename, dramatically speeding up your debugging workflow.

## ✨ Key Features

*   **☕ Android Logcat Style:** Get beautiful, easy-to-read logs formatted as `yyyy-MM-dd HH:mm:ss.SSS [D/tag] message`.
*   **🏷️ Automatic Tagging:** The name of the source file (`main.py`) that calls the log is automatically used as the tag, so you can instantly identify the origin of a log.
*   **🎨 Colored Output:** Log levels (Debug, Info, Warning, Error) are color-coded for enhanced visual recognition.
*   **🚀 Concise API:** Use intuitive methods nearly identical to the Android `Log` class: `Log.d()`, `Log.i()`, `Log.w()`, and `Log.e()`.
*   **🔧 Zero Configuration:** Works right out of the box after installation with no extra setup required.

## 📦 Installation

```shell
pip install logcatter
```

## 🚀 Quick Start

Just import the `Log` class into your project and start logging.

```python
from logcatter import Log

Log.d("This is log!!")
Log.setLevel(Log.WARNING)  # Hide DEBUG, INFO level logs
Log.i("This is info!!")  # You cannot see this because you set the minimum level `WARNING`
Log.e("ERROR!!!", e=ValueError())  # You can log the caught exception/error with argument `e`
Log.f("FATAL ERROR", s=True)  # You can log the stacktrace with flag `s`
```

### 💻 Output Example

Running the code above will produce this beautifully formatted output in your terminal:
