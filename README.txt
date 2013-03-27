_____________________________________________
PyTone

Screencast: http://www.youtube.com/watch?v=KE38gcoGWd8
Requires scipy and pygames modules. Uses modified python-musical module as well, but source code for that is included.

+ will concatenate notes.
If the second argument to + is a string, it will concatenate that string as a note.
/ will play notes overlaid with one another.
>> will shift the notes up by the amount given. If given a tuple, will call shift using those arguments.
<< will shift notes down by amount given.
< will put the start time of the left side at the time given by the right side.
- is the note for a rest.
* will repeat n times.
** will scale the length of notes.
% will set the volume of all notes.
~ will reverse the sequence of notes.
Notes can be created as either:
    Notes('A3') which creates a note of A3 with default note length
    Notes(('A3',1.0)) which creates a note of A3 with 1.0 note length
    Notes(('A3',1.0,0.25)) which creates a note of A3 with 1.0 note length & 0.25 volume
Chords can be created by Notes(['A3',('A4',1.0)]), as a list of notes.

When Notes are printed, they will print in the format (Note, Time, NoteLength).