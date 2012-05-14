from notes import Notes

'''
    Introduction
'''
intro1 = Notes('D4',['A4','D5'])
intro2 = Notes('F#4',['C#5','A4'])
intro = ((intro1*4+intro2*4) % 0.25 )*2
'''
    Verses
'''
verseBase = Notes('A4')*5 + Notes('G4','F#4','G4')
verseMod = verseBase.replace('B4',3)\
                    .replace('E4',7)\
                    + [('F#4',1.0), ('-', 2.0)]
verseStart = verseBase.without(0) + verseBase.replace('B4',3) + verseBase + verseMod

verse2 = Notes('G4','G4','G4','F#4','E4','D4','E4',('F#4',1.0), ('-', 1.0))
verse3 = Notes('F#4','F#4','D4',('E4',1.0),('-',1.75))
verse = verseStart + verse2 + verse3
verses = (verse*2)%0.5

'''
    Verse Background
'''
afterIntro1 = Notes('B3') + Notes.thirdFifth('B3','minor')
afterIntro2 = Notes([('A4',0.5),('A3',0.5)],'-')
afterIntro3 = Notes('G3') + Notes.thirdFifth('G3','major')
afterIntro4 = Notes('A3') + Notes.thirdFifth('A3','major')
afterIntro = afterIntro1*3 + afterIntro2 + afterIntro3*2 + afterIntro4*2\
                           + afterIntro1*4 + afterIntro3*2 + afterIntro4*2

verseBackground = intro + afterIntro + intro + afterIntro
verseBackground = verseBackground % 0.25

'''
    Chorus
'''
chorusMain1 = Notes(('D5',1.0),'-','-','D5','F#5','E5','D5','C#5',('D5',1.0),'-',('B4',1.0),('-',1.25))
chorusMain2 = Notes(('A4',1.0),'-','-','A4','A4','G4','F#4','E4',('F#4',1.0),('-',1.75))
chorusMainStart = (chorusMain1 + chorusMain2)*2
chorusMainEnd = chorusMain2[2:] <= chorusMainStart.elapsedTime-1
chorusMain = chorusMainStart/chorusMainEnd

'''
    Chorus Background
'''
chorusBackground = (intro1*3 + afterIntro2 + afterIntro1*3 + 'C#4' + ['E4','A4'])*4
chorusBackground = chorusBackground % 0.25

'''
    Combine them to make a song!
'''
song = intro + verses/verseBackground + chorusMain/chorusBackground
song.play()