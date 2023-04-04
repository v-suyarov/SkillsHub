import os
import sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SkillsHub.settings')
django.setup()
import os
from django.conf import settings
from PIL import Image, ImageDraw
import random
import string
from MainSite.models import Skill, Student

print("a")
a :int = 1
a :list[int] = list()
# skills = ["C++", "Python"]
# prog_lang = Skill.objects.get(name='Языки программирования')
# children = prog_lang.child_skills.all()

# high_level = Skill(name='Высокоуровневые', parent_skill=prog_lang)
# high_level.save()
#
# low_level = Skill(name='Низкоуровневые', parent_skill=prog_lang)
# low_level.save()
#
# prog_lang.child_skills.add(high_level, low_level)

