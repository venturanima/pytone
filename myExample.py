from notes import Notes

'''
    Background
'''
background = Notes(('C4',1.0), ['G4','D4'])*4 + Notes(('C4',1.0), ['G4','E4'])*4
background = background%0.25
'''
    Main sequence
'''
main1 = Notes('-','C4','C4','D4','E4','D4','E4','F4',('G4',1.0),('-',1.75))
main2Core = Notes('F4','F4','G4','F4','E4','D4')
main2 = Notes('-') + main2Core + Notes('E4',('C4',1.0),('-',1.75))
'''
    Main sequence without ending rest
'''
main3 = main1/(main1 <= main1.elapsedTime-2.0)
main3 = main3/(main3 <= main3.elapsedTime-2.0)
main4 = main3/(main2 <= main3.elapsedTime-2.0)
'''
    Ending notes, with no background
'''
main5 = Notes('-','F4')
main5 = main5 + main2Core + Notes(('C4',1.0,0.25),'-',('G3',1.0,0.1),'-',('E3',1.0,0.25),'-',('G3',1.0,0.5),'-',[('E3',1.0,1.0),('G3',1.0,1.0),('C4',1.0,1.0)])
main = main1*2 + main2*2 + main4%0.5 + main2 + main5
'''
    The song!
'''
(background*2 + (main/(background*8)) ).play()
