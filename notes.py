from musical.theory import Note, Scale
from timeline import Hit, Timeline
from musical.audio import playback, source

class Notes:
    def __init__(self, *noteStrList):
        # Keep track of currect note placement time in seconds
        self.elapsedTime = 0.0
        self.timeDelta = 0.25
        self.noteLength = 0.25
        self.volume = 0.75
        self.notes = []
        
        #Notes(('A3', 1.0, 0.5)) gives Note('A3') for 1.0 seconds at 0.5 volume
        for noteStr in noteStrList:
            self.append(noteStr)
    

    ''' 
        Return scale starting from root
    '''
    @classmethod
    def scale(cls, rootStr, scale='major'):
        if type(rootStr) == type((0,0)):
            root = rootStr[0]
        else:
            root = Note(rootStr)
        newNotes = Notes()
        
        scale = Scale(root, scale)
        newNotes.append(root)
        for i in range(1,len(scale.intervals)+1):
            newNotes.append(scale.transpose(root,i))
        return newNotes
    ''' 
        Return arpeggio of "root" within "scale"
    '''
    @classmethod
    def arpeggio(cls, rootStr, scale='major'):
        if type(rootStr) == type((0,0)):
            root = rootStr[0]
        else:
            root = Note(rootStr)
        newNotes = Notes()
        scale = Scale(root, scale)
        newNotes.append(root)
        newNotes.append(scale.transpose(root, 2))
        newNotes.append(scale.transpose(root, 4))
        return newNotes
        
    ''' Return chord progression of scale instance as a list.
        Octave of tonic chord is at "base_octave"
    '''
    def progression(self, scaleType='major', base_octave=3):
        newNotes = Notes()
        for (root,time,length) in self.notes:
            newNotes = newNotes.extend(Notes.triad(root,scaleType))
        return newNotes

    '''
        Change tempo of notes.
    '''
    def changeTempo(self, newDelta):
        newNotes = self.new()
        newNotes.timeDelta = newDelta
        for (note,time,noteLen) in self.notes:
            newNotes.append(note)
        return newNotes


    '''
        Shift notes by shiftDist in the key. If note not in key, then not shifted.
    '''
    def shift(self, shiftDist, scaleType='major', key=None):
        if key == None:
            key = self.notes[0][0].note
        newNotes = self.new()
        
        #hacky
        def rootAtC(scale):
            if 'c' in scale:
                index = scale.index('c')
            elif 'c#' in scale:
                index = scale.index('c#')
            elif 'd' in scale:
                index = scale.index('d')
            else:
                index = scale.index('d#')
            for i in range(index):
                scale.append(scale.pop(0))
            return scale
        
        scale = [note.note for (note,time,noteLen) in Notes.scale(key, scaleType)[:-1].notes]
        scale = rootAtC(scale)
        # chromatic = [note.note for (note,time,noteLen) in Notes.scale(key, 'chromatic')[:-2].notes]
        # chromatic = rootAtC(chromatic)
        
        # for note in [nt for (nt,time,noteLen) in self.notes]:
        for (note,time,noteLen) in self.notes:
            if note.note in scale:
                # print note.value, time, noteLen
                octave = note.getOctave()
                index = scale.index(note.note)
                if (index+shiftDist)> len(scale) - 1:
                    octave += 1
                elif (index+shiftDist) < 0:
                    octave -= 1
                shifted = scale[(index + shiftDist)%len(scale)] + str(octave)
                shiftedNote = Note(shifted, note.volume)
                # print shiftedNote.value,time,noteLen
                newNotes.append((shiftedNote, time,noteLen))
            else:#not in scale. if there is time, do chroma->scale shift
                newNotes.append((note.value,time,noteLen))
                # index = chromatic.index(note.note)
                # if chromatic[index+1] in scale:
                    # newShift = shiftDist - 1
                
                # print note.note + ' not in scale\n'
        # print scale
        # print [note.value for (note,time,noteLen) in self]
        # print [note.value for (note,time,noteLen) in newNotes]
        newNotes.elapsedTime = self.elapsedTime
        return newNotes
                    

    '''
        Returns all notes in the Notes object as a chord
    '''    
    def allChorded(self):
        newNotes = self.new()
        newNotes.notes = [(note,0,1.0) for (note,time,noteLen) in self.notes]
        return newNotes
        
    '''
        Adds specified note to play with note at index.
    '''
    def chord(self, noteStr, index=-1):
        if type(noteStr) == type((0,0)):
            note = noteStr[0]
        else:
            note = Note(noteStr)
        prev = self.notes[index]
        time = prev[1]
        noteLen = prev[2]
        self.notes.insert(index,(note,time,noteLen))
        return self               
    '''
        Return copy with new volume.
    '''
    def withVolume(self,vol):
        newNotes = self.new()
        for (note,time,noteLen) in self.notes:
            newNote = Note(note, vol)
            newNotes.notes.append((newNote,time,noteLen))
        newNotes.volume = vol
        # print newNotes
        return newNotes
    
    '''
        Put notes at this absolute time.
    '''
    def putAt(self,absTime):
        newNotes = self.new()
        for (note,time,noteLen) in self.notes:
            newNotes.notes.append((note,time+absTime,noteLen))
        newNotes.elapsedTime += absTime
        return newNotes
    '''
        Sorts self.notes
    '''
    def sort(self):
        self.notes = sorted(self.notes,key=lambda x:x[1])
        return self
    
    '''
        Delay notes by a specified amount of time.
    '''
    def delay(self, delayTime):
        newNotes = self.new()
        newNotes.elapsedTime += delayTime
        for (note, time, noteLen) in self.notes:
            newNotes.notes.append((note,time+delayTime,noteLen))
        return newNotes
        
    '''
        Doubles notes, (C-D turns into CC-DD) with delay being how long after the original the double is played.
    '''
    def double(self, delay):
        newNotes = self.copy()
        for (note,time,noteLen) in self.notes:
            newNotes.notes.append((note, time+delay,noteLen))
        return newNotes
    
    '''
        Reverse note sequence. Times and note lengths are still all the same.
    '''
    def reverse(self):     
        timeList = sorted(self.notes, key=lambda x: x[1])
        timeMap = {}
        i = 1
        for (note,time,noteLen) in timeList:
            timeMap[time] = timeList[-i][1]
            i = i + 1
            
        newNotes = self.new()
        for (note, time, noteLen) in self.notes:
            newNotes.notes.append((note,timeMap[time],noteLen))
        newNotes = newNotes.sort()
        return newNotes
    '''
        Repeat note sequence. Does not mutate.
    '''
    def repeat(self, times=2):
        newSelf = self.copy()
        localElapsed = 0
        repeatedNotes = []
        
        for (note,time,noteLen) in newSelf.notes:
            for i in range(1,times):
                repeatedNotes.append((note,time + i*newSelf.elapsedTime,noteLen))
        newSelf.notes.extend(repeatedNotes)
        newSelf.elapsedTime *= times
        return newSelf
        
        
    


 


    '''
        Overlaying two Notes objects will play them at the same time.
    '''  
    def overlay(self,notes2):
        newNotes = self.copy()
        for (note, time, noteLen) in notes2.notes:
            newNotes.notes.append((note,time,noteLen))
        newNotes.elapsedTime = max(self.elapsedTime, notes2.elapsedTime)
        return newNotes
        
    '''
        Append each note in a notes object to end
    '''
    def extend(self, notesObj, noteLength=None, elapsed=None):
        newNotes = self.new()
        if elapsed == None:
            elapsed = self.elapsedTime
            
        for (note, time, noteLen) in self.notes:
            newNotes.notes.append((note,time,noteLen))
            
        for (note, time, noteLen) in notesObj.notes:
            newNotes.notes.append((note,time + elapsed,noteLen))
            
        newNotes.elapsedTime = self.elapsedTime + notesObj.elapsedTime
        return newNotes
    
    '''
        Append note to the end of the sequence. Will increment time.
    '''   
    def append(self, noteStr, noteLength=None, volume=None):
        if noteLength == None:
            noteLength = self.noteLength
        if volume == None:
            volume = self.volume
        
        if type(noteStr) == type(''):#note
            if noteStr == '-':
                self.elapsedTime += self.timeDelta
            else:
                note = Note(noteStr, self.volume)
                #add a note at a time
                self.notes.append((note, self.elapsedTime, self.noteLength))
                self.elapsedTime += self.timeDelta
                
        elif type(noteStr) == type((0,0)):#(note,noteLength,vol)
            if noteStr[0] == '-':
                self.elapsedTime += self.timeDelta*noteStr[1]/noteLength
            elif type(noteStr[0]) == type(Note('C')):
                self.notes.append(noteStr)
                self.elapsedTime += self.timeDelta
            else:
                note = Note(noteStr[0], self.volume)
                if len(noteStr) > 2:
                    note = Note(noteStr[0], noteStr[2])
                self.notes.append((note, self.elapsedTime, noteStr[1]))
                self.elapsedTime += self.timeDelta
                
        elif type(noteStr) == type([]):#chord
            for noteStr2 in noteStr:
                if type(noteStr2) == type(''):#note
                    if noteStr2 == '-':
                        self.elapsedTime += self.timeDelta
                    else:
                        note = Note(noteStr2, self.volume)
                        #add a note at a time
                        self.notes.append((note, self.elapsedTime, self.noteLength))
                elif type(noteStr2) == type((0,0)):#(note,time,vol)
                    if noteStr2[0] == '-':
                        self.elapsedTime += self.timeDelta*noteStr2[1]/noteLength
                    else:
                        note = Note(noteStr2[0], self.volume)
                        if len(noteStr2) > 2:
                            note = Note(noteStr2[0], noteStr2[2])
                        self.notes.append((note, self.elapsedTime, noteStr2[1]))
                elif type(noteStr2) == type(Note('C')):#Note obj
                    self.notes.append((noteStr2,self.elapsedTime,self.noteLength))
            self.elapsedTime += self.timeDelta
        elif type(noteStr) == type(Note('C')):
            self.notes.append((noteStr,self.elapsedTime,self.noteLength))
            self.elapsedTime += self.timeDelta
            # self.append(str(noteStr.note)+str(noteStr.octave))
        return self
    
    '''
        Return copy of notes with noteStr appended without mutating original.
    '''    
    def withNote(self, noteStr):
        newNotes = self.copy()
        newNotes.append(noteStr)
        return newNotes
    '''
        Remove a note at a specified index. Mutates self
    '''
    def remove(self, index, noteLength=None):
        self.notes.pop(index)
        return self
    '''
        Remove a note at a specified index. Does not mutate self.
    '''
    def without(self, index, noteLength=None):
        newNotes = self.copy()
        newNotes.notes.pop(index)
        return newNotes
     
    '''
        Replaces note at index with new note.
    '''
    def replace(self, new, index):
        newNotes = self.copy()
        newNotes[index] = new
        return newNotes
    '''
        Returns empty instance of Notes with same timeDelta, notelength, volume, elapsedTime.
    '''    
    def new(self):
        newNotes = Notes([])
        newNotes.elapsedTime = self.elapsedTime
        newNotes.timeDelta = self.timeDelta
        newNotes.noteLength = self.noteLength
        newNotes.volume = self.volume
        newNotes.notes = []
        return newNotes
    '''
        Copy notes
    '''
    def copy(self):
        newSelf = Notes([])
        newSelf.elapsedTime = self.elapsedTime
        newSelf.timeDelta = self.timeDelta
        newSelf.noteLength = self.noteLength
        newSelf.volume = self.volume
        
        #Note is separated into (note, time, length)
        for (note,time,len) in self.notes:
            newNote = Note(note, self.volume)
            newSelf.notes.append((newNote,time,len))
        return newSelf
        
    '''
        Print notes
    '''
    def __repr__(self):
        return str(self.notes)
    
    '''
        Returns number of unique notes.
    '''
    def __len__(self):
        return len(self.notes)
        
    '''
        Get note at index
    '''
    
    def __getitem__(self, index=0):
        return self.notes[index]
    '''
        Set note at index
    '''
    def __setitem__(self, key, value):
        note = self.notes[key]
        self.notes[key] = (Note(value,note[0].volume), note[1], note[2])
        return self
        
    '''
        Get note at slice
    '''
    def __getslice__(self, index1, index2):
        newNotes = self.new()
        newNotes.notes = self.notes[index1:index2]
        startTime = None
        notesList = []
        for (note,time,noteLen) in newNotes.notes:
            if startTime == None:
                startTime = time
            notesList.append((note,time-startTime,noteLen))
        if index2 > len(self.notes):
            newNotes.elapsedTime = self.notes[len(self.notes)-1][1] - self.notes[index1][1]
        else:
            newNotes.elapsedTime = self.notes[index2][1] - self.notes[index1][1]
        newNotes.notes = notesList
        return newNotes

    '''
        Overload / with overlay.
    '''
    def __div__(self, other):
        return self.overlay(other)
    def __truediv__(self, other):
        return self.overlay(other)
        
    '''
        Set volume to vol
    '''
    def __mod__(self, vol):
        return self.withVolume(vol)
        
    '''
        Scale note length of all notes by scale.
    '''
    def __pow__(self,scale):
        newNotes = self.new()
        for (note, time, noteLen) in self.notes:
            newLen = noteLen * scale
            newNotes.notes.append((note,time,newLen))
        return newNotes
    '''
        Reverse notes
    '''
    def __invert__(self):
        return self.reverse()
    '''
        Adding two Notes objects will add then together. If you want to play one after the other, use extend.
    '''
    def __add__(self,notes2):
        if type(notes2) == type(Notes('C4','C5')):
            return self.extend(notes2)
        return self.withNote(notes2)
        
    '''
        Will shift notes by given amount
    '''
    def __rshift__(self,shiftAmt):
        if type(shiftAmt) == type((0,0)):
            if len(shiftAmt) == 2:
                return self.shift(shiftAmt[0],shiftAmt[1])
            else:
                return self.shift(shiftAmt[0],shiftAmt[1], shiftAmt[2])
        return self.shift(shiftAmt)
    def __lshift__(self,shiftAmt):
        if type(shiftAmt) == type((0,0)):
            if len(shiftAmt) == 2:
                return self.shift(-shiftAmt[0],shiftAmt[1])
            else:
                return self.shift(-shiftAmt[0],shiftAmt[1], shiftAmt[2])
        return self.shift(-shiftAmt)
    '''
        Repeat notes n times
    '''
    def __mul__(self,n):
        return self.repeat(n)
    '''
        Will put start time of notes at n
    '''
    def __lt__(self,n):
        return self.putAt(n)
    def __le__(self,n):
        return self.putAt(n)
        
    '''
        Return elapsed time since beginning
    '''
    def getElapsedTime(self):
        return self.elapsedTime
    '''
        Set elapsed time since beginning
    '''
    def setElapsedTime(self, time):
        self.elapsedTime = time
        return self
    
    '''
        Play the notes
    '''
    def play(self):
        print "Rendering timeline..."
        timeline = Timeline()
        for (note, time, noteLen) in self.notes:
            timeline.add(time, Hit(note, noteLen, 'pluck'))
        render = timeline.render()
        print "Playing notes..."
        playback.play(render)