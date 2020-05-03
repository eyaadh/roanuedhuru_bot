# roanuedhuru_bot
A simple Telegram group butler bot build for the chat [CityofAddu](https://t.me/CityofAddu).

Tested on Python3.7, Win and Ubuntu

## Cloning & Run:

1. `git clone https://github.com/eyaadh/roanuedhuru_bot.git`, to clone the repository.
2. `cd roanuedhuru`, to enter the directory.
3. `pip3 install -U https://github.com/pyrogram/pyrogram/archive/asyncio.zip`, to install pyrogram-asyncio.
4. - `apt-get install tesseract-ocr libtesseract-dev libleptonica-dev pkg-config` for installing tesseract on Debian/Ubuntu.
   - For windows use conda -  `conda install -c conda-forge tesserocr`
5. `pip3 install -r requirements.txt`, to install rest of the dependencies/requirements.
> If you get the error `error: command 'x86_64-linux-gnu-gcc' failed with exit status 1` on ubuntu while trying to insall tesserocr python library ensure you have python3.7-dev and cython installed.
6. Create a new `config.ini` using the sample available at `roanu\working_dir`.
7. Run with `python3.8 -m roanu`, stop with <kbd>CTRL</kbd>+<kbd>C</kbd>.
> It is recommended to use [virtual environments](https://docs.python-guide.org/dev/virtualenvs/) while running the app, this is a good practice you can use at any of your python projects as virtualenv creates an isolated Python environment which is specific to your project.

