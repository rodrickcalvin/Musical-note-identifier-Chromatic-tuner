# Note Names, Frequencies & Note Wave Lengths
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
