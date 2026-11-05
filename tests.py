import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_create_choice_with_empty_text():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('')

def test_create_choice_with_text_longer_than_100_characters():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('a' * 101)

def test_add_choices_assigns_sequential_ids():
    question = Question(title='q1')

    first_choice = question.add_choice('a')
    second_choice = question.add_choice('b')

    assert first_choice.id == 1
    assert second_choice.id == 2

def test_add_choice_can_mark_it_as_correct():
    question = Question(title='q1')

    choice = question.add_choice('a', is_correct=True)

    assert choice.is_correct

def test_remove_choice_by_id_removes_only_the_selected_choice():
    question = Question(title='q1')
    first_choice = question.add_choice('a')
    second_choice = question.add_choice('b')

    question.remove_choice_by_id(first_choice.id)

    assert question.choices == [second_choice]

def test_remove_all_choices_clears_the_question():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    question.remove_all_choices()

    assert question.choices == []

def test_set_correct_choices_marks_the_requested_choices():
    question = Question(title='q1')
    first_choice = question.add_choice('a')
    second_choice = question.add_choice('b')

    question.set_correct_choices([second_choice.id])

    assert not first_choice.is_correct
    assert second_choice.is_correct

def test_correct_selected_choices_returns_selected_correct_choices():
    question = Question(title='q1', max_selections=2)
    correct_choice = question.add_choice('a', is_correct=True)
    incorrect_choice = question.add_choice('b')

    selected_correct_choices = question.correct_selected_choices(
        [correct_choice.id, incorrect_choice.id]
    )

    assert selected_correct_choices == [correct_choice.id]

def test_correct_selected_choices_rejects_too_many_selections():
    question = Question(title='q1', max_selections=1)
    first_choice = question.add_choice('a')
    second_choice = question.add_choice('b')

    with pytest.raises(Exception):
        question.correct_selected_choices([first_choice.id, second_choice.id])