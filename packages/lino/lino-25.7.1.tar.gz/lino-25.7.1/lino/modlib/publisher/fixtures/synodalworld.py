from lino.api import rt, _

home_children = [
    (_("Mission"), None, []),
    (_("Maxim"), None, []),
    (_("Propaganda"), None, []),
    (_("About us"), None, [
        (_("Team"), None, []),
        (_("History"), None, []),
        (_("Contact"), None, []),
        (_("Terms & conditions"), None, []),
    ]),
]


def objects():
    image = rt.models.uploads.Upload.objects.first()
    def iterate(iterable):
        try:
            for obj in iterable:
                yield iterate(obj)
        except TypeError:
            if (obj := iterable).title == 'Mission':
                obj.main_image = image
            yield obj
    for obj in rt.models.publisher.make_demo_pages(home_children):
        yield iterate(obj)

