# from django.http import request
from todproof_proj.settings import AUTH_USER_MODEL
from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Contribution, Edit, Message, Lookup, Translation, Assignment, Sentence
from .forms import MessageForm, TranslationForm, AssignmentForm, SentenceForm
from django.contrib import messages
import re

def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
  return render(request, 'todproof/home.html', {})

###############################################################################
# Message
###############################################################################

def index_messages(request):
  message_list = Message.objects.all().order_by('title')#sort by date instead of title
  return render(request, 'todproof/index_messages.html', {'message_list': message_list})

def show_message(request, message_id):
  message = Message.objects.get(pk=message_id)
  translations = message.translations
  return render(request, 'todproof/show_message.html', {'message': message, 'translations': translations})
  # return render(request, 'todproof/show_message.html', {'message': message})

def create_message(request):
  if request.method == 'POST':
    form = MessageForm(request.POST)
    if form.is_valid():
      try:
        message = form.save()
        model = form.instance
        # return redirect('index-messages')
        return redirect(f'/messages/{message.id}/')
      except:
        pass
    # print('post')
    # return HttpResponse("<a class='dropdown-item' href='#'>Translations</a>")
  elif request.method == 'GET':
    form = MessageForm()
    # print('get')
    return render(request, 'todproof/create_message.html', {'form': form})

def update_message(request, message_id):
  message = Message.objects.get(pk=message_id)
  form = MessageForm(initial={'dod': message.dod, 'tod': message.tod, 'dow': message.dow, 'title': message.title, 'descriptor': message.descriptor})
  if request.method == 'POST':
    form = MessageForm(request.POST, instance=message)
    if form.is_valid():
      try:
        form.save()
        model = form.instance
        print('Message id=' + message_id + ' updated successfully')
        return redirect(f'/messages/{message_id}/')
      except Exception as e:
        print('Message update failure: ' + e)
        pass
    else:
      print('form is not valid')
  elif request.method == 'GET':
    form = MessageForm(initial={'dod': message.dod, 'tod': message.tod, 'dow': message.dow, 'descriptor': message.descriptor, 'title': message.title })
    return render(request, 'todproof/update_message.html', {'message': message, 'form': form})

def delete_message(request, message_id):
  message = Message.objects.get(pk=message_id)
  try:
    message.delete()
    print('Message delete success')
  except Exception as e:
    print('Message delete failure: ' + e)
    pass
  return redirect('index-messages')
  # return redirect(f'/messages/')

def search_messages(request):
  if request.method == 'POST':
    searched = request.POST['searched']
    # messages = Message.objects.filter(title__contains=searched).filter(descriptor__contains=searched)
    messages = Message.objects.filter(title__contains=searched)
    # messages = Message.objects.filter(descriptor__contains=searched)

    return render(request, 'todproof/search_messages.html', {'searched':searched,'messages':messages})
  else:
    return render(request, 'todproof/search_messages.html', {})    

###############################################################################
# Translation
###############################################################################

def index_all_translations(request):
  translation_list = Translation.objects.all()
  return render(request, 'todproof/index_all_translations.html', {'translation_list': translation_list})

def index_message_translations(request, message_id):
  message = Message.objects.get(pk=message_id)
  translations = message.translations.all
  # return redirect('/')
  return render(request, 'todproof/show_message.html', {'message': message, 'translations': translations})

def show_translation(request, message_id, translation_id):
  # return redirect('/')
  # return HttpResponse("<a class='dropdown-item' href='#'>Translations</a>")
  # return redirect('show')
  message = Message.objects.get(pk=message_id)
  translation = Translation.objects.get(pk=translation_id)
  assignments = translation.assignments.all
  sentences = translation.sentences.all
  lookups = translation.lookups.all
  return render(request, 'todproof/show_translation.html', {'message': message, 'translation': translation, 'assignments': assignments, 'sentences': sentences, 'lookups': lookups})

def create_translation(request, message_id):
  if request.method == 'POST':
    form = TranslationForm(request.POST)
    if form.is_valid():
      try:
        # form.save()
        translation = form.save()
        message = Message.objects.get(pk=message_id)
        # translation = Translation.objects.get(pk=translation_id)
        translation = Translation.objects.get(pk=translation.id)
        translation.message_id = message_id
        translation.save()
        # model = form.instance
        # return redirect('index-translations')
        # message
        return render(request, 'todproof/show_message.html', {'message': message})
      except:
        pass
    # print('post')
    # return HttpResponse("<a class='dropdown-item' href='#'>Translations</a>")
  elif request.method == 'GET':
    form = TranslationForm()
    # print('get')
    return render(request, 'todproof/create_translation.html', {'form': form})

