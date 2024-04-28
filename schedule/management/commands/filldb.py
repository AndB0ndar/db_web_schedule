from django.core.management.base import BaseCommand
import datetime
import requests

from schedule.models import RichGroup, DaySchedule, Lesson, Stats, TinyGroup


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

        groups: list[dict] = requests.get(f"{self.url}{self.groups}").json()
        for group in groups:
            group_name = group['groupName']
            group_suffix = group['groupSuffix']

            t_group, _ = TinyGroup.objects.get_or_create( groupName=group_name, groupSuffix=group_suffix)
            data = requests.get(
                f"{self.url}{self.certain}"
                , params={'name': group_name, 'suffix': group_suffix}
            ).json()

            for group_data in data:
                r_group, created = RichGroup.objects.update_or_create(
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
                    for f_even, lesson_data_list in enumerate(day_schedule_data['odd'], day_schedule_data['even']):
                        for lesson_data in lesson_data_list:
                            lesson = Lesson.objects.create(
                                day_schedule=day_schedule,
                                is_even_week=f_even,
                                name=lesson_data["name"],
                                type=lesson_data["type"],
                                tutor=lesson_data.get("tutor"),
                                place=lesson_data.get("place"),
                                link=lesson_data.get("link")
                            )
                            lesson.save()
