from notes import Notes
'''
    Fugues start with a theme that sounds successively in each voice, creating the exposition.
'''
scale = Notes.scale('G3','minor')
theme = (scale[:3] + Notes.triad('G3','minor')) * 2 + scale
exposition = theme%0.75 + (theme>>(3,'minor')) % 0.5 + (theme>>(5,'minor')) % 0.25
'''
    This is followed by the episode, developed from previously heard material.
'''
episode = (~scale)[:4] + scale[3:7].chord(scale[7]) % 0.5
episode = episode * 2 + theme % 0.25
'''
    We then bring this simple fugue to a conclusion with the coda.
'''
arpeggio = Notes.arpeggio((~scale)[7],'minor')
arpeggio = arpeggio + (arpeggio>>(7,'minor'))
arpeggio = arpeggio + arpeggio.allChorded().chord('G5')
coda = Notes('G4') + (~scale)[:7] + arpeggio
'''
    Play all the notes!
'''
(exposition + episode + coda).play()