def update_translation(request, message_id, translation_id):
  message = Message.objects.get(pk=message_id)
  translation = Translation.objects.get(pk=translation_id)
  form = TranslationForm(initial={'lan': translation.lan, 'tran_title': translation.tran_title, 'eng_tran': translation.eng_tran, 'descrip': translation.descrip, 'blkc': translation.blkc, 'subc': translation.subc, 'senc': translation.senc, 'xcrip': translation.xcrip, 'li': translation.li, 'pubdate': translation.pubdate, 'version': translation.version })
  if request.method == 'POST':
    form = TranslationForm(request.POST, instance=translation)
    if form.is_valid():
      try:
        form.save()
        model = form.instance
        print('Translation id=' + translation_id + ' updated successfully')
        # return redirect(f'/messages/{message_id}/translations/{translation_id}/')
        return redirect(f'/messages/{message_id}/')
        # return render(request, 'todproof/show_message_translation.html', {'message': message, 'translation': translation})
        # return redirect('index-translations')
      except Exception as e:
        # print('Translation update failure: ' + e)
        pass
    else:
      print('form is not valid')  
  elif request.method == 'GET':
    form = TranslationForm(initial={'lan': translation.lan, 'tran_title': translation.tran_title, 'eng_tran': translation.eng_tran, 'descrip': translation.descrip, 'blkc': translation.blkc, 'subc': translation.subc, 'senc': translation.senc, 'xcrip': translation.xcrip, 'li': translation.li, 'pubdate': translation.pubdate, 'version': translation.version })
    return render(request, 'todproof/update_translation.html', {'message': message, 'translation': translation, 'form': form})

def delete_translation(request, message_id, translation_id):
  translation = Translation.objects.get(pk=translation_id)
  message = Message.objects.get(pk=message_id)
  try:
    translation.delete()
    print('Translation delete success')
  except Exception as e:
    print('Translation delete failure: ' + e)
  # return redirect(f'/messages/{message_id}/translations/')
  return redirect(f'/messages/{message_id}/')

# from .forms import UploadFileForm
# def lookup_link(request, message_id, translation_id):
#   if request.method == 'POST':
#     form = UploadFileForm(request.POST, request.FILES)
#     if form.is_valid():
#       handle_uploaded_file(request.FILES['myfile'])
#       # return HttpResponseRedirect('/success/url/')
#       return redirect(f'/messages/{message_id}/translations/{translation_id}')
#   else:
#     form = UploadFileForm()
#   return render(request, 'todproof/upload.html', {'form': form})

# https://stackoverflow.com/questions/50521674/how-to-convert-content-of-inmemoryuploadedfile-to-string
def handle_lookup_file(f, translation_id):
  # print(f.name); print(f.size); print(f)
  translation = Translation.objects.get(pk=translation_id)
  str_text = ''
  for line in f: str_text = str_text + line.decode(); # "str_text" will be of `str` type
  str_split = str_text.split('\n')#; print(str_split)
  num_of_lookups = 0
  for line in str_split:
    if line.strip(): #non-empty after strip
      print(line)
      # get line parts
      line_parts = line.split(' ')
      blk = line_parts[0]
      sub = line_parts[1]
      rsub = line_parts[2]
      # create lookup
      new_lookup = Lookup(blk=blk, sub=sub, rsub=rsub, translation=translation)
      new_lookup.save()
      if new_lookup:
        print(f"new_lookup: {new_lookup.blk} {new_lookup.sub} {new_lookup.rsub}")
      else:
        print(f"ERROR: Could not create lookup {new_lookup.blk} {new_lookup.sub} {new_lookup.rsub}")
        # flash[:danger] = "ERROR: Could not create lookup #{new_lookup.blk} #{new_lookup.sub} #{new_lookup.rsub}"
      new_lookup = None
      num_of_lookups += 1
  # mark as imported
  Translation.objects.filter(id=translation_id).update(li=True)

