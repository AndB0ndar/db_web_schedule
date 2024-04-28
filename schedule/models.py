from djongo import models


class TinyGroup(models.Model):
    groupName = models.CharField(max_length=15)
    groupSuffix = models.CharField(max_length=100)

    def __str__(self):
        return self.groupName


class RichGroup(models.Model):
    group = models.OneToOneField(TinyGroup, on_delete=models.CASCADE)
    remoteFile = models.CharField(max_length=100)
    unitName = models.CharField(max_length=100)
    unitCourse = models.CharField(max_length=100)
    updatedDate = models.DateTimeField()

    def __str__(self):
        return f"{self.group.name} {self.updatedDate}"


class Time(models.Model):
    group = models.ForeignKey(RichGroup, on_delete=models.DO_NOTHING)
    time = models.CharField(max_length=100)


class DaySchedule(models.Model):
    group = models.ForeignKey(RichGroup, on_delete=models.CASCADE)
    day = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.group.name} {self.day}"


class Lesson(models.Model):
    day_schedule = models.ForeignKey(DaySchedule, on_delete=models.CASCADE)
    is_even_week = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    tutor = models.CharField(max_length=100, blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.type}"


class Week(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.DO_NOTHING)
    number = models.IntegerField()


class Stats(models.Model):
    groupsCount = models.IntegerField()
    scrapperUpdatedDate = models.DateTimeField()

    def __str__(self):
        return f"Stats: Groups Count - {self.groupsCount}, Updated Date - {self.scrapperUpdatedDate}"
