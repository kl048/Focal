import random
import sys

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

    FIRM_A_YES_ABOVE_21 = {
        22: (37, 29, [21, 21]),
        23: (40, 31, [0, 22]),
        24: (44, 33, [0, 23]),
        25: (48, 35, [0, 24]),
        26: (52, 37, [0, 25]),
        27: (56, 39, [0, 26]),
        28: (0, 41, [0, 27])
    }
    FIRM_A_YES_BELOW_21 = {
        21: 34,
        20: 31,
        19: 28,
        18: 25,
        17: 22,
        16: 19,
        15: 16,
        14: 13,
        13: 12,
        12: 11,
        11: 10,
        10: 9,
        9: 8,
        8: 7,
        7: 6,
        6: 5,
        5: 4,
        4: 3,
        3: 2,
        2: 1,
        1: 0,
        0: 0
    }
    FIRM_A_NO_ABOVE_21 = {
        22: (37, 29, [21, 21]),
        23: (40, 31, [0, 22]),
        24: (44, 33, [0, 23]),
        25: (48, 35, [0, 24]),
        26: (52, 37, [0, 25]),
        27: (56, 39, [0, 26]),
        28: (60, 41, [0, 27]),
        29: (64, 43, [0, 28]),
        30: (45, 29, [0, 0]),
        31: (47, 30, [0, 0]),
        32: (49, 31, [0, 0]),
        33: (51, 32, [0, 0]),
        34: (53, 33, [0, 0]),
        35: (55, 34, [0, 0]),
        36: (57, 35, [0, 0]),
        37: (59, 36, [0, 0]),
        38: (61, 37, [0, 0]),
        39: (63, 38, [0, 0]),
        40: (65, 39, [0, 0]),
        41: (67, 40, [0, 0]),
        42: (69, 41, [0, 0]),
        43: (71, 42, [0, 0]),
        44: (73, 43, [0, 0]),
        45: (75, 44, [0, 0]),
        46: (77, 45, [0, 0]),
        47: (79, 46, [0, 0]),
        48: (81, 47, [0, 0]),
        49: (0, 0, [0, 0]),
    }
    FIRM_A_NO_BELOW_21 = {
        21: 34,
        20: 31,
        19: 28,
        18: 25,
        17: 22,
        16: 19,
        15: 16,
        14: 13,
        13: 12,
        12: 11,
        11: 10,
        10: 9,
        9: 8,
        8: 7,
        7: 6,
        6: 5,
        5: 4,
        4: 3,
        3: 2,
        2: 1,
        1: 0,
        0: 0
    }
    FIRM_B_YES_ABOVE_21 = {
        22: (35, 30, [15, 15]),
        23: (39, 32, [16, 16]),
        24: (43, 34, [0, 17]),
        25: (47, 36, [0, 18]),
        26: (51, 38, [0, 19]),
        27: (55, 40, [0, 20]),
        28: (0, 42, [0, 21])
    }
    FIRM_B_YES_BELOW_21 = {
        21: 32,
        20: 29,
        19: 26,
        18: 23,
        17: 20,
        16: 18,
        15: 16,
        14: 14,
        13: 12,
        12: 10,
        11: 8,
        10: 6,
        9: 4,
        8: 2,
        7: 0,
        6: 0,
        5: 0,
        4: 0,
        3: 0,
        2: 0,
        1: 0,
        0: 0
    }
    FIRM_B_NO_ABOVE_21 = {
        22: (35, 30, [15, 15]),
        23: (39, 32, [16, 16]),
        24: (43, 34, [0, 17]),
        25: (47, 36, [0, 18]),
        26: (51, 37, [0, 19]),
        27: (55, 40, [0, 20]),
        28: (59, 42, [0, 21]),
        29: (63, 44, [0, 22]),
        30: (46, 23, [0, 0]),
        31: (48, 24, [0, 0]),
        32: (50, 25, [0, 0]),
        33: (52, 26, [0, 0]),
        34: (54, 27, [0, 0]),
        35: (56, 28, [0, 0]),
        36: (58, 29, [0, 0]),
        37: (60, 30, [0, 0]),
        38: (62, 31, [0, 0]),
        39: (64, 32, [0, 0]),
        40: (66, 33, [0, 0]),
        41: (68, 34, [0, 0]),
        42: (70, 35, [0, 0]),
        43: (72, 36, [0, 0]),
        44: (74, 37, [0, 0]),
        45: (76, 38, [0, 0]),
        46: (78, 39, [0, 0]),
        47: (80, 40, [0, 0]),
        48: (82, 41, [0, 0]),
        49: (0, 0, [0, 0]),
    }
    FIRM_B_NO_BELOW_21 = {
        21: 32,
        20: 29,
        19: 26,
        18: 23,
        17: 20,
        16: 18,
        15: 16,
        14: 14,
        13: 12,
        12: 10,
        11: 8,
        10: 6,
        9: 4,
        8: 2,
        7: 0,
        6: 0,
        5: 0,
        4: 0,
        3: 0,
        2: 0,
        1: 0,
        0: 0
    }