def import_lookup(request, message_id, translation_id):
  if request.method == 'POST':
    handle_lookup_file(request.FILES['document'], translation_id)
    return redirect(f'/messages/{message_id}/translations/{translation_id}')
  else:
    return render(request, 'todproof/upload.html')

def delete_lookup(request, message_id, translation_id):
  translation = Translation.objects.get(pk=translation_id)
  # determine the lookups to be deleted
  # lookups = translation.lookups
  lookups = Lookup.objects.filter(translation_id=translation_id)
  num_of_lookups = len(lookups)
  print(f"num_of_lookups: {num_of_lookups}")
  if num_of_lookups > 0:
    for lookup in lookups:
      lookup.delete()
    #mark as not imported 
    Translation.objects.filter(id=translation_id).update(li=False)
    # flash[:danger] = "#{num_of_lookups} lookups for this translation deleted"
  else:
    pass
    # flash[:danger] = 'No lookups for this translation deleted'
  return redirect(f'/messages/{message_id}/translations/{translation_id}')

###############################################################################
# Sentence
###############################################################################

# def index_translation_sentences(request, translation_id):
#   translation = Translation.objects.get(pk=translation_id)
#   sentences = translation.sentences.all
#   # return redirect('/')
#   return render(request, 'todproof/show_document_translation.html', {'translation': translation, 'sentences': sentences})

def sentence_vote_time(sentence):
  # svc = sentence_vote_contribution(sentence)
  # if svc
  #   svc.effort_in_seconds
  # else
  #   0
  return 7.7

def sentence_create_time(sentence):
  # sccs = sentence_create_contributions(sentence)
  # sccs.sum("effort_in_seconds")
  return 8.8

def show_sentence(request, translation_id, sentence_id):
  translation = Translation.objects.get(pk=translation_id)
  sentence = translation.sentences.get(pk=sentence_id)

  # session_context = Assignment.objects.filter(pk=get_current_user().cur_assign.id)[0].context
  session_context = Assignment.objects.get(pk=get_current_user().cur_assign.id).context
  print('session_context = ', session_context)
  # Assignment.objects.filter(pk=get_current_user().cur_assign.id).update(context=2)
  # session_context = 2

  #update pred_E_edits
  # @pred_E_edits = Edit.joins(sentence: :translation).where(translations: {id: @sentence.translation.eng_tran_id}, sentences: {rsen: @sentence.rsen-session[:context]..@sentence.rsen-1})
  pred_E_edits = Edit.objects.select_related().filter(sentence__translation__id=sentence.translation.eng_tran_id, sentence__rsen__range=(sentence.rsen-session_context, sentence.rsen-1))

  #update E_edit
  # @E_edit = Edit.joins(sentence: :translation).where(translations: {id: @sentence.translation.eng_tran_id}, sentences: {rsen: @sentence.rsen}).first
  E_edit = Edit.objects.select_related().filter(sentence__translation__id=sentence.translation.eng_tran_id, sentence__rsen=sentence.rsen)[0]

  #update succ_E_edits
  # @succ_E_edits = Edit.joins(sentence: :translation).where(translations: {id: @sentence.translation.eng_tran_id}, sentences: {rsen: @sentence.rsen+1..@sentence.rsen+session[:context]})
  succ_E_edits = Edit.objects.select_related().filter(sentence__translation__id=sentence.translation.eng_tran_id, sentence__rsen__range=(sentence.rsen+1, sentence.rsen+session_context))

  return render(request, 'todproof/show_sentence.html', 
    {'translation': translation, 'sentence': sentence, 'E_edit': E_edit, 'sentence_count': translation.sentences.count(), 
    'sentence_vote_time': sentence_vote_time(sentence), 'sentence_create_time': sentence_create_time(sentence), 'pred_E_edits': pred_E_edits, 'succ_E_edits': succ_E_edits})


def create_sentence(request, translation_id):
  translation = Translation.objects.get(pk=translation_id)
  if request.method == 'POST':
    form = SentenceForm(request.POST)
    if form.is_valid():
      try:
        # form.save()
        sentence = form.save()
        # translation = Translation.objects.get(pk=translation_id)
        sentence = Sentence.objects.get(pk=sentence.id)
        sentence.translation_id = translation_id
        sentence.save()
        return render(request, 'todproof/show_translation.html', {'translation': translation})
      except:
        pass
  elif request.method == 'GET':
    form = SentenceForm()
    return render(request, 'todproof/create_sentence.html', {'translation': translation, 'form': form})

