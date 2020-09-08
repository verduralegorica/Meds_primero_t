
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

doc = ''


class Constants(BaseConstants):
    """
    Description:
        Inherits oTree Class BaseConstants. Defines constants for
        the experiment these will remain unchanged
    """

    players_per_group = None
    num_rounds = 1
    timer = 20
    payment_per_answer = c(0.2)


    instructions_template = 'meds_primero_t/InstruccionesB.html'
    instructions_button = "meds_primero_t/Instructions_Button.html"
    contact_template = "meds_primero_t/Contactenos.html"

    name_in_url = 'pxe_nto_med1'  # name in webbrowser


    # Respuestas del quiz de entendimiento
    quiz_fields = dict(
        question_1_response=2,
        question_2_response=3,
        question_3_response=1,
        question_4_response=3,
    )

    #Preguntas del quiz de entendimiento

    preguntas_quiz = ['¿En qué consiste el cuestionario que se brindará en la segunda parte de la sesión?',
                      '¿Cuántos casos hipotéticos se presentarán en la primera sección del “Cuestionario Principal”?',
                      '¿En qué consiste la segunda sección del “Cuestionario Principal”?',
                      '¿Cuántos enunciados se presentarán en la segunda parte del “Cuestionario Principal”?']

    # Displayed answers
    quiz_answers = ['Compra y uso de medicamentos', 'Cuatro casos hipotéticos',
                    'Indicar qué tan de acuerdo estás con enunciados presentados',
                    'Nueve enunciados']
    respuestas_quiz = ['Compra y uso de medicamentos', 'Cuatro casos hipotéticos',
                       'Indicar qué tan de acuerdo estás con enunciados presentados',
                       'Nueve enunciados']

    # Possible choices
    q1_choices = [[1, 'Frecuencia de uso de aparatos electrónicos'],
                  [2, 'Compra y uso de medicamentos'],
                  [3, 'Uso y preferencias de aplicativos móviles'],
                  [4, 'Compras de productos en línea']]
    q2_choices = [[1, 'Dos casos hipotéticos'],
                  [2, 'Tres casos hipotéticos'],
                  [3, 'Cuatro casos hipotéticos'],
                  [4, 'Cinco casos hipotéticos']]
    q3_choices = [[1, 'Indicar qué tan de acuerdo estás con enunciados presentados'],
                  [2, 'Elegir entre dos opciones específicas presentadas'],
                  [3, 'Responder detalladamente a las preguntas presentadas'],
                  [4, 'Llenar los espacios en blanco de enunciados presentados']]
    q4_choices = [[1, 'Siete enunciados'],
                  [2, 'Ocho enunciados'],
                  [3, 'Nueve enunciados'],
                  [4, 'Diez enunciados']]
    # To randomize the order in which the answers are presented
    random.SystemRandom().shuffle(q1_choices)
    random.SystemRandom().shuffle(q2_choices)
    random.SystemRandom().shuffle(q3_choices)
    random.SystemRandom().shuffle(q4_choices)



class Subsession(BaseSubsession):

    def creating_session(self):

        for p in self.get_players():
            p.participant.vars['final_payoff'] = 0
            p.participant.vars['quiz_payoff'] = 0
            p.participant.vars['quiz_earnings'] = 0

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    # Para el pay-off del sistema
    def set_payoffs(self):
        p.payoff = self.player.quiz_earnings


    def current_field(self):
        return 'question_{}_response'.format(self.quiz_page_counter + 1)

    quiz_incorrect_answer = models.StringField(initial=None)
    quiz_respuesta_incorrecta = models.StringField(initial=None)

    # IP field
    player_ip = models.StringField()
    current_practice_page = models.IntegerField(initial=0)

    '''Quiz'''

    # Contar las preguntas correctas acertadas a la primera
    num_correct = models.IntegerField(initial=0)
    quiz_page_counter = models.IntegerField(initial=0)

    # Inc Attemp per question
    q_incorrect_attempts = models.IntegerField(initial=0)
    q_timeout = models.IntegerField(initial=0)
    q_validation = models.IntegerField(initial=0)
    q_attempts = models.IntegerField(initial=0)
    error_sequence = models.CharField(initial='')
    timeout_sequence = models.CharField(initial='')

    question_1_response = models.IntegerField(verbose_name='', widget=widgets.RadioSelect,
                                              choices=Constants.q1_choices)
    question_2_response = models.IntegerField(verbose_name='', widget=widgets.RadioSelect,
                                              choices=Constants.q2_choices)
    question_3_response = models.IntegerField(verbose_name='', widget=widgets.RadioSelect,
                                              choices=Constants.q3_choices)
    question_4_response = models.IntegerField(verbose_name='', widget=widgets.RadioSelect,
                                              choices=Constants.q4_choices)
    quiz_earnings = models.CurrencyField(initial=0)

    # Hidden Field for detecting bots
    quiz_dec_2 = models.LongStringField(blank=True)
