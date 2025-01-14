# `krikflip`

A Krita plugin which automatically (visually) flips your canvas at the interval of your choice.

If you are a digital artist, flipping your canvas frequently is good practice for spotting anatomical and compositional errors which can otherwise go unnoticed due to sensory adaptation.

# Installation

 Installation follows standard Krita plugin conventions.

# Usage

`krikflip` provides a docker which looks like this:

![krikflip-screenshot](https://github.com/user-attachments/assets/c0156835-8a95-4fd9-af12-068a03a389a5)

Use the slider to select how often you want your canvas flipped (between 1 and 180 minutes). The scale is logarithmic.

Toggle the 'Stopped' button to 'Running' to start the countdown. The 'Flip now' button will immediately flip the canvas horizontally. When the timer is running, this button will display a percentage which decrements to 0% as the timer runs out.

When the timer expires, the canvas is visually flipped and the timer resets.