def update_sentence(request, translation_id, sentence_id):
  sentence = Sentence.objects.get(pk=sentence_id)
  translation = Translation.objects.get(pk=translation_id)
  form = SentenceForm(initial={'blk': sentence.blk, 'sub': sentence.sub, 'rsub': sentence.rsub, 'sen': sentence.sen, 'rsen': sentence.rsen, 'typ': sentence.typ, 'tie': sentence.tie })
  if request.method == 'POST':
    form = SentenceForm(request.POST, instance=sentence)
    if form.is_valid():
      try:
        form.save()
        model = form.instance
        print('Sentence id=' + sentence_id + ' updated successfully')
        return redirect(f'/translations/{translation_id}/sentences/{sentence_id}')
      except Exception as e:
        # print('Sentence update failure: ' + e)
        pass
    else:
      print('form is not valid')  
  elif request.method == 'GET':
    form = SentenceForm(initial={'blk': sentence.blk, 'sub': sentence.sub, 'rsub': sentence.rsub, 'sen': sentence.sen, 'rsen': sentence.rsen, 'typ': sentence.typ, 'tie': sentence.tie })
    return render(request, 'todproof/update_sentence.html', {'translation': translation, 'sentence': sentence, 'form': form})

def delete_sentence(request, translation_id, sentence_id):
  sentence = Sentence.objects.get(pk=sentence_id)
  translation = Translation.objects.get(pk=translation_id)
  try:
    sentence.delete()
    print('Sentence delete success')
  except Exception as e:
    print('Sentence delete failure: ' + e)
  return redirect(f'/messages/{translation.message.id}/translations/{translation_id}')

def prev_sentence(request, translation_id, sentence_id):
  translation = Translation.objects.get(pk=translation_id)
  sentence = Sentence.objects.get(pk=sentence_id)

  #update rsen
  prev_rsen = sentence.rsen - 1
  if prev_rsen < 1:
    prev_rsen = 1
    print(f"This is the first sentence.")
    messages.error(request, f"This is the first sentence.")
  Assignment.objects.filter(pk=get_current_user().cur_assign.id).update(place=prev_rsen) #was: current_user.cur_assign.update(place: prev_rsen)

  #update @sentence
  sentence = translation.sentences.filter(rsen=prev_rsen)[0] #@sentence = @translation.sentences.where(rsen: prev_rsen).first

  return redirect(f'/translations/{translation_id}/sentences/{sentence.id}') 

def next_sentence(request, translation_id, sentence_id):
  translation = Translation.objects.get(pk=translation_id)
  sentence = Sentence.objects.get(pk=sentence_id)

  #update rsen
  next_rsen = sentence.rsen + 1
  if next_rsen > translation.senc:
    next_rsen = translation.senc
    print(f"This is the last sentence.")
    messages.error(request, f"This is the last sentence.")
  Assignment.objects.filter(pk=get_current_user().cur_assign.id).update(place=next_rsen) #was: current_user.cur_assign.update(place: next_rsen)

  #update @sentence
  sentence = translation.sentences.filter(rsen=next_rsen)[0] #@sentence = @translation.sentences.where(rsen: next_rsen).first

  return redirect(f'/translations/{translation_id}/sentences/{sentence.id}') 

def decrease_context(request, translation_id, sentence_id):
  translation = Translation.objects.get(pk=translation_id)
  sentence = Sentence.objects.get(pk=sentence_id)

  context = Assignment.objects.get(pk=get_current_user().cur_assign.id).context - 1
  if context < 0:
    Assignment.objects.filter(pk=get_current_user().cur_assign.id).update(context=0)
    print(f"This is the minimum context.")
    messages.error(request, f"This is the minimum context.")
  else:
    Assignment.objects.filter(pk=get_current_user().cur_assign.id).update(context=context)
  print('context = ', context)

  return redirect(f'/translations/{translation_id}/sentences/{sentence.id}') 

