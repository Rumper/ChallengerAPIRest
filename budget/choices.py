from django.utils.translation import ugettext_lazy as _

PUBLISHED = 'pub'
PENDING = 'pen'
DISCARDED = 'dis'


STATUS = (
    (PUBLISHED, _('Published')),
    (PENDING, _('Pending')),
    (DISCARDED, _('Discarded')),
)

STATUS_DICT = dict((k, v) for k, v in STATUS)


