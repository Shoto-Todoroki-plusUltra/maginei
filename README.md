# maginei

Him, whose head is bedecked with a peacock feather and is adept in playing His flute, is the most beautiful.
<br>Visualize images on command line.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Installation

Installation is simple. Simply build using cargo:
```bash
# Clone the repository
git clone https://github.com/Shoto-Todoroki-plusUltra/maginei.git

#Navigate into the project directory
cd maginei

#build
cargo build
```

## Usage
```
Usage: ./maginei [-f width] [-i file_path] [file_path]
  -f width      Set the width (default: 200)
  -i file_path  Specify the input file path
  -h, --help    Show this help message
If no flags are used, the first argument is treated as the file path.
```

Make sure that a single line in the terminal is long enough to hold characters as the `width`, else there will be an overflow causing the image to be distorted. Try to make sure that the `width` is the number of characters a single line can store in the terminal. Longer the `width`, clearer the image.

## NOTE
Still a new project so bare with me.
