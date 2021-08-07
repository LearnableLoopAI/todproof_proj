from todproof.models import Sentence
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),

    # Message
    path('messages/new', views.create_message, name='create-message'),
    path('messages/', views.index_messages, name='index-messages'),
    path('messages/<message_id>/', views.show_message, name='show-message'),
    path('messages/<message_id>/edit', views.update_message, name='update-message'),
    path('messages/<message_id>/delete', views.delete_message, name='delete-message'),
    path('messages/search', views.search_messages, name='search-messages'),

    # Translation
    path('all_translations', views.index_all_translations, name='index-all-translations'),
    # path('messages/<message_id>/translations/', views.show_message_translations, name='show-message-translations'),

    path('messages/<message_id>/translations/', views.index_message_translations, name='index-message-translations'),
    path('messages/<message_id>/translations/<translation_id>/', views.show_translation, name='show-translation'),
    path('messages/<message_id>/translations/new', views.create_translation, name='create-translation'),
    path('messages/<message_id>/translations/<translation_id>/edit', views.update_translation, name='update-translation'),
    path('messages/<message_id>/translations/<translation_id>/delete', views.delete_translation, name='delete-translation'),

    path('lookup_link/messages/<message_id>/translations/<translation_id>', views.import_lookup, name='import-lookup'),
    path('lookup_delete_link/messages/<message_id>/translations/<translation_id>', views.delete_lookup, name='delete-lookup'),

    # Sentence
    # path('translations/<translation_id>/sentences/', views.index_translation_sentences, name='index-translation-sentences'),
    path('translations/<translation_id>/sentences/<sentence_id>/', views.show_sentence, name='show-sentence'),
    path('translations/<translation_id>/sentences/new', views.create_sentence, name='create-sentence'),
    path('translations/<translation_id>/sentences/<sentence_id>/edit', views.update_sentence, name='update-sentence'),
    path('translations/<translation_id>/sentences/<sentence_id>/delete', views.delete_sentence, name='delete-sentence'),

    # # Change #add AFTER import_content
    # # path('sentences/<sentence_id>/changes/', views.index_sentence_changes, name='index-sentence-changes'),
    # path('sentences/<sentence_id>/changes/<change_id>/', views.show_sentence_change, name='show-sentence-change'),
    # path('sentences/<sentence_id>/changes/new', views.create_sentence_change, name='create-sentence-change'),
    # path('sentences/<sentence_id>/changes/<change_id>/edit', views.update_sentence_change, name='update-sentence-change'),
    # path('sentences/<sentence_id>/changes/<change_id>/delete', views.delete_sentence_change, name='delete-sentence-change'),

    # Assignment
    path('assignments/', views.index_assignments, name='index-assignments'),
    path('assignments/<assignment_id>/', views.show_assignment, name='show-assignment'),
    path('assignments/new', views.create_assignment, name='create-assignment'),
    path('assignments/<assignment_id>/edit', views.update_assignment, name='update-assignment'),
    path('delete_assignment/<assignment_id>', views.delete_assignment, name='delete-assignment'),

    path('import_content_for_validation/assignments/<assignment_id>/', views.import_content_for_validation, name='import-content-for-validation'),
    path('import_content/assignments/<assignment_id>/', views.import_content, name='import-content'),

    # User
    path('users/', views.index_users, name='index-users'),
    # path('switch_current_assignment/translations/<translation_id>/sentences/<sentence_id>/', views.switch_current_assignment, name='switch-current-assignment'),
    path('switch_current_assignment/assignments/<assignment_id>/', views.switch_current_assignment, name='switch-current-assignment'),


]