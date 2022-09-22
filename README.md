# Musical-note-identifier-Chromatic-tuner
Go to [Theory.md](https://github.com/rodrickcalvin/Musical-note-identifier-Chromatic-tuner/blob/master/Theory.md) to get the indepth explanation of the theory behind the system.

## After:
- Clone the project to your local computer.
- Make sure have a stable python 
- Install the following packages
  > ### For GUI:
  > Choose your favorite GUI library to build. The options are:
  > - Kivy
  > - KivyMD
  > - PyQT
  > - tKinter

   !!! Disclaimer: Choose wisely considering ease of use and quality output...
  > ### For the logic and backend:
  > Take note to always use a python version compatible with the libraries. At inintial development we used python version 3.6 because pyAudio wouldn't install on later versions of python 3.7+. I am currently running python 3.8.10 from WSL2 and it works fine.
  > - Create a virtual environment using virtualenv or virtualenvwrapper
  > - If using windows make sure your visual c++ and build tools are installed. Hence you may need to have visual studio installed on your computer.
  > - If you are using WSL/WSL2 OR linux, you may need to install the following packages:
  >   - libasound2-dev
  >   - portaudio19-dev
  >   - libportaudio2
  >   - libportaudiocpp0
  >   - ffmpeg
  >   - libav-tools
  >   - libavcodec-extra
  > Run the following command to install the required packages: 
  > ```bash
  > $ sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
  > $ sudo apt-get install ffmpeg
  > ```
  > - activate your environment:
  > ```"myenv\Scripts\activate"``` for virtualenv and ```"workon myenv"``` for virtualenvwrapper.
  > - install the requirements needed for the project:
  > ```"pip install -r requirements.txt"```
  > - Run the ```multithreading.py``` file.

  :):):):):):):):):):):):):):):):):):):):)Enjoy yourself:):):):):):):):):):):):):):):)

  ## Contributions:
  You are welcome to contribute to this project. Just star the project and cite it in your work
  
  We developed it during a process to find a solution to an assignment in the course: ```Audio and Speech Signal Processing``` under the Computer Engineering undergraduate programme at university.

  We were asked to develop a simple audio processing application using what we had learnt. And so we came up with the [idea](https://github.com/rodrickcalvin/Musical-note-identifier-Chromatic-tuner/blob/master/Concept%20Note.pdf) as a small project.

  > A big shoutout [Matt Zucker](https://github.com/mzucker) from Philadelphia for the repository that guided us through the creation of this application.....




