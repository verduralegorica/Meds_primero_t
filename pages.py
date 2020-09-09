
from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Player, Group


class Instrucciones(Page):

    form_model = 'player'

    def vars_for_template(self):
        return dict(participant_id=self.participant.label)


    def is_displayed(self):
        if self.participant.vars['MobilePhones'] is False:
            return True
        else:
            return False

class Entendimiento(Page):

    form_model = 'player'

    def get_form_fields(self):
        return [self.player.current_field()]

    def error_message(self, values):
        player = self.player

        current_field = player.current_field()
        correct_answer = Constants.quiz_fields[current_field]

        if values[current_field] != correct_answer:  # if answer is incorrect in current field
            # counting incorrect attempts
            player.q_incorrect_attempts += 1
            # telling the player the correct answer
            self.player.quiz_incorrect_answer = 'Alternativa incorrecta. La respuesta correcta es "' \
                                                + str(Constants.quiz_answers[player.quiz_page_counter]) + '"'
            return self.player.quiz_incorrect_answer

    def vars_for_template(self):
        player = self.player
        preguntas_quiz = Constants.preguntas_quiz
        quiz_earnings = self.player.quiz_earnings

        index = player.quiz_page_counter
        return {'participant_id': self.participant.label,
                'question': preguntas_quiz[index],
                'page_number': index + 1,
                'incorrect_answer': player.quiz_incorrect_answer,
                'quiz_earnings': quiz_earnings,
                'dollar_amount': self.player.quiz_earnings.to_real_world_currency(self.session)
                }



    def before_next_page(self):
        player = self.player
        player.quiz_page_counter += 1

        if self.timeout_happened:
            player.q_timeout = 1
        if player.q_timeout == 1 and player.q_incorrect_attempts == 0:
            player.q_validation = 1
        if player.q_incorrect_attempts == 0 and self.timeout_happened is False:
            player.num_correct += 1
            player.quiz_earnings += Constants.payment_per_answer
            if player.quiz_page_counter == 1:
                self.participant.vars['ea1'] += 1
            if player.quiz_page_counter == 2:
                self.participant.vars['ea2'] += 1
            if player.quiz_page_counter == 3:
                self.participant.vars['ea3'] += 1
            if player.quiz_page_counter == 4:
                self.participant.vars['ea4'] += 1


        self.participant.vars['quiz_earnings'] += player.quiz_earnings
        player.error_sequence += str(player.q_incorrect_attempts)
        player.timeout_sequence += str(player.q_timeout)
        player.q_timeout = 0
        player.q_incorrect_attempts = 0




    def is_displayed(self):

        # Adds quiz earnings to player's payoff
        self.participant.vars['quiz_earnings'] = self.player.quiz_earnings.to_real_world_currency(self.session)
        self.participant.vars['quiz_questions_correct'] = self.player.num_correct
        self.player.payoff = self.player.quiz_earnings

        if self.participant.vars['MobilePhones'] is False:
            return True
        else:
            return False




    timeout_seconds = 300

class Cartilla(Page):

    def vars_for_template(self):
        return dict(participant_id=self.participant.label)
    form_model = 'player'

    def is_displayed(self):
        if self.participant.vars['MobilePhones'] is False:
            return True
        else:
            return False

# Orden en que se mostrarán las páginas
page_sequence = [Instrucciones,
                 Entendimiento,
                 Entendimiento,
                 Entendimiento,
                 Entendimiento,
                 Cartilla,
                 ]