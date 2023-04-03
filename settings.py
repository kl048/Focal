from os import environ

SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=7)
SESSION_CONFIGS = [
    dict(
        name='focal_point_teams',
        display_name='Focal point - Firms 2 / Employees 2',
        num_demo_participants=4,
        app_sequence=['focal_task', 'focal_crt', 'focal_survey'],
        use_browser_bots=False,
        show_instructions=False,
        num_firms=2,
        players_per_group=2,
    ),
]


LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

DEMO_PAGE_INTRO_HTML = ''

PARTICIPANT_FIELDS = ['uuid', 'moved', 'player_moving','end_payoff_two','end_payoff_four']
SESSION_FIELDS = ['show_round = True']

ROOMS = [
    dict(
        name='firms_2A_employees_2A',
        display_name='Firms 2A - Employees 2A',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='firms_2B_employees_2B',
        display_name='Firms 2B - Employees 2B',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='firms_2C_employees_2C',
        display_name='Firms 2C - Employees 2C',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='firms_2D_employees_2D',
        display_name='Firms 2D - Employees 2D',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='firms_2E_employees_2E',
        display_name='Firms 2E - Employees 2E',
        participant_label_file='_rooms/workstation.txt',
    ),
    
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']