def increase_context(request, translation_id, sentence_id):
  translation = Translation.objects.get(pk=translation_id)
  sentence = Sentence.objects.get(pk=sentence_id)

  context = Assignment.objects.get(pk=get_current_user().cur_assign.id).context + 1
  if context > 10:
    Assignment.objects.filter(pk=get_current_user().cur_assign.id).update(context=10)
    print(f"This is the maximum context.")
    messages.error(request, f"This is the maximum context.")
  else:
    Assignment.objects.filter(pk=get_current_user().cur_assign.id).update(context=context)
  print('context = ', context)

  return redirect(f'/translations/{translation_id}/sentences/{sentence.id}') 

###############################################################################
# Assignment
###############################################################################

def index_assignments(request):
  assignment_list = Assignment.objects.all()
  return render(request, 'todproof/index_assignments.html', {'assignment_list': assignment_list})

def show_assignment(request, assignment_id):
  assignment = Assignment.objects.get(pk=assignment_id)
  return render(request, 'todproof/show_assignment.html', {'assignment': assignment})

def create_assignment(request):
  if request.method == 'POST':
    form = AssignmentForm(request.POST)
    if form.is_valid():
      try:
        assignment = form.save()
        model = form.instance
        # return redirect('index-messages')
        return redirect(f'/assignments/{assignment.id}/')
      except:
        pass
    # print('post')
    # return HttpResponse("<a class='dropdown-item' href='#'>Translations</a>")
  elif request.method == 'GET':
    form = AssignmentForm()
    # print('get')
    return render(request, 'todproof/create_assignment.html', {'form': form})

def update_assignment(request, assignment_id):
  assignment = Assignment.objects.get(pk=assignment_id)
  form = AssignmentForm(initial={'role': assignment.role, 'active': assignment.active, 'ci': assignment.ci, 'place': assignment.place, 'translation': assignment.translation, 'user': assignment.user, 'status': assignment.status, 'ccs': assignment.ccs, 'ccs_k': assignment.ccs_k, 'ccs_m': assignment.ccs_m, 'vcs': assignment.vcs, 'vcs_a': assignment.vcs_a, 'vcs_c': assignment.vcs_c, 'vcs_t': assignment.vcs_t, 'vcs_p': assignment.vcs_p, 'ct': assignment.ct, 'vt': assignment.vt, 'majtes': assignment.majtes, 'tietes': assignment.tietes, 'notes': assignment.notes})
  if request.method == 'POST':
    form = AssignmentForm(request.POST, instance=assignment)
    if form.is_valid():
      try:
        form.save()
        model = form.instance
        print('Assignment id=' + assignment_id + ' updated successfully')
        return redirect(f'/assignments/{assignment_id}/')
      except Exception as e:
        print('Assignment update failure: ' + e)
        pass
    else:
      print('form is not valid')
  elif request.method == 'GET':
    form = AssignmentForm(initial={'role': assignment.role, 'active': assignment.active, 'ci': assignment.ci, 'place': assignment.place, 'translation': assignment.translation, 'user': assignment.user, 'status': assignment.status, 'ccs': assignment.ccs, 'ccs_k': assignment.ccs_k, 'ccs_m': assignment.ccs_m, 'vcs': assignment.vcs, 'vcs_a': assignment.vcs_a, 'vcs_c': assignment.vcs_c, 'vcs_t': assignment.vcs_t, 'vcs_p': assignment.vcs_p, 'ct': assignment.ct, 'vt': assignment.vt, 'majtes': assignment.majtes, 'tietes': assignment.tietes, 'notes': assignment.notes})
    return render(request, 'todproof/update_assignment.html', {'assignment': assignment, 'form': form})

def delete_assignment(request, assignment_id):
  assignment = Assignment.objects.get(pk=assignment_id)
  try:
    assignment.delete()
    print('Assignment delete success')
  except Exception as e:
    print('Assignment delete failure: ' + e)
    pass
  return redirect('index-assignments')
  # return redirect(f'/assignments/')

