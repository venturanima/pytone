from notes import Notes
notes = Notes.scale('G3')
notes = notes + (~notes)[1:]
notes.play()