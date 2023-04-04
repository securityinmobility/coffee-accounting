#!/bin/bash

num="$1"

wget -O num.png "https://github.com/AprilRobotics/apriltag-imgs/raw/master/tag36h11/tag36_11_001$num.png"
convert num.png -scale 1600% big_num.png

cp apriltagged-list.svg apriltagged-list.tmp.svg
sed -i "s/#999#/$1/" apriltagged-list.tmp.svg

inkscape apriltagged-list.tmp.svg "--export-pdf=apriltagged-list-$num.pdf"
