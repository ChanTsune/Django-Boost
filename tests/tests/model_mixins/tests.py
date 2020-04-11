from django.test import TestCase, override_settings


@override_settings(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)
class TestLogicalDeletionMixin(TestCase):
    from .models import LogicalDeletionModel

    model = LogicalDeletionModel

    def _register_items(self, *args):
        for item in args:
            self.model.objects.create(name=item)

    def _heard_delete(self):
        for i in self.model.all():
            i.delete(heard=True)

    def test_delete(self):
        self._register_items(*[str(i) for i in range(10)])
        item = self.model.objects.get(name="0")
        item.delete()
        self.assertNotEqual(item.deleted_at, None)

    def test_heard_delete(self):
        self._register_items(*[str(i) for i in range(10)])
        item = self.model.objects.get(name="0")
        item.delete(hard=True)
        with self.assertRaises(self.model.DoesNotExist):
            self.model.objects.get(name="0")

    def test_alive(self):
        self._register_items(*[str(i) for i in range(10)])
        item = self.model.objects.get(name="0")
        item.delete()
        self.assertEqual(len(self.model.objects.alive()), 9)

    def test_dead(self):
        self._register_items(*[str(i) for i in range(10)])
        item = self.model.objects.get(name="0")
        item.delete()
        self.assertEqual(len(self.model.objects.dead()), 1)
