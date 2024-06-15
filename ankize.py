import json
import os
import requests
import html
import genanki
import shutil

def generate_anki(section_name, section_id):
  MODEL_YES_NO_ID = 1789531432
  MODEL_ABCD_ID = 1789531433
  DECK_ID = 14101918  # need to append two numbers
  BUILD = 'tmp'
  ITEMS = os.path.join(BUILD, '{}.json'.format(section_id))
  DEST = 'dest'
  ANKI_DECK = os.path.join(DEST, 'prawko{}.apkg'.format(section_id))

  def get_deck_id(section_id):
    deck_base = DECK_ID*100
    return deck_base + section_id

  my_deck = genanki.Deck(
    get_deck_id(section_id),
    'Prawo jazdy::{}'.format(section_name))

  yesNo_model = genanki.Model(
    MODEL_YES_NO_ID,
    'Tak/Nie',
    fields=[
      {'name': 'Media'},
      {'name': 'Question'},
      {'name': 'Answer'},
      {'name': 'Comment'},
    ],
    templates=[
      {
        'name': 'Tak/Nie',
        'qfmt': '{{Media}}<br>{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br><br>{{Comment}}',
      },
    ])

  abcd_model = genanki.Model(
    MODEL_ABCD_ID,
    'Pole jednokrotnego wyboru',
    fields=[
      {'name': 'Image'},
      {'name': 'Question'},
      {'name': 'Q_1'},
      {'name': 'Q_2'},
      {'name': 'Q_3'},
      {'name': 'Q_4'},
      {'name': 'CorrectAnswer'},
      {'name': 'Comment'},
    ],
    templates=[
      {
        'name': 'Pole jednokrotnego wyboru',
        'qfmt': '{{Image}}<br>{{Question}}<hr>{{Q_1}}<br><br>{{Q_2}}<br><br>{{Q_3}}<br><br>{{Q_4}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{CorrectAnswer}}<br><br>{{Comment}}',
      },
    ])

  my_package = genanki.Package(my_deck)
  my_package.media_files = []

  with open(ITEMS) as f:
      d = json.load(f)
      for elem in d:
          image = ''
          if elem['Image'] != '':
            externalSource = elem['Image'][-9:] + '.jpg'
            image = '<img src="{}">'.format(externalSource)
          if elem['Video'] != '':
            externalSource = elem['Video'][-9:] + '.webm'
            image = '<video controls><source src="{}" type="video/webm"></video>'.format(externalSource)

          if len(elem['Answers']) > 2:
            if len(elem['Answers']) < 4:
              elem['Answers'].append('')
            my_note = genanki.Note(
                model=abcd_model,
                fields=[
                  image,
                  elem['Question'],
                  *elem['Answers'],
                  elem['CorrectAnswer'],
                  elem['Comment'],
                ]
            )
          else:
            my_note = genanki.Note(
                model=yesNo_model,
                fields=[
                  image,
                  elem['Question'],
                  elem['CorrectAnswer'],
                  elem['Comment'],
                ]
            )

          if elem['Image'] != '':
            my_package.media_files.append(os.path.join(BUILD, str(section_id), elem['Image'][-9:]+'.jpg'))
          #if elem['Video'] != '':
            # Doesn't work
            #my_package.media_files.append(os.path.join(BUILD, '11', elem['Video'][-9:]+'.webm'))

          my_deck.add_note(my_note)

  try:
      os.mkdir(DEST)
  except OSError:
      pass
    
  my_package.write_to_file(ANKI_DECK)