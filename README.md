# set-solver
A program to find sets in the card game "SET"

Read more about the game on [Wikipedia](https://en.wikipedia.org/wiki/Set_(card_game))


# Installation
`# pip install -r requirements.txt`

___

Or install the packages seperately:

`# pip install numpy==1.16.3`

`# pip install opencv-contrib-python==3.4.5.20`


# Usage
`$ python cards.py [imagefile(s)]`

The program can be run, with as many imagefiles as desired.
If the image is not found, it is simply skipped.

I have only tested it with `.jpg` files, but any of the filetypes listed in the [OpenCV Docs](https://docs.opencv.org/3.4.6/d4/da8/group__imgcodecs.html#ga288b8b3da0892bd651fce07b3bbd3a56) should work.


# Example
If you want to run the program with this image:

![Set1](/img/1.jpg "Example image")

Run this
`$ python cards.py img\1.jpg`

Whereafter a folder named `1_solution` will be created inside the `img` folder.

Inside this folder, you will find images, with all the sets found on the image. Like the one below

![Set1_sol1](/img/1_solution/set1.jpg "Example output")


## Disclaimer
The code is still not working 100% correcly on all of the images, I know, it's still in the early development stages.


# License
The repo is licensed under [GPL-3.0](/LICENSE)


# Contact
You are welcome to contact me, if you have any questions, at [tinggaard@yahoo.com](mailto:tinggaard@yahoo.com)
Or if you have suggestions, feel free to fork me here on GitHub


# <3
Made with blood, sweat and tears, by Jens Tinggaard