from .base import LoginRequiredMixin
from ..forms import SongForm, InstrumentForm
from django.urls import reverse
from django.shortcuts import render,redirect, HttpResponseRedirect
from django.views import generic
from ..models import Profile, Song, SongPart, InstrumentPart

# Multi step creation of songs
def addSongStep1(request):

    # Maintain these variables in the session
    args = ['title', 'artist', 'key']
    initial = {}

    for argument in args:
        initial[argument] = request.session.get(argument, None)

    # The first step uses the SongForm form
    form = SongForm(request.POST or None, initial=initial)

    if request.method == 'POST':
        if form.is_valid():

            # Save data from the first step
            for argument in args:
                request.session[argument] = form.cleaned_data[argument]

            song = form.save(commit=False)

            cur_song = request.session.get('song', None)
            prev_song = Song.objects.filter(pk=cur_song).first()
            # If the song has already been created update it otherwise create a new song
            if cur_song is None or prev_song is None:
                song.save()
                request.session['song'] = song.pk
            else:
                prev_song = song
                prev_song.save()

            # Go the the second step
            return HttpResponseRedirect(reverse('musicnotes:add-song-2'))

    return render(request, 'musicnotes/add_song_1.html', {'form': form})


def addSongStep2(request):

    if request.method == 'GET':
        song = Song.objects.get(pk=request.session.get('song', None))
        song_parts = SongPart.objects.filter(song=song)
        context = {}
        context['song'] = song
        context['song_part_list'] = song_parts
        context['new_parts'] = ['Intro', 'Verse', 'Chorus', 'Bridge', 'Solo', 'Intermezzo', 'Outro']
        context['existing_parts'] = filterParts(song_parts)

        return render(request, 'musicnotes/add_song_2.html', context=context)

    if request.method == 'POST':
        return render(request, 'musicnotes/add_song_3.html')



def addSongStep3(request):

    song = Song.objects.get(pk=request.session.get('song', None))
    song_parts = filterParts(SongPart.objects.filter(song=song))
    form = InstrumentForm(request.POST or None, initial={'capo': 0, 'music': " "})

    if request.method == 'POST':

        for part in song_parts:
            if str(part.pk) in request.POST:
                instrument_part = form.save(commit=False)

                instrument_exists = InstrumentPart.objects.filter(song_part=part, instrument='chords').first()
                if instrument_exists:
                    break

                if instrument_part.capo == None:
                    instrument_part.capo = 0

                instrument_part.song_part = part
                instrument_part.instrument = "chords"
                instrument_part.music = parseChords(instrument_part.music)
                instrument_part.save()

                break

    instrument_parts = []
    for part in song_parts:
        instrument_part = InstrumentPart.objects.filter(song_part=part).first()
        if instrument_part is not None:
            instrument_parts.append(instrument_part)
        else:
            instrument_parts.append(None)

    context = {}
    context['song'] = song
    context['form'] = form
    context['song_part_list'] = song_parts
    context['instrument_part_list'] = instrument_parts

    return render(request, 'musicnotes/add_song_3.html', context=context)


def finishSong(request):
    del request.session['song']
    request.session.modified = True

    return redirect('musicnotes:index')


class SongDetailView(LoginRequiredMixin, generic.DetailView):
    model = Song
    template_name = 'musicnotes/song_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SongDetailView, self).get_context_data(**kwargs)
        song = context['song']

        song_parts = filterParts(SongPart.objects.filter(song=song))
        print(song_parts)
        instrument_parts = []
        for part in song_parts:
            instrument_parts.append(InstrumentPart.objects.get(song_part=part, instrument='chords'))

        context['instrument_part_list'] = instrument_parts

        return context


def addSongPart(request, type_nr):
    parts = ['Intro', 'Verse', 'Chorus', 'Bridge', 'Solo', 'Intermezzo', 'Outro']
    part = parts[int(type_nr)]

    song = Song.objects.get(pk=request.session.get('song', None))

    song_parts = SongPart.objects.filter(song=song)
    #last_object = song_parts.order_by('-number').first()

    identifier = getLetterCount(song_parts.filter(type_name=part).count() + 1)
    song_part = SongPart.objects.create(song=song,
                                        number=song_parts.count()+1,
                                        type_name=part,
                                        identifier=identifier,
                                        count=1)
    song_part.save()

    return redirect(reverse('musicnotes:add-song-2'))


def addExistingSongPart(request, pk):

    song = Song.objects.get(pk=request.session.get('song', None))

    part = SongPart.objects.get(pk=pk)
    last_object = SongPart.objects.filter(song=song).order_by('-number').first()

    if last_object is not None and last_object.type_name == part.type_name and last_object.identifier == part.identifier:

        last_object.count += 1
        last_object.save()

    else:
        song_part = SongPart.objects.create(song=song,
                                            number=last_object.number+1,
                                            type_name=part.type_name,
                                            identifier=part.identifier,
                                            count=1)
        song_part.save()

    return redirect(reverse('musicnotes:add-song-2'))


def removeSongPart(request, pk):
    song_part = SongPart.objects.get(pk=pk)
    song_part.delete()

    return redirect(reverse('musicnotes:add-song-2'))


def getLetterCount(count):
    return str(chr(count+0x40))


def filterParts(parts):
    result = []

    for part in parts:

        part_present = False
        for item in result:
            if part.type_name == item.type_name and part.identifier == item.identifier:
                part_present = True
                break

        if not part_present:
            result.append(part)

    return result

def getEmptyTab(length):
    open_notes = ['e', 'B', 'G', 'D', 'A', 'E']
    result = ''
    for note in open_notes:
        result += note + ' |'
        for i in range(0, length):
            result += '-'

        result += '|\n'

    return result


def parseChords(input):

    result = ''

    input = input.strip()
    measures = input.split("|")
    first = True
    for measure in measures:
        measure = measure.strip()
        chords = measure.split()
        current = '&nbsp;&nbsp;&nbsp;&nbsp;'.join(chords)

        if first:
            result = current
            first = False
        else:
            result = '<br><br>'.join((result, current))

        # for chord in chords:
        #     result += chord
        #     result += '&nbsp;&nbsp;&nbsp;&nbsp;'

    return result

    # def step1(request):
    #     initial = {'fn': request.session.get('fn', None)}
    #     form = PersonForm(request.POST or None, initial=initial)
    #     if request.method == 'POST':
    #         if form.is_valid():
    #             request.session['fn'] = form.cleaned_data['fn']
    #             return HttpResponseRedirect(reverse('step2'))
    #     return render(request, 'step1.html', {'form': form})
    #
    # def step2(request):
    #     form = PetForm(request.POST or None)
    #     if request.method == 'POST':
    #         if form.is_valid():
    #             pet = form.save(commit=False)
    #             person = Person.objects.create(fn=request.session['fn'])
    #             pet.owner = person
    #             pet.save()
    #             return HttpResponseRedirect(reverse('finished'))
    #     return render(request, 'step2.html', {'form': form})