class Subsession(BaseSubsession):
    winning_price = models.IntegerField()


def creating_session(subsession: Subsession):
    session = subsession.session

    # Assign treatment and phase in the different rounds
    session_treatment = session.config['session_treatment']
    for p in subsession.get_players():
        if session_treatment == "YES_NO":
            if 1 <= subsession.round_number <= 25:
                p.session_phase = "YES"
            else:
                p.session_phase = "NO"
        else:
            if 1 <= subsession.round_number <= 25:
                p.session_phase = "NO"
            else:
                p.session_phase = "YES"

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

    for g in groups:
        my_firm_price = g.price
        other_firms_prices = [group.price for group in subsession.get_groups() if group != g]
        other_firm_price = other_firms_prices[0]  # We only have two groups.
        for player in g.get_players():
            profit = calculate_possible_profit(player, my_firm_price, other_firm_price)
            player.payoff = cu(profit)

    winning_price = min([g.price for g in groups])
    subsession.winning_price = winning_price

    num_winners = len([g for g in groups if g.price == winning_price])

    for g in groups:
        g.win = g.price == winning_price
    for g in groups:
        if winning_price == g.price:
            c = g.color


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
        group.price = random.choice(prices) if prices else random.randint(C.PRICE_MIN,
                                                                          group.get_player_by_id(1).price_max())
        group.agreed = False


class Player(BasePlayer):
    session_treatment = models.StringField()
    session_phase = models.StringField()

    suggestion = models.IntegerField(
        label='Please suggest to your teammates, the price at which you want to sell your goods', max=C.PRICE_MAX,
        min=C.PRICE_MIN)
    price = models.IntegerField(label='What is the price you want to set for your firm?', min=C.PRICE_MIN)

    def price_max(player):
        max_price = C.PRICE_MAX
        if player.session_phase == "YES":
            max_price = 28
        return max_price

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


def get_profit_matrix(player: Player, firm, phase, is_over_21=False):
    """
    Gets the profit matrix depending of the firm, phase and player own price input.
    :param player: The player object
    :param firm: The firm the player belongs to
    :param phase: The session_phase assigned to the player.
    :param is_over_21: True if own player price value is more than 21
    :return:
    """
    if firm == "A" and phase == "YES" and is_over_21:
        return C.FIRM_A_YES_ABOVE_21
    elif firm == "A" and phase == "YES" and not is_over_21:
        return C.FIRM_A_YES_BELOW_21
    elif firm == "A" and phase == "NO" and is_over_21:
        return C.FIRM_A_NO_ABOVE_21
    elif firm == "A" and phase == "NO" and not is_over_21:
        return C.FIRM_A_NO_BELOW_21
    elif firm == "B" and phase == "YES" and is_over_21:
        return C.FIRM_B_YES_ABOVE_21
    elif firm == "B" and phase == "YES" and not is_over_21:
        return C.FIRM_B_YES_BELOW_21
    elif firm == "B" and phase == "NO" and is_over_21:
        return C.FIRM_B_NO_ABOVE_21
    elif firm == "B" and phase == "NO" and not is_over_21:
        return C.FIRM_B_NO_BELOW_21


