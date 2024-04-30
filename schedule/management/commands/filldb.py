from django.core.management.base import BaseCommand
import requests
import json

from schedule.models import RichGroup, DaySchedule, Lesson, Stats, TinyGroup, Week


class Command(BaseCommand):
    url = "https://mirea.xyz/api/v1.3/"
    groups = "groups/all"
    certain = "groups/certain"
    status = "stats"

    help = 'Load data from API into Django models'

    def handle(self, *args, **options):
        stats = requests.get(f"{self.url}{self.status}").json()
        stats = Stats.objects.create(
            groupsCount=stats['groupsCount'],
            scrapperUpdatedDate=stats['scrapperUpdatedDate']
        )
        stats.save()

        # groups: list[dict] = requests.get(f"{self.url}{self.groups}").json()  # load all groups
        with open("res/data/data.json") as f:
            groups = json.load(f)

        for group in groups:
            group_name = group['groupName']
            group_suffix = group['groupSuffix']

            t_group, _ = TinyGroup.objects.get_or_create( groupName=group_name, groupSuffix=group_suffix)
            data = requests.get(
                f"{self.url}{self.certain}"
                , params={'name': group_name, 'suffix': group_suffix}
            ).json()

            for group_data in data:
                r_group, _ = RichGroup.objects.update_or_create(
                    group=t_group,
                    defaults={
                        "remoteFile": group_data["remoteFile"],
                        "unitName": group_data["unitName"],
                        "unitCourse": group_data["unitCourse"],
                        "updatedDate": group_data["updatedDate"]
                    }
                )
                for day_schedule_data in group_data["schedule"]:
                    day_schedule, _ = DaySchedule.objects.get_or_create(
                        group=r_group,
                        day=day_schedule_data["day"]
                    )
                    for f_even, lessons in enumerate([day_schedule_data['odd'], day_schedule_data['even']]):
                        for dict_lesson in lessons:
                            for lesson in dict_lesson:
                                lsn = Lesson.objects.create(
                                    day_schedule=day_schedule,
                                    is_even_week=f_even,
                                    name=lesson["name"],
                                    type=lesson["type"],
                                    tutor=lesson.get("tutor"),
                                    place=lesson.get("place"),
                                    link=lesson.get("link")
                                )
                                lsn.save()
                                """
                                if lesson['weeks'] is not None:
                                    for number in lesson['weeks']:
                                        week, _ = Week.objects.create(
                                            lesson=lsn,
                                            number=number
                                        )
                                        week.save()
                                """
