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

class AutoOneToOneField(OneToOneField):
	'''
		A OneToOne field that will create of the model if the related model follows
		the reverse relation and it hasn't been created yet.
		
		You can pass 'defaults' to specify the new creation defaults to pass to
		get_or_create.  It should be either a dict, or a callable that accepts one
		parameter: the instance following the relation.
	'''

	def contribute_to_related_class(self, cls, related):
		setattr(cls, related.get_accessor_name(), AutoSingleRelatedObjectDescriptor(related))
