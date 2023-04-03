from otree.api import *

import pandas as pd
import openpyxl


c = cu

doc = 'Focal point'


class C(BaseConstants):
    NAME_IN_URL = 'focal_task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 50
    NUM_ROUNDS_PRE = 17
    ROUND_NUMBER_SWITCH = 21
    NUM_ROUNDS_PROB = 50
    PRICE_MIN = cu(0)
    PRICE_MAX = cu(49)
    COLORS = ['A', 'B']
    NUM_CUSTOMERS = 200
    INSTRUCTIONS_TEMPLATE = 'focal/instructions.html'
    SECOND_INSTRUCTIONS_TEMPLATE = 'focal/second_instructions.html'
    ECU_LABEL = 'ECUs'
    EXCHANGE_RATE_TWO_FIRMS = 0.00006667


class Subsession(BaseSubsession):
    winning_price = models.IntegerField()


def creating_session(subsession: Subsession):
    session = subsession.session
    if subsession.round_number == 1:
        from random import shuffle

        session = subsession.session
        players_per_group = session.config['players_per_group']
        num_firms = session.config['num_firms']
        num_participants = session.num_participants
        if num_participants != num_firms * players_per_group:
            raise ValueError(f'Number of participants in the session must be {num_firms} * {players_per_group}')

        players = subsession.get_players()
        shuffle(players)
        for p in players:
            p.participant.moved = False

        group_matrix = [players[n: n + players_per_group] for n in range(0, len(players), players_per_group)]

        for n, s in enumerate(subsession.in_rounds(1, C.ROUND_NUMBER_SWITCH - 1)):
            # set group matrix for all rounds up to the switch round (excluded)
            s.set_group_matrix(group_matrix)
            if n == 0:
                for i, g in enumerate(s.get_groups()):
                    color = C.COLORS[i]
                    g.color = color
                    for p in g.get_players():
                        p.participant.uuid = f'{color} {p.id_in_group}'
            else:
                for i, g in enumerate(s.get_groups()):
                    g.color = C.COLORS[i]

        # From each original group extract a randomly selected employee using pop() with a random index
        from random import randint
        employees_to_switch = [g.pop(randint(0, players_per_group - 1)) for g in group_matrix]
        for e in employees_to_switch:
            e.participant.moved = True
            e.moved = True
            e.group.moved_player_id = e.id_in_group

        # Change the list order of the employees to re-assign
        employees_to_switch.append(employees_to_switch.pop(0))

        for n, p in enumerate(employees_to_switch):
            # Reassign each employee to the new group
            group_matrix[n].append(p)

        for s in subsession.in_rounds(C.ROUND_NUMBER_SWITCH, C.NUM_ROUNDS):
            # Set group matrix for all rounds from the switch round (included)
            s.set_group_matrix(group_matrix)

            for i, g in enumerate(s.get_groups()):
                g.color = C.COLORS[i]


def set_payoffs(subsession: Subsession):
    session = subsession.session
    groups = subsession.get_groups()
    for g in groups:
        set_price(g)

    winning_price = min([g.price for g in groups])
    subsession.winning_price = winning_price

    num_winners = len([g for g in groups if g.price == winning_price])

    for g in groups:
        g.win = g.price == winning_price
    for g in groups:
        if winning_price==g.price:
            c=g.color


class Group(BaseGroup):
    color = models.StringField(choices=C.COLORS)
    agreed = models.BooleanField()
    price = models.IntegerField()
    win = models.BooleanField()
    moved_player_id = models.IntegerField()


def set_agreed(group: Group):
    players_per_group = group.session.config['players_per_group']
    group.agreed = sum(
        p.price == group.get_player_by_id(1).price for p in group.get_players()) >= players_per_group - 1


def get_employee_to_move(group: Group):
    return [p for p in group.get_players() if p.participant.moved][0]


def set_price(group: Group):
    import random
    players_per_group = group.session.config['players_per_group']
    players = group.get_players()
    prices = [p.price for p in players if p.field_maybe_none('price') is not None]
    price = None
    for p in prices:
        n = prices.count(p)
        if n >= players_per_group:
            group.agreed = True
            price = p
            group.price = p
            break

    if not price:
        group.price = random.choice(prices) if prices else random.randint(C.PRICE_MIN, C.PRICE_MAX)
        group.agreed = False


