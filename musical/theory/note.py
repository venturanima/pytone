class Note:

    ''' Note class handles note/octave object, transposition, and frequency
      calculation
    '''

    NOTES = ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']

    ''' Instantiate note, examples:
        Note('C')      # C4 (middle C)
        Note(0)        # C at octave 0
        Note(1)        # C-sharp at octave 0
        Note(12)       # C at octave 0
        Note('C2')     # C at octave 2
        Note('Db')     # D-flat at octave 4
        Note('D#3')    # D-sharp at octave 3
        Note(('G', 5)) # G note at octave 5

    '''
    def __init__(self, note, volume=0.75):
        self.volume = volume
        if isinstance(note, str):
            self.index = Note.index_from_string(note)
        elif isinstance(note, tuple):
            self.index = Note.index_from_string(note[0]) + 12 * note[1]
        elif isinstance(note, Note):
            self.index = note.index
        else:
            self.index = int(note)

    def __repr__(self):
        return "Note('%s%i')" % (self.note, self.getOctave())

    def __cmp__(self, other):
        return cmp(self.index, other.index)

    def __float__(self):
        return self.frequency()


    ''' absolute note (str+octave)
    '''
    @property
    def value(self):
        return str(self.note)+str(self.getOctave())
        
    ''' note name property
    '''
    @property
    def note(self):
        return Note.NOTES[self.index % 12]

    ''' octave number
    '''
    def getOctave(self):
        return int(self.index / 12)

    ''' Get index number from note string
    '''
    @classmethod
    def index_from_string(cls, note):
        octave = 4
        note = note.strip().lower()
        if note[-1].isdigit():
            note, octave = note[:-1], int(note[-1])
        if len(note) > 1:
            note = cls.normalize(note)
        return cls.NOTES.index(note) + 12 * octave

    ''' Translate accidentals and normalize flats to sharps
        For example E#->F, F##->G, Db->C#
    '''
    @classmethod
    def normalize(cls, note):
        index = cls.NOTES.index(note[0].lower())
        for accidental in note[1:]:
            if accidental == '#':
                index += 1
            elif accidental == 'b':
                index -= 1
        return cls.NOTES[index % 12]

    ''' Return new instance of note at given octave
    '''
    def at_octave(self, octave):
        return Note((self.index % 12) + 12 * octave, self.volume)

    ''' Return transposed note by halfstep delta
    '''
    def transpose(self, halfsteps):
        return Note(self.index + halfsteps, self.volume)

    ''' Return frequency of note
    '''
    def frequency(self):
        return 16.35159783128741 * 2.0 ** (float(self.index) / 12.0)

    def second(self, scale='major'):
        from scale import Scale
        scale = Scale(self, scale)
        return scale.transpose(self, 1)
    def third(self, scale='major'):
        from scale import Scale
        scale = Scale(self, scale)
        return scale.transpose(self, 2)
    def fourth(self, scale='major'):
        from scale import Scale
        scale = Scale(self, scale)
        return scale.transpose(self, 3)
    def fifth(self, scale='major'):
        from scale import Scale
        scale = Scale(self, scale)
        return scale.transpose(self, 4)
    def sixth(self, scale='major'):
        from scale import Scale
        scale = Scale(self, scale)
        return scale.transpose(self, 5)
    def seventh(self, scale='major'):
        from scale import Scale
        scale = Scale(self, scale)
        return scale.transpose(self, 6)
    def octave(self, scale='major'):
        from scale import Scale
        scale = Scale(self, scale)
        return scale.transpose(self, 7)
    def triad(self, scaleType='major'):
        from scale import Scale
        from notes import Notes
        scale = Scale(self, scaleType)
        return Notes([self, self.third(scaleType), self.fifth(scaleType)])
    
    # '''
        # Transpose note by amount in given scale (scaletype, amt)
    # '''
    # def __rshift__(self,tuple):
        # if type(tuple) == type(3):
            # scale = Scale(self, 'major')
            # return scale.transpose(self,tuple)
        # else:
            # scaleType = tuple[0]
            # amt = tuple[1]
            # scale = Scale(self, scaleType)
            # return scale.transpose(self,amt)
        