from django.db import models
from django.db.models import OneToOneField
from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.related import SingleRelatedObjectDescriptor

class AutoSingleRelatedObjectDescriptor(SingleRelatedObjectDescriptor):
	def __get__(self, instance, instance_type=None):
		try:
			return super(AutoSingleRelatedObjectDescriptor, self).__get__(instance, instance_type)
		except self.related.model.DoesNotExist:
			obj = self.related.model(**{self.related.field.name: instance})
			obj.save()
			return obj
#class AutoSingleRelatedObjectDescriptor(related.SingleRelatedObjectDescriptor):
#	def __init__(self, related, defaults=None):
#		self._defaults = defaults or {}
#		super(AutoSingleRelatedObjectDescriptor, self).__init__(related)
#
#		def __get__(self, instance, instance_type=None):
#			if instance is None:
#				return self
#
#			try :
#				return getattr(instance, self.cache_name)
#			except AttributeError:
#				rel = self.related
#				params = {'%s' % rel.field.name: instance}
#				defaults = self._defaults
#				if callable(defaults):
#					defaults = defaults(instance)
#				params['defaults'] = self._defaults
#				db = router.db_for_read(rel.model, instance=instance)
#				rel_obj = rel.modem._base_manager.using(db).get_or_create(**params)[0]
#				setattr(instance, self.cache_name, rel_obj)
#				return rel_obj

class AutoOneToOneField(OneToOneField):
	'''
		A OneToOne field that will create of the model if the related model follows
		the reverse relation and it hasn't been created yet.
		
		You can pass 'defaults' to specify the new creation defaults to pass to
		get_or_create.  It should be either a dict, or a callable that accepts one
		parameter: the instance following the relation.
	'''

#	def __init__(self, *args, **kwargs):
#		super(AutoOneToOneField, self).__init__(*args, **kwargs)
#		self.defaults = kwargs.get('defaults', {})

	def contribute_to_related_class(self, cls, related):
		setattr(cls, related.get_accessor_name(), AutoSingleRelatedObjectDescriptor(related))
