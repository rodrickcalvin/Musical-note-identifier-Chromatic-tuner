# Theory behind the Apllication
In music, we talk about many things for example ```the key```, ```the chords```, ```the notes``` and ```the octaves```.

To relate music with physics and mathematics language, we take a deeper look into the above terms.
### A musical key
> It is a scale around which music revolves. Hence the fundamental notes making the song's melody, chords and bassline are derived from that group of notes.

### A musical chord
> It is a combination of two or more harmonics notes played at the same time.

### A musical note
> It is a melody interpreted by a brain for a specific frequency.

### An octave
> This is an interval between one musical pitch to another which is double it frequency.

When sound is input into the computer through a microphone, it is transformed from ```spatial domain``` to ```frequency domain``` to easily discern which is noise and the required note from the input.

To break it down in details:
1. We use ```STFT (Short Time Fourier Transform)``` that takes in an input and splits it into segments and each segment is converted to frequency domain.

> The following functions in ```logic.py``` :
> * ```freq_to_number(f)```
> * ```number_to_freq(n)```
> * ```note_name(n)```

> are from a useful website:
https://newt.phys.unsw.edu.au/jw/notes.html

> * number of octaves, ```n_0 = log_2(f2/f1)```

In electronic music, most calculations of pitch are carried out in **MIDI** numbers, ```m```.  "```m```" increases by one for each equal tempered *semitone*. Using a simple formula for conversion between frequencies and **MIDI** numbers, we can easily convert to whichever we may need.
> From ```frequencies.py```, we use a reference frequency A4, always set at ```440Hz``` and its known **MIDI** number which is ```69```.
> * **MIDI** number, ```m```= 12 x log_2(f_*m*/440)+ 69
> * ```f_m``` = (2^(m-69)/12) x 440