class Player(BasePlayer):
    suggestion = models.IntegerField(
        label='Please suggest to your teammates, the price at which you want to sell your goods', max=C.PRICE_MAX,
        min=C.PRICE_MIN)
    price = models.IntegerField(label='What is the price you want to set for your firm?', max=C.PRICE_MAX,
                                min=C.PRICE_MIN)
    price_timeout = models.BooleanField(initial=False)
    is_winner = models.BooleanField()
    moved = models.BooleanField()
    num_failed_attempts = models.IntegerField(initial=0)
    failed_too_many = models.BooleanField(initial=False)

    teamquiz1 = models.StringField(
        label='Which is the largest state in the U.S. (by area)?'
    )
    teamquiz1_wrong = models.IntegerField(initial=0)

    teamquiz2 = models.StringField(
        label='What is the third sign of the zodiac?'
    )
    teamquiz2_wrong = models.IntegerField(initial=0)

    teamquiz3 = models.StringField(
        label='Which natural disaster is measured with a Richter scale?'
    )
    teamquiz3_wrong = models.IntegerField(initial=0)

    teamquiz4 = models.IntegerField(
        label='How many Amendments does the US constitution have?'
    )
    teamquiz4_wrong = models.IntegerField(initial=0)

    teamquiz5 = models.StringField(
        label='Which planet is known as the red planet?'
    )
    teamquiz5_wrong = models.IntegerField(initial=0)

    teamquiz6 = models.IntegerField(
        label='Please enter your label (the number assigned to you).'
    )
    teamquiz6_wrong = models.IntegerField(initial=0)


def set_results(subsession: Subsession):
    set_payoffs(subsession)


# PAGES
class Introduction(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Waitforteam(WaitPage):
    wait_for_all_groups = True
    pass


class Teamchat(Page):
    form_model = 'player'
    form_fields = ['teamquiz6', 'teamquiz1', 'teamquiz2', 'teamquiz3', 'teamquiz4', 'teamquiz5']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def get_timeout_seconds(player: Player):
        if player.round_number == 1:
            timeout_seconds = 300
        else:
            timeout_seconds = 301
        return timeout_seconds

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        group = player.group
        return dict(
            suggestions=[(p.participant.uuid, p.suggestion) for p in group.get_players() if
                         p.field_maybe_none('suggestion')],
            player_uuid=get_employee_to_move(group).participant.uuid,
            nickname=f'Player {participant.uuid}'
        )

    @staticmethod
    def error_message(player: Player, values):
        # alternatively, you could make quiz1_error_message, quiz2_error_message, etc.
        # but if you have many similar fields, this is more efficient.
        solutions = dict(
            teamquiz1=('ALASKA', 'ALASKA'),
            teamquiz2=('GEMINI', 'GEMINI'),
            teamquiz3=('EARTHQUAKE', 'EARTHQUAKE'),
            teamquiz4=('27', '27'),
            teamquiz5=('MARS', 'MARS'),
            teamquiz6=('40', '40'),
        )

        # error_message can return a dict whose keys are field names and whose
        # values are error messages
        errors = {
            k: solutions[k][1] for k, v in values.items() if v != solutions[k][0]
        }

        for k in errors.keys():
            num = getattr(player, f'{k}_wrong')
            setattr(player, f'{k}_wrong', num + 1)

        # print('errors is', errors)
        if errors:
            player.num_failed_attempts += 1
            if player.num_failed_attempts >= 1:
                player.failed_too_many = True
                # we don't return any error here; just let the user proceed to the
                # next page, but the next page is the 'suggest" page where the game starts
            else:
                return errors


class WaitSuggestions(WaitPage):
    pass


class Chat(Page):
    form_model = 'player'
    form_fields = ['price']

    @staticmethod
    def get_timeout_seconds(player: Player):
        if player.round_number in [1, 2, 21, 22]:
            timeout_seconds = 180
        else:
            timeout_seconds = 60
        return timeout_seconds

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        group = player.group
        return dict(
            suggestions=[(p.participant.uuid, p.suggestion) for p in group.get_players() if
                         p.field_maybe_none('suggestion')],
            player_uuid=get_employee_to_move(group).participant.uuid,
            nickname=f'Player {participant.uuid}'
        )


class Decide(Page):
    form_model = 'player'
    form_fields = ['price']

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        group = player.group
        return dict(
            suggestions=[(p.participant.uuid, p.suggestion) for p in group.get_players() if
                         p.field_maybe_none('suggestion')],
            player_uuid=get_employee_to_move(group).participant.uuid,
            nickname=f'Player {participant.uuid}'
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            from random import randint
            player.price = randint(C.PRICE_MIN, C.PRICE_MAX)
            player.price_timeout = True


class WaitingResults(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_results


class Results(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(
            payoff=int(player.payoff),
            cumulative_payoff=int(player.participant.payoff),
            employee_to_move=get_employee_to_move(player.group),
            other_firms=[(g.color, g.price) for g in player.subsession.get_groups() if g != group],
        )


class SubjectMovingGroupWarning(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(
            player_uuid=get_employee_to_move(group).participant.uuid,
        )

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 17


class EndTask(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        xrate = C.EXCHANGE_RATE_TWO_FIRMS if player.session.config['num_firms'] == 2 else C.EXCHANGE_RATE_FOUR_FIRMS
        return dict(
            total_earnings=cu(participant.payoff * xrate + 7)
        )


page_sequence = [
    SubjectMovingGroupWarning, Waitforteam, Teamchat, WaitSuggestions, Chat, Decide, WaitingResults, Results, EndTask
]