def calculate_possible_profit(player: Player, my_price, other_price):
    """
    Calculates the possible profits given inputs from the player
    :param player: The player object
    :param my_price: The input of the player price
    :param other_price: The input of the other players price
    :return: THe possible profits.
    """
    firm = player.group.color
    session_phase = player.session_phase

    # Anything over 49 in the no phase, returns 0
    if session_phase == 'NO' and my_price >= 49:
        return 0

    profit = 0

    if my_price > 21:
        profit_matrix = get_profit_matrix(player, firm, session_phase, True)
        if my_price < other_price:
            profit = profit_matrix[my_price][0]
        elif my_price == other_price:
            profit = profit_matrix[my_price][1]
        elif my_price > other_price:
            if other_price <= 21:
                profit = profit_matrix[my_price][2][1]
            else:
                profit = profit_matrix[my_price][2][0]
    else:
        profit_matrix = get_profit_matrix(player, firm, session_phase)
        profit = profit_matrix[my_price]

    return profit


def calculate_possible_profit_other_firm(player: Player, other_price, my_price):
    """
    Calculates the possible profits given inputs from the player
    :param player: The player object
    :param my_price: The input of the player price
    :param other_price: The input of the other players price
    :return: THe possible profits.
    """

    group = player.group

    firm = [g.color for g in player.subsession.get_groups() if g != group][0]
    session_phase = player.session_phase

    # Anything over 49 in the no phase, returns 0
    if session_phase == 'NO' and other_price >= 49:
        return 0

    profit = 0

    if other_price > 21:
        profit_matrix = get_profit_matrix(player, firm, session_phase, True)
        if other_price < my_price:
            profit = profit_matrix[other_price][0]
        elif other_price == my_price:
            profit = profit_matrix[other_price][1]
        elif other_price > my_price:

            if my_price <= 21:
                profit = profit_matrix[other_price][2][1]
            else:
                profit = profit_matrix[other_price][2][0]
    else:
        profit_matrix = get_profit_matrix(player, firm, session_phase)
        profit = profit_matrix[other_price]

    return profit


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


class ChatDecide(Page):
    form_model = 'player'
    form_fields = ['price']

    @staticmethod
    def get_timeout_seconds(player: Player):
        if player.round_number in [1, 2, 26, 27]:
            timeout_seconds = 180
        else:
            timeout_seconds = 60
        return timeout_seconds

    @staticmethod
    def js_vars(player):
        sec_to_hide_btn = 0

        if player.round_number in [1, 2, 26, 27]:
            sec_to_hide_btn = 60
        else:
            sec_to_hide_btn = 30

        return dict(
            sec_to_hide_btn=sec_to_hide_btn
        )

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        group = player.group

        return dict(
            suggestions=[(p.participant.uuid, p.suggestion) for p in group.get_players() if
                         p.field_maybe_none('suggestion')],
            player_uuid=get_employee_to_move(group).participant.uuid,
            nickname=f'Player {participant.uuid}',
            group_color=group.color,
            phase=player.session_phase,
            other_group_color=[g.color for g in player.subsession.get_groups() if g != group][0],
        )

    def live_method(player: Player, data):
        """
        Receives player calculator inputs and calculates the expected profits
        :param data: A dictionary containing the following keys: my_price and other_price.
        This information is used as input to calculate the profits
        :return: the expected profit value.
        """
        my_price = data.get("my_price", None)
        other_price = data.get("other_price", None)

        # Validate input is not none
        if my_price is None or other_price is None:
            return ChatDecide.construct_response_msg(player, "error", "Invalid input")

        # Validate input is in the correct range
        minima = 0
        maxima = sys.maxsize
        if player.session_phase == 'YES':
            maxima = 28

        if not (minima <= my_price <= maxima) or not (minima <= other_price <= maxima):
            return ChatDecide.construct_response_msg(player, "error",
                                                     "Invalid input. Must be a number within the range: {}-{}".format(
                                                         minima, maxima))

        # Calculate possible profit
        possible_profit = calculate_possible_profit(player, my_price, other_price)
        possible_profit_other_firm = calculate_possible_profit_other_firm(player, other_price, my_price)

        # Send back response to Html
        return ChatDecide.construct_response_msg(player, "success", "", possible_profit, possible_profit_other_firm)

    @staticmethod
    def construct_response_msg(player: Player, type, message, value=None, value_other_firm=None):
        response = dict()
        response["type"] = type
        response["message"] = message
        response["value"] = value
        response["value_other_firm"] = value_other_firm

        return {player.id_in_group: response}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            from random import randint
            player.price = randint(C.PRICE_MIN, player.price_max())
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
    SubjectMovingGroupWarning,
    Waitforteam,
    Teamchat,
    WaitSuggestions,
    ChatDecide,
    WaitingResults,
    Results,
    EndTask
]