def import_content_for_validation(request, assignment_id):
  if request.method == 'POST':
    # prepare file as list of strings
    str_text = ''
    for line in request.FILES['document']: str_text = str_text + line.decode()
    str_split = str_text.split('\n'); #print(str_split[:10])

    # remove title line
    str_split.pop(0)
    rsub_sen_ary = []
    for line in str_split:
      # line = line.strip()
      if line: #non-empty after strip, only non-blank lines
        print(line)
        # 1. test line for valid descriptor
        match = re.search('^[0-9]+\.[0-9]+\.[ncspqkhijv]\s', line)
        if match == None:
          print(f"ERROR: {line}")
          messages.error(request, f"ERROR: Invalid descriptor in line: {line}  (Validation failed. Import aborted.)")
          return redirect(f'/assignments/{assignment_id}/')
        # 2. test for unique rsub.sen combinations
        # get line parts
        line_parts = line.split(' ', 2) #split by space into 2 parts
        # get signature
        signature = line_parts[0]
        # get signature parts
        signature_parts = signature.split('.')
        rsub = signature_parts[0]
        sen = signature_parts[1]
        rsub_sen = rsub + '.' + sen; #print(f"rsub_sen: XXX{rsub_sen}XXX")
        if rsub_sen in rsub_sen_ary:
          print(f"ERROR: Duplicate rsub.sen combination found in line: {line}  (Validation failed. Import aborted.)")
          messages.error(request, f"ERROR: Duplicate rsub.sen combination found in line: {line}  (Validation failed. Import aborted.)")
          return redirect(f'/assignments/{assignment_id}/')
        else:
          rsub_sen_ary.append(rsub_sen)
    assignment = Assignment.objects.all().get(pk=assignment_id)
    required_unique_combinations = assignment.translation.senc #found_unique_combinations = rsub_sen_ary.uniq.length
    found_unique_combinations = len(rsub_sen_ary)
    print(f"Unique rsub.sen combinations required: {required_unique_combinations}")
    print(f"Unique rsub.sen combinations found: {found_unique_combinations}")
    messages.info(request, f"Unique rsub.sen combinations found: #{found_unique_combinations}, Required:  #{required_unique_combinations}.")
    return redirect(f'/assignments/{assignment_id}/')
  else:
    return render(request, 'todproof/upload.html')
  
# from django.core.exceptions import DoesNotExist
# from django.core.exceptions import ObjectDoesNotExist

def import_content(request, assignment_id):
  assignment = Assignment.objects.all().get(pk=assignment_id)
  # determine the kind of additions to be created
  role = assignment.role
  if role in ['MT', 'HT', 'NT']:
    kind = 'T'
  elif role in ['TE', 'CE', 'LA']: #both 'C' and 'V' kinds
    messages.error(request, f"Content import for role #{role} is not currently supported")
    return redirect(f'/assignments/{assignment_id}/')
  elif role in ['EE', 'SE', 'PE']: #'C' kind
    messages.error(request, f"Content import for role {role} is not currently supported")
    return redirect(f'/assignments/{assignment_id}/')
  elif role in ['EP']:
    kind = 'E'
  else:
    messages.error(request, f"ERROR: Invalid role: {role}")
    return redirect(f'/assignments/{assignment_id}/')

  if request.method == 'POST':
    # prepare file as list of strings
    str_text = ''
    for line in request.FILES['document']: str_text = str_text + line.decode()
    str_split = str_text.split('\n'); print(str_split[:10])

    str_split.pop(0) #remove title line
    num_of_contributions = 0
    for line in str_split:
      # line = line.strip()
      if line: #non-empty after strip, only non-blank lines
        print(line)

        # get line parts
        line_parts = line.split(' ', 1) #split by space into 2 parts

        # get signature
        signature = line_parts[0]

        # get content
        content = line_parts[1].strip() #remove NL at end: No NL here

        # get signature parts
        signature_parts = signature.split('.')
        rsub_num = int(signature_parts[0])
        sen_num = int(signature_parts[1])
        typ_char = signature_parts[2]; #print(f"==========={rsub_num}.{sen_num}============")

        #check if sentence already exists, if not, create
        # existing_sen = Sentence.joins(:translation).where(translations: {id: @assignment.translation_id}, sentences: {rsub: rsub_num, sen: sen_num})
        # try: 
        existing_sen = Sentence.objects.filter(translation__id=assignment.translation_id, rsub=rsub_num, sen=sen_num)
        if len(existing_sen) == 0:
          print('does not exist............')
          if assignment.translation.eng_tran is not None: #OTH
            # lookup = task.translation.eng_tran.lookups.where(rsub: rsub_num).first
            lookup = Lookup.objects.filter(translation_id=assignment.translation.eng_tran.id, rsub=rsub_num)[0]
          else: #ENG
            # lookup = task.translation.lookups.where(rsub: rsub_num).first
            lookup = Lookup.objects.filter(translation_id=assignment.translation.id, rsub=rsub_num)[0]; print('lookup:',lookup)
          blk_num = lookup.blk #was: blk_num = lookup.blk
          sub_num = lookup.sub #was: sub_num = lookup.sub
          # existing_sen = Sentence.create(rsen: num_of_contributions+1, blk: blk_num, sub: sub_num, rsub: rsub_num, sen: sen_num, typ: typ_char, tie: false, translation: @assignment.translation)
          existing_sen = Sentence.objects.create(rsen=num_of_contributions+1, blk=blk_num, sub=sub_num, rsub=rsub_num, sen=sen_num, typ=typ_char, tie=False, translation=assignment.translation)
        elif len(existing_sen) == 1:
            print('exists............')
            existing_sen = existing_sen[0] #was: existing_sen = existing_sen.first
        else:
            messages.error(request, f"There is more than one sentence with rsub: {rsub_num} and sen: {sen_num}. This is an error!")
            return redirect(f'/assignments/{assignment_id}/')
        # except ObjectDoesNotExist: #was: if existing_sen.length == 0:if existing_sen.length == 0:

        #create new edit
        new_edit = Edit.objects.create(content=content, hid=False, top='Z', sentence=existing_sen)
        #print(f"--- {new_edit.edit_text}"
        if new_edit:
          print(f"new_edit: {new_edit.content}")
        else:
          messages.error(request, f"ERROR: Could not create edit with content: {content}, sentence: #{existing_sen.id}.")
          return redirect(f'/assignments/{assignment_id}/')

        #create contribution
        new_contribution = Contribution.objects.create(kind=kind, effort_in_seconds=0, edit=new_edit, assignment=assignment)
        #print(f"--- #{new_contribution.contribution_text}")
        if new_contribution:
          print(f"new_contribution: {new_contribution.edit.content}")
        else:
          messages.error(request, f"ERROR: Could not create contribution with kind: {kind}, edit: {new_edit.id}.")
          return redirect(f'/assignments/{assignment_id}/')

        new_edit = None
        new_contribution = None
        num_of_contributions += 1

    #mark as imported
    Assignment.objects.filter(id=assignment_id).update(ci=True) #was: @assignment.update(ci: true)

    messages.error(request, f"{num_of_contributions} '{kind}' contributions for this assignment imported")
    return redirect(f'/assignments/{assignment_id}/')
  else:
    return render(request, 'todproof/upload.html')
  
