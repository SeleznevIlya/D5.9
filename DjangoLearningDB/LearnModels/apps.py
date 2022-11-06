from django.apps import AppConfig


class LearnmodelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LearnModels'

    def ready(self):
        import LearnModels.signals
        # from .tasks import send_message
        # from .schenduler import post_schenduler
        # print('started')
        #
        # post_schenduler.add_job(
        #     id='send mail',
        #     func=lambda : print('123'),
        #     trigger='interval',
        #     seconds=10,
        # )
        # post_schenduler.start()

