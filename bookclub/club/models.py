from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    published_year = models.IntegerField(null=True, blank=True)
    total_pages = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Reading(models.Model):
    STATUS_CHOICES = [
        ('reading',   'Currently Reading'),
        ('completed', 'Completed'),
        ('dropped',   'Dropped'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='readings')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='readings')
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reading',db_index=True)
    rating = models.IntegerField(null=True, blank=True)  # 1–5

    def __str__(self):
        return f"{self.member} – {self.book} ({self.status})"

    def days_to_finish(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None