###############################################################################
# User
###############################################################################
from django.contrib.auth import get_user_model
from crum import get_current_user

def index_users(request):
  User = get_user_model()
  users = User.objects.all()
  return render(request, 'todproof/index_users.html', {'users': users})

def switch_current_assignment(request, assignment_id):
  assignment = Assignment.objects.get(pk=assignment_id)
  current_user = get_current_user(); #print(type(current_user))
  User = get_user_model()  
  User.objects.all().filter(id=current_user.id).update(cur_assign=assignment.id)
#   if @user.save
#     flash[:success] = "Assignment was successfully switched"
#     if Assignment.admin_roles.include? @user.cur_assign.role
#       redirect_to assignment_path(assignment)
#     else
#       translation = @user.cur_assign.translation
#       sentence = translation.sentences.where(rsen: @user.cur_assign.place).first
#       redirect_to translation_sentence_path(translation, sentence)
#     end
#   else
#     flash[:danger] = "Assignment was NOT switched"
#     redirect_to :back
#   end
# end
  # return render(request, 'todproof/show_translation_sentence.html', {'translation': task.translation, 'sentence': 1})
  # return render(request, 'todproof/show_translation_sentence.html', {'translation': get_current_user().cur_assign.translation, 'sentence': 1})
  # render(request, 'todproof/show_task.html', {'task': task})
  # return render(request, 'todproof/show_task.html', {'task': task})
  # return render(request, 'todproof/show_task.html', {'task': get_current_user().cur_task})
  # return redirect(f'switch_current_assignment/assignments/{assignment_id}')
  # return redirect('index-assignments') WORKS!!!!
  #- return redirect('switch-current-assignment')
  return redirect(f'/assignments/{assignment.id}/') #WORKS!!!
  #- return redirect(f'translations/{get_current_user().cur_assign.translation.id}/sentences/1/')