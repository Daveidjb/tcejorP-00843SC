from django.core.management.base import BaseCommand
from club.models import Author, Genre, Book, Member, Reading
from datetime import date

class Command(BaseCommand):
    help = 'Load sample data'

    def handle(self, *args, **kwargs):
        if Reading.objects.exists():
            self.stdout.write('Data already loaded, skipping.')
            return

    # Clear any partial data from previous failed attempts
        Genre.objects.all().delete()
        Author.objects.all().delete()
        Book.objects.all().delete()
        Member.objects.all().delete()


        romance           = Genre.objects.create(name="Romance")
        scifi             = Genre.objects.create(name="Science Fiction")
        fantasy           = Genre.objects.create(name="Fantasy")
        fiction           = Genre.objects.create(name="Fiction")
        realistic_fiction = Genre.objects.create(name="Realistic Fiction")
        nonfiction        = Genre.objects.create(name="Non-Fiction")
        biography         = Genre.objects.create(name="Biography")

        orwell   = Author.objects.create(first_name="George", last_name="Orwell")
        christie = Author.objects.create(first_name="Agatha", last_name="Christie")
        le_guin  = Author.objects.create(first_name="Ursula", last_name="Le Guin")
        yuval    = Author.objects.create(first_name="Yuval",  last_name="Harari")

        b1 = Book.objects.create(title="1984",                         author=orwell,   genre=fiction,    published_year=1949, total_pages=328)
        b2 = Book.objects.create(title="Animal Farm",                  author=orwell,   genre=fiction,    published_year=1945, total_pages=112)
        b3 = Book.objects.create(title="Murder on the Orient Express", author=christie, genre=fiction,    published_year=1934, total_pages=256)
        b4 = Book.objects.create(title="The Left Hand of Darkness",    author=le_guin,  genre=scifi,      published_year=1969, total_pages=304)
        b5 = Book.objects.create(title="Sapiens",                      author=yuval,    genre=nonfiction, published_year=2011, total_pages=443)

        alice = Member.objects.create(first_name="Alice", last_name="Smith",   email="alice@example.com")
        bob   = Member.objects.create(first_name="Bob",   last_name="Johnson", email="bob@example.com")
        carol = Member.objects.create(first_name="Carol", last_name="Lee",     email="carol@example.com")

        Reading.objects.create(book=b1, member=alice, start_date=date(2024,1,5),  end_date=date(2024,1,20), status="completed", rating=5)
        Reading.objects.create(book=b3, member=alice, start_date=date(2024,2,1),  end_date=date(2024,2,10), status="completed", rating=4)
        Reading.objects.create(book=b5, member=bob,   start_date=date(2024,1,10), end_date=date(2024,2,15), status="completed", rating=4)
        Reading.objects.create(book=b2, member=bob,   start_date=date(2024,3,1),  end_date=None,            status="reading",   rating=None)
        Reading.objects.create(book=b4, member=carol, start_date=date(2024,2,20), end_date=date(2024,3,10), status="completed", rating=3)
        Reading.objects.create(book=b1, member=carol, start_date=date(2024,3,15), end_date=None,            status="dropped",   rating=2)

        self.stdout.write('Sample data loaded successfully